import hashlib
import json
import re
from typing import Dict, Any

from .policy_schema import Policy

class GovernanceModelMock:
    """
    Mock governance model: builds a prompt from the policy template and context,
    returns a deterministic pseudo risk score in [0,100].
    """

    @staticmethod
    def build_prompt(policy: Policy, context_data: Dict[str, Any]) -> str:
        prompt = policy.risk_prompt_template
        # Replace [KEY] with str(value); keys are case-insensitive, prefer upper-case
        for k, v in context_data.items():
            token = f"[{str(k).upper()}]"
            prompt = prompt.replace(token, str(v))
        return prompt

    @staticmethod
    def get_risk_score(prompt: str) -> float:
        # If prompt contains explicit override like RISK_SCORE=95, honor it (for tests)
        m = re.search(r"RISK_SCORE\s*=\s*(\d+(?:\.\d+)?)", prompt)
        if m:
            try:
                val = float(m.group(1))
                return max(0.0, min(100.0, val))
            except ValueError:
                pass
        # Deterministic pseudo-score via hash
        h = hashlib.sha256(prompt.encode("utf-8")).digest()
        score = h[0] % 101  # 0..100
        return float(score)
