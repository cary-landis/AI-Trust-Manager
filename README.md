# AI Trust Manager (MVP)

Python FastAPI MVP for evaluating AI governance policies with probabilistic risk via a mock Governance Model. No GUI. Simple, mainstream stack.

- API: FastAPI (POST `/api/v1/evaluate`)
- Storage: SQLite for audit logs (`app_data/audit.db`)
- Policies: JSON files in `policies/`
- License: MIT

Quickstart (Windows PowerShell)

1. Create a venv and install deps
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run API
```
uvicorn --app-dir src ai_trust_manager.api.main:app --reload --port 5080
```

3. Try it
```
Invoke-RestMethod -Method POST http://localhost:5080/api/v1/evaluate `
  -ContentType "application/json" `
  -Body '{"policy_name":"Basement Safety Alert","context_data":{"AGE":90,"HISTORICAL_MINUTES_IN_LOCATION":"5,7,5,3,10,14,7","CURRENT_MINUTES_IN_LOCATION":40,"LOCATION":"basement"}}'
```

4. Run tests
```
pytest -q
```

One-command helpers (Windows PowerShell)
- Run the API: `scripts\run.ps1`
- Run tests: `scripts\test.ps1`

Release checklist
- All tests pass locally: `pytest -q`
- API runs locally: `scripts\\run.ps1` and hit `http://127.0.0.1:5080/docs`
- CI green on main (GitHub Actions)

Tag and push v1.0.0
```
git add .
git commit -m "v1.0.0: MVP engine, API, policies"
git tag v1.0.0
git push origin main --tags
```

Folder structure
```
policies/ (Component #1)
  README.md
  samples/
    basement_safety_alert.json
src/
  ai_trust_manager/
    core/ (Component #2)
    api/  (Component #3)
tests/
app_data/
```
