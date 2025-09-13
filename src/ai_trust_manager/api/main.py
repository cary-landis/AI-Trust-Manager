from __future__ import annotations
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Optional

from ai_trust_manager.core.engine import AdaptivePolicyEngine

app = FastAPI(title="AI Trust Manager API", version="0.1.0")
engine = AdaptivePolicyEngine()

class EvaluateRequest(BaseModel):
    policy_name: str
    context_data: Dict[str, Any]

@app.post("/api/v1/evaluate")
def evaluate(req: EvaluateRequest):
    if not req.policy_name:
        raise HTTPException(status_code=400, detail="policy_name is required")
    res = engine.evaluate(req.policy_name, req.context_data)
    if "error" in res and res["error"] == "policy_not_found":
        raise HTTPException(status_code=404, detail="policy not found")
    return res
