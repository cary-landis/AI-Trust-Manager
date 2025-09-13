# Policies (Component #1)

Write policies as JSON files placed in this folder (or a subfolder). The API reads from `policies/` on each request.

Schema (MVP):
- `policy_name` (string)
- `purpose` (string)
- `risk_prompt_template` (string; placeholders like `[AGE]`)
- `trigger_condition` (string; only `RISK_SCORE [>, >=, ==, <=, <] NUMBER`)
- `output_directives` (object)
  - `action` (string)
  - `log_event` (boolean)
- `security_level` (CRITICAL|HIGH|MEDIUM|LOW)
- `governance_model` (string)

Example in `samples/basement_safety_alert.json`.
