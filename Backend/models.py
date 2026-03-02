from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict

class VulnerabilityFinding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    vulnerability_type: Optional[str] = Field(
        None, 
        description="Type of vulnerability found"
    )
    code_snippet: Optional[str] = Field(
        None, 
        description="Code snippet showing the vulnerability"
    )
    recommendation: Optional[str] = Field(
        None, 
        description="Recommended fix for the vulnerability"
    )

class FindingsResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    findings: List[VulnerabilityFinding] = Field(
        default_factory=list,
        description="List of vulnerability findings"
    )

class AgentResults(BaseModel):
    model_config = ConfigDict(extra="forbid")

    results: Dict[str, List[VulnerabilityFinding]] = Field(
        default_factory=dict,
        description="Results from each file analyzed"
    )
