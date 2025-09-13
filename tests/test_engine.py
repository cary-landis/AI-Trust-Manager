from __future__ import annotations
from pathlib import Path
from sqlalchemy import create_engine, text

from ai_trust_manager.core.engine import AdaptivePolicyEngine, PolicyRepository
from ai_trust_manager.core import governance_mock

SAMPLES = Path("policies/samples")


def _audit_count() -> int:
    eng = create_engine("sqlite:///app_data/audit.db")
    with eng.connect() as conn:
        # Table is created on first import; if missing, treat as 0
        try:
            result = conn.execute(text("SELECT COUNT(*) FROM audit_logs"))
            return int(result.scalar() or 0)
        except Exception:
            return 0


def test_approved_when_fixed_risk_above_threshold(monkeypatch):
    # Force deterministic risk score = 95
    monkeypatch.setattr(
        governance_mock.GovernanceModelMock,
        "get_risk_score",
        staticmethod(lambda prompt: 95.0),
        raising=False,
    )
    repo = PolicyRepository(folder=SAMPLES)
    engine = AdaptivePolicyEngine(repo)
    ctx = {"AGE": 90, "CURRENT_MINUTES_IN_LOCATION": 40, "LOCATION": "basement"}
    before = _audit_count()
    res = engine.evaluate("Basement Safety Alert", ctx)
    after = _audit_count()
    assert res["policy_decision"] == "approved"
    assert res["directive"] is not None
    assert after == before + 1


def test_denied_when_fixed_risk_below_threshold(monkeypatch):
    # Force deterministic risk score = 10
    monkeypatch.setattr(
        governance_mock.GovernanceModelMock,
        "get_risk_score",
        staticmethod(lambda prompt: 10.0),
        raising=False,
    )
    repo = PolicyRepository(folder=SAMPLES)
    engine = AdaptivePolicyEngine(repo)
    ctx = {"AGE": 20, "CURRENT_MINUTES_IN_LOCATION": 1}
    before = _audit_count()
    res = engine.evaluate("Basement Safety Alert", ctx)
    after = _audit_count()
    assert res["policy_decision"] == "denied"
    assert res["directive"] is None
    assert after == before + 1
