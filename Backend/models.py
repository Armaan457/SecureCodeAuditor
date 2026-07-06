from pydantic import BaseModel, Field, ConfigDict, HttpUrl, model_validator
from typing import List, Literal, Dict

class RepoRequest(BaseModel):
    github_url: HttpUrl

class VulnerabilityFinding(BaseModel):
    model_config = ConfigDict(extra="forbid")
    vulnerability_type: str = Field(
        ...,
        description="Type of vulnerability found"
    )
    severity: Literal["Critical", "High", "Medium", "Low", "Informational"] = Field(
        ...,
        description="Severity of the vulnerability"
    )
    confidence: Literal["High", "Medium"] = Field(
        ...,
        description="Confidence level of the finding"
    )
    code_snippet: str = Field(
        ...,
        min_length=1,
        description="Exact vulnerable code snippet"
    )
    reason: str = Field(
        ...,
        min_length=1,
        description="Explanation of why the code is vulnerable"
    )
    recommendation: str = Field(
        ...,
        min_length=1,
        description="Recommended remediation"
    )

    @model_validator(mode="after")
    def strip_and_validate(self):
        for field in ("vulnerability_type", "code_snippet", "reason", "recommendation"):
            value = getattr(self, field).strip()
            if not value:
                raise ValueError(f"{field} cannot be blank")
            setattr(self, field, value)
        return self

class AgentResults(BaseModel):
    model_config = ConfigDict(extra="forbid")
    results: Dict[str, List[VulnerabilityFinding]] = Field(
        default_factory=dict,
        description="Results grouped by filename"
    )
