import json
import re
import zipfile
import io

ALLOWED_EXTENSIONS = {'.py', '.js', '.ts', '.json', '.jsx', '.tsx', '.java', '.xml', '.html', '.css', '.go', '.c', '.cpp'}

def extract_json(target):
    
    json_pattern = r'```json\n(.*)\n```'
    json_matches = re.findall(json_pattern, target, re.DOTALL)

    extracted_jsons = []

    for match in json_matches:
        try:
            json_data = json.loads(match)
            if not (isinstance(json_data, dict) and json_data.get('findings') == []):
                extracted_jsons.append(json_data)        
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print(f"Problematic JSON String: {match}")
            return extracted_jsons
    
    return extracted_jsons


async def extract_zip_files(file):
    files = {}
    
    contents = await file.read()
    with zipfile.ZipFile(io.BytesIO(contents)) as zip_ref:
        for file_name in zip_ref.namelist():
            if not file_name.endswith('/'): 
                extension = '.' + file_name.split('.')[-1]
                if extension in ALLOWED_EXTENSIONS:
                    with zip_ref.open(file_name) as f:
                        files[file_name] = f.read().decode('utf-8')
    
    return files