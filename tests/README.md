# Table-driven tests

Edit `tests.json` to add cases. Example case structure:

```
{
  "name": "example",
  "policy": "POLICY_NAME",
  "ctx": {"KEY": "VALUE"},
  "risk_score": 95.0,
  "expected": {
    "policy_decision": "approved",
    "directive_present": true,
    "audit_delta": 1
  }
}
```

- `risk_score` is optional; when omitted the normal model is used.
- `audit_delta` is optional; include it to assert audit row increments.

Run:

```
py tests\\run_tests.py
```
