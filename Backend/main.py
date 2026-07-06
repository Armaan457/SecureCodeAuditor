from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from utils import extract_json,validate_repository, clone_repo,  validate_github_url, get_cache_key, cache_exists, load_cache, save_cache, load_repo_files
from Agent import analyze_file
from models import AgentResults, VulnerabilityFinding, RepoRequest
from pydantic import ValidationError
import concurrent.futures

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://sca.armaanjagirdar.me"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze", response_model=AgentResults)
async def analyze_repo(request: RepoRequest):
    owner, repo = validate_github_url(str(request.github_url))
    sha = await validate_repository(owner, repo)

    cache_key = get_cache_key(sha)

    if cache_exists(cache_key):
        # print("Cache Hit")
        return AgentResults(**load_cache(cache_key))

    temp_repo = clone_repo(str(request.github_url))

    try:
        files = load_repo_files(temp_repo.name)
        if not files:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No supported source files found."
            )

        all_findings = {}

        def process_file(filename, content):
            result = analyze_file(filename, content)
            findings_list = []
            seen = set()
            for output in result["results"]:
                json_found = extract_json(output["output"].content)
                for item in json_found:
                    findings = item.get("findings", [])
                    if not isinstance(findings, list):
                        continue
                    for finding in findings:
                        try:
                            finding = VulnerabilityFinding.model_validate(finding)
                        except ValidationError:
                            continue

                        key = (finding.vulnerability_type, finding.code_snippet)
                        if key in seen:
                            continue
                        seen.add(key)
                        findings_list.append(finding)
            return filename, findings_list

        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {
                    executor.submit(process_file, filename, content): filename
                    for filename, content in files.items()
                }
                for future in concurrent.futures.as_completed(futures):
                    filename = futures[future]

                    try:
                        _, findings = future.result()
                        all_findings[filename] = findings
                    except Exception as e:
                        print(f"Error processing {filename}: {e}")
                        all_findings[filename] = []

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="We're still in prototype phase. Try again later."
            )
        response = AgentResults(results=all_findings)
        save_cache(
            cache_key=cache_key,
            findings=response.model_dump(),
        )
        return response
    finally:
        temp_repo.cleanup()
