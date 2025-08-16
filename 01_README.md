# AI Risk Assessment Agent (NIST CSF v2)

A tiny Python agent that:
- ingests questionnaire answers and an optional asset profile,
- maps them to NIST CSF v2 functions (Govern, Identify, Protect, Detect, Respond, Recover),
- computes **function scores & overall risk (0–100)**,
- emits **JSON and CSV** for audit trails,
- (optional) drafts narrative recommendations with an LLM if `OPENAI_API_KEY` is set.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/risk_agent.py assess \
  --answers data/sample_responses.yml \
  --assets  data/sample_assets.yml \
  --outdir  outputs
