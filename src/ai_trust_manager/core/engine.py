from __future__ import annotations
from .engine_AI import get_risk_score
import json
import re
from pathlib import Path
from typing import Any, Dict, Optional

from .policy_schema import Policy
from .governance_mock import GovernanceModelMock
from .audit import add_audit_entry

POLICIES_DIR = Path("policies")


class PolicyRepository:
    def __init__(self, folder: Path = POLICIES_DIR):
        self.folder = folder

    def get_by_name(self, policy_name: str) -> Optional[Policy]:
        if not self.folder.exists():
            return None
        for p in self.folder.rglob("*.json"):
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                pol = Policy.model_validate(data)
                if pol.policy_name.lower() == policy_name.lower():
                    return pol
            except Exception:
                continue
        return None


def eval_condition(condition: str, risk_score: float) -> bool:
    m = re.match(r"^\s*RISK_SCORE\s*(>=|<=|>|<|==)\s*(\d+(?:\.\d+)?)\s*$", condition, re.IGNORECASE)
    if not m:
        return False
    op = m.group(1)
    threshold = float(m.group(2))
    if op == ">":
        return risk_score > threshold
    if op == ">=":
        return risk_score >= threshold
    if op == "<":
        return risk_score < threshold
    if op == "<=":
        return risk_score <= threshold
    if op == "==":
        return abs(risk_score - threshold) < 1e-9
    return False


class AdaptivePolicyEngine:
    def __init__(self, repo: PolicyRepository | None = None):
        self.repo = repo or PolicyRepository()

    def evaluate(self, policy_name: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
        policy = self.repo.get_by_name(policy_name)
        if policy is None:
            return {"error": "policy_not_found"}

        # Build prompt and compute risk score
        prompt = GovernanceModelMock.build_prompt(policy, context_data)
        risk_score = get_risk_score(prompt, context_data)

        # Evaluate condition
        triggered = eval_condition(policy.trigger_condition, risk_score)
        decision = "approved" if triggered else "denied"
        directive = policy.output_directives.model_dump()

        # Audit
        add_audit_entry(
            policy_name=policy.policy_name,
            security_level=policy.security_level.value,
            context_obj=context_data,
            risk_score=risk_score,
            decision=decision,
            directive_obj=directive,
            error=None if re.match(r"^\s*RISK_SCORE\s*(>=|<=|>|<|==)\s*", policy.trigger_condition, re.IGNORECASE) else "invalid_trigger"
        )

        return {
            "policy_decision": decision,
            "directive": directive if triggered else None,
            "triggered_policy": policy.policy_name,
            "risk_score": risk_score,
        }
