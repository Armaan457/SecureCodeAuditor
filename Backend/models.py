from pydantic import BaseModel, Field, ConfigDict, model_validator
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

    @model_validator(mode="after")
    def validate_dependent_fields(self):
        if self.vulnerability_type is not None:
            if not self.code_snippet or not self.code_snippet.strip():
                raise ValueError("code_snippet cannot be null or empty when vulnerability_type is provided")
            if not self.recommendation or not self.recommendation.strip():
                raise ValueError("recommendation cannot be null or empty when vulnerability_type is provided")
        return self

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
