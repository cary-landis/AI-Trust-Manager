from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional

class SecurityLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class OutputDirectives(BaseModel):
    action: str = Field(default="none")
    log_event: bool = Field(default=True, alias="log_event")

class Policy(BaseModel):
    policy_name: str
    purpose: str
    risk_prompt_template: str
    trigger_condition: str
    output_directives: OutputDirectives
    security_level: SecurityLevel
    governance_model: str
