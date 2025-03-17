from pydantic import BaseModel
from typing import Dict, Any

class FindingsResponse(BaseModel):
    results: Dict[str, Any]
