import json
import re
import os
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlparse
import httpx
from fastapi import HTTPException
from upstash_redis import Redis
from dotenv import load_dotenv
load_dotenv()

def extract_json(target):
    if not target:
        return []

    extracted_jsons = []
    decoder = json.JSONDecoder()

    def append_if_valid(parsed):
        if not isinstance(parsed, dict):
            return

        findings = parsed.get("findings")
        if not isinstance(findings, list):
            return

        if len(findings) == 0:
            return

        extracted_jsons.append(parsed)

    def parse_from_text(text):
        index = 0
        text_length = len(text)

        while index < text_length:
            next_obj = text.find("{", index)
            next_arr = text.find("[", index)

            candidates = [position for position in [next_obj, next_arr] if position != -1]
            if not candidates:
                break

            start = min(candidates)
            try:
                parsed, end = decoder.raw_decode(text, start)
                if isinstance(parsed, list):
                    for item in parsed:
                        append_if_valid(item)
                else:
                    append_if_valid(parsed)
                index = end
            except json.JSONDecodeError:
                index = start + 1

    fenced_pattern = r"```(?:json)?\s*(.*?)\s*```"
    fenced_matches = re.findall(fenced_pattern, target, re.DOTALL | re.IGNORECASE)

    for match in fenced_matches:
        parse_from_text(match)

    parse_from_text(target)

    unique_jsons = []
    seen = set()
    for item in extracted_jsons:
        fingerprint = json.dumps(item, sort_keys=True)
        if fingerprint not in seen:
            seen.add(fingerprint)
            unique_jsons.append(item)

    return unique_jsons


CACHE_VERSION = os.getenv("CACHE_VERSION", "v1")
CACHE_TTL = int(os.getenv("CACHE_TTL", "86400"))
redis = Redis(
    url=os.getenv("UPSTASH_REDIS_REST_URL"),
    token=os.getenv("UPSTASH_REDIS_REST_TOKEN"),
)

CLONE_TIMEOUT = 60
MAX_REPO_SIZE_KB = 40 * 1024 
MAX_FILES = 10
ALLOWED_EXTENSIONS = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.html', '.css', '.go', '.c', '.cpp'}

def get_cache_key(owner: str, repo: str, commit_sha: str):
    return f"{CACHE_VERSION}:{owner}:{repo}:{commit_sha}"

def validate_github_url(url: str):
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise HTTPException(400, "Invalid URL.")
    if parsed.netloc.lower() != "github.com":
        raise HTTPException(400, "Only GitHub repositories are supported.")

    parts = parsed.path.strip("/").split("/")

    if len(parts) < 2:
        raise HTTPException(
            400,
            "Repository URL must be https://github.com/<owner>/<repo>"
        )
    owner = parts[0]
    repo = parts[1].removesuffix(".git")
    return owner, repo

def get_latest_commit_sha(repo_url: str) -> str:
    try:
        result = subprocess.run(
            ["git", "ls-remote", repo_url, "HEAD"],
            capture_output=True,
            text=True,
            timeout=20,
            check=True,
        )
        return result.stdout.split()[0]

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to access repository."
        )

def cache_exists(cache_key: str) -> bool:
    return redis.exists(cache_key) == 1
def load_cache(cache_key: str):
    cached = redis.get(cache_key)
    if cached is None:
        return None
    if isinstance(cached, str):
        return json.loads(cached)
    return cached
def save_cache(cache_key: str, findings: dict):
    redis.set(
        cache_key,
        json.dumps(findings),
        ex=CACHE_TTL,
    )

def clone_repo(repo_url: str):
    temp_dir = tempfile.TemporaryDirectory()
    try:
        subprocess.run(
            ["git", "clone", "--depth",  "1", repo_url, temp_dir.name],
            check=True,
            timeout=CLONE_TIMEOUT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except subprocess.TimeoutExpired:
        temp_dir.cleanup()
        raise HTTPException(408, "Repository clone timed out.")
    except subprocess.CalledProcessError as e:
        temp_dir.cleanup()
        raise HTTPException(400, e.stderr)
    return temp_dir


async def validate_repository(owner: str, repo: str):
    async with httpx.AsyncClient(timeout=20) as client:
        repo_resp = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}"
        )
        if repo_resp.status_code != 200:
            raise HTTPException(
                404,
                "Repository not found."
            )

        repo_info = repo_resp.json()
        if repo_info["size"] > MAX_REPO_SIZE_KB:
            raise HTTPException(
                413,
                f"Repository exceeds {MAX_REPO_SIZE_KB // 1024} MB."
            )
        default_branch = repo_info["default_branch"]

        commit_resp = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/commits/{default_branch}"
        )
        if commit_resp.status_code != 200:
            raise HTTPException(400, "Unable to fetch latest commit.")
        sha = commit_resp.json()["sha"]

        tree_resp = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/git/trees/{default_branch}",
            params={"recursive": "1"},
        )
        if tree_resp.status_code != 200:
            raise HTTPException(400, "Unable to inspect repository.")
        tree = tree_resp.json()["tree"]
        file_count = sum(
            1
            for node in tree
            if (node["type"] == "blob" and Path(node["path"]).suffix.lower() in ALLOWED_EXTENSIONS)
        )
        if file_count > MAX_FILES:
            raise HTTPException(
                413,
                f"Repository contains more than {MAX_FILES} supported source files."
            )
        return sha

def load_repo_files(repo_path):
    files = {}
    for root, _, filenames in os.walk(repo_path):
        for filename in filenames:
            extension = os.path.splitext(filename)[1].lower()

            if extension not in ALLOWED_EXTENSIONS:
                continue

            path = os.path.join(root, filename)
            relative = os.path.relpath(path, repo_path)

            try:
                with open(path, "rb") as f:
                    content = f.read()
                for encoding in ("utf-8", "latin-1", "cp1252"):
                    try:
                        files[relative] = content.decode(encoding)
                        break
                    except UnicodeDecodeError:
                        pass
            except Exception:
                continue
    return files