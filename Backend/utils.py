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