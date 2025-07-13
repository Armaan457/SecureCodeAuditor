from fastapi import FastAPI, UploadFile, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from utils import extract_json, extract_zip_files
from Agent import analyze_file
from models import FindingsResponse
import concurrent.futures
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://secure-code-auditor.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze", response_model=FindingsResponse)
@limiter.limit("5/minute")
async def analyze_zip(file: UploadFile, request: Request):
    if not file.filename.endswith(".zip"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Only ZIP files are allowed."
        )
    
    files = await extract_zip_files(file)
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid files found in the ZIP."
        )
    
    all_findings = {}
    
    def process_file(filename, content):
        result = analyze_file(filename, content)
        findings_list = []

        for output in result['results']:
            json_found = extract_json(output['output'].content)
            for item in json_found:
                for finding in item.get('findings', []):
                    if not any(f["code_snippet"] == finding["code_snippet"] and f["vulnerability_type"] == finding["vulnerability_type"] for f in findings_list):
                        findings_list.append({
                            "vulnerability_type": finding["vulnerability_type"],
                            "code_snippet": finding["code_snippet"],
                            "recommendation": finding["recommendation"]
                        })

        return filename, findings_list

    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(process_file, filename, content): filename for filename, content in files.items()}
            for future in concurrent.futures.as_completed(futures):
                filename, findings = future.result()
                all_findings[filename] = findings
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"We're still in prototype phase. Try again later with less number of files"
        )

    return {"results": all_findings}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)