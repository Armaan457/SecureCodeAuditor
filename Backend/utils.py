import json
import re
import zipfile
import io

ALLOWED_EXTENSIONS = {'.py', '.js', '.ts', '.json', '.jsx', '.tsx', '.java', '.xml', '.html', '.css', '.go', '.c', '.cpp'}

def extract_json(target):
    if not target:
        return []

    extracted_jsons = []
    decoder = json.JSONDecoder()

    def append_if_valid(parsed):
        if not isinstance(parsed, dict):
            return

        findings = parsed.get("findings")
        if findings == []:
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


async def extract_zip_files(file):
    files = {}
    
    ignored_directories = {
        '__MACOSX', 
        '.DS_Store', 
    }
    
    contents = await file.read()
    with zipfile.ZipFile(io.BytesIO(contents)) as zip_ref:
        for file_name in zip_ref.namelist():
            if file_name.endswith('/'):
                continue
                
            should_skip = False
            for ignored in ignored_directories:
                if file_name.startswith(ignored) or f"/{ignored}" in file_name or file_name.endswith(ignored):
                    should_skip = True
                    break
            
            if should_skip:
                continue
                
            if '.' not in file_name:
                continue
                
            extension = '.' + file_name.split('.')[-1].lower()
            if extension in ALLOWED_EXTENSIONS:
                try:
                    with zip_ref.open(file_name) as f:
                        file_content = f.read()
                        try:
                            files[file_name] = file_content.decode('utf-8')
                        except UnicodeDecodeError:
                            try:
                                files[file_name] = file_content.decode('latin-1')
                            except UnicodeDecodeError:
                                try:
                                    files[file_name] = file_content.decode('cp1252')
                                except UnicodeDecodeError:
                                    print(f"Error: Could not decode file {file_name}, skipping...")
                                    continue
                except Exception as e:
                    print(f"Error: Could not extract file {file_name}: {e}")
                    continue
    
    return files