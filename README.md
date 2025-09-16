
# AI Trust Manager

## TL;DR
AI Trust Manager is an open-source Python framework for governing semi-autonomous AI agent-driven systems, especially in digital health. It helps developers build, test, and audit trust policies for AI agents using simulated or real AI risk scoring.

---

## What is AI Trust Manager?
Our innovation is the AI Trust Policy Manager for Semi-autonomous Digital Health Agents (AI Trust Manager), a software system that governs semi-autonomous AI agents. It solves the problem of under-governed AI agents performing risky actions in healthcare environments.

AI Trust Manager provides a flexible engine for evaluating context against policies, simulating AI risk scoring, and auditing decisions. It is designed for developers and researchers who want to experiment with AI policy governance, risk assessment, and compliance for agent-driven systems.

## Key Features
- Table-driven policy tests
- Modular policy engine (`AdaptivePolicyEngine`)
- Simulated AI risk scoring (easy to swap for real AI)
- Audit logging to SQLite (`audit.db`)
- Easy-to-extend policy schema and repository
- Open source and ready for contributions

## Quick Start
1. **Clone the repo:**
   ```
   git clone https://github.com/cary-landis/AI-Trust-Manager.git
   cd AI-Trust-Manager
   ```
2. **Set up Python environment:**
   - Use Python 3.13+ (virtual environment recommended)
   - Install dependencies:
     ```
     pip install -r requirements.txt
     ```
3. **Run tests:**
   ```
   python tests/run_tests.py
   ```

## How It Works
- **Policy Evaluation:**
  - Policies are defined in JSON files under `policies/samples/`.
  - The engine evaluates context against policy rules using a risk score.
  - AI risk scoring is simulated via `engine_AI.py` (replace with real AI when ready).
- **Testing:**
  - Table-driven tests are defined in `tests/tests.json`.
  - The test runner (`run_tests.py`) loads cases, evaluates policies, and checks audit logs.
- **Audit Logging:**
  - All decisions are logged to `app_data/audit.db` for traceability.

## Technical Details
- **Engine:** `src/ai_trust_manager/core/engine.py` implements the main policy evaluation logic.
- **AI Simulation:** `src/ai_trust_manager/core/engine_AI.py` simulates AI risk scoring. Pass `risk_score` in context for testing.
- **Audit:** `src/ai_trust_manager/core/audit.py` handles audit log entries.
- **Policy Schema:** `src/ai_trust_manager/core/policy_schema.py` defines policy structure.

## Contributing
Pull requests and issues are welcome! See the LICENSE file for terms. Please document your changes and add tests where possible.

## License
This project is licensed under the terms of the LICENSE file in the repository.
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
- Run the API: `scripts\run_app.ps1`
- Run tests: `scripts\run_tests.ps1`

Release checklist
- All tests pass locally: `pytest -q`
- API runs locally: `scripts\\run_app.ps1` and hit `http://127.0.0.1:5080/docs`
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
