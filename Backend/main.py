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
    allow_origins=["*"],
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
        try:
            result = analyze_file(filename, content)
            findings = []
            for output in result['results']:
                findings.extend(extract_json(output['output'].content))
            return filename, findings
        except Exception as e:
            return filename, {"error": str(e)}

    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(process_file, filename, content): filename for filename, content in files.items()}
            for future in concurrent.futures.as_completed(futures):
                filename, findings = future.result()
                all_findings[filename] = findings
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during file processing: {str(e)}"
        )

    return {"results": all_findings}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)