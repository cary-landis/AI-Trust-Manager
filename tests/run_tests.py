from __future__ import annotations
import json
import sqlite3
from contextlib import contextmanager, nullcontext
from pathlib import Path
import sys

# Anchor all paths off the repo root so this works no matter where it's run from
REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLES = REPO_ROOT / "policies" / "samples"
CASES_FILE = REPO_ROOT / "tests" / "tests.json"
AUDIT_DB = REPO_ROOT / "app_data" / "audit.db"

# Ensure local src is importable
sys.path.insert(0, str(REPO_ROOT / "src"))

from ai_trust_manager.core.engine import AdaptivePolicyEngine, PolicyRepository  # noqa: E402
from ai_trust_manager.core import governance_mock  # noqa: E402


def audit_count() -> int:
    try:
        con = sqlite3.connect(str(AUDIT_DB))
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM audit_logs")
        row = cur.fetchone()
        return int(row[0]) if row and row[0] is not None else 0
    except Exception:
        return 0
    finally:
        try:
            con.close()
        except Exception:
            pass


@contextmanager
def temp_attr(obj, name, value):
    had = hasattr(obj, name)
    old = getattr(obj, name, None)
    setattr(obj, name, value)
    try:
        yield
    finally:
        if had:
            setattr(obj, name, old)
        else:
            delattr(obj, name)


def run_case(case: dict) -> tuple[bool, str]:
    # Directly call engine.evaluate; AI call should be handled in engine or its module

    exp = case.get("expected", {})
    check_audit = "audit_delta" in exp
    before = audit_count() if check_audit else None

    try:
        repo = PolicyRepository(folder=SAMPLES)
        engine = AdaptivePolicyEngine(repo)
        res = engine.evaluate(case["policy"], case.get("ctx", {}))
    except Exception as e:
        return False, f"name={case.get('name','?')} policy={case.get('policy','?')} error={e}"

    checks: list[bool] = []
    details: list[str] = []

    if "policy_decision" in exp:
        ok_dec = res.get("policy_decision") == exp["policy_decision"]
        checks.append(ok_dec)
        details.append(f"decision exp={exp['policy_decision']} got={res.get('policy_decision')}")

    if "directive_present" in exp:
        got_present = res.get("directive") is not None
        ok_dir = got_present == exp["directive_present"]
        checks.append(ok_dir)
        details.append(f"directive_present exp={exp['directive_present']} got={got_present}")

    if check_audit and before is not None:
        after = audit_count()
        delta = after - before
        ok_audit = delta == exp["audit_delta"]
        checks.append(ok_audit)
        details.append(f"audit_delta exp={exp['audit_delta']} got={delta}")

    ok = all(checks) if checks else True
    msg = f"name={case.get('name','?')} policy={case.get('policy','?')} " + " | ".join(details)
    return ok, msg


def main() -> int:
    if not CASES_FILE.exists():
        print(f"No tests found: {CASES_FILE} not present")
        return 1
    cases = json.loads(CASES_FILE.read_text(encoding="utf-8"))
    if not isinstance(cases, list):
        print("tests.json must contain a JSON array of cases")
        return 1

    passed = failed = 0
    for case in cases:
        ok, msg = run_case(case)
        print(("PASS: " if ok else "FAIL: ") + msg)
        passed += int(ok)
        failed += int(not ok)

    total = passed + failed
    print(f"\nSummary: {passed}/{total} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
