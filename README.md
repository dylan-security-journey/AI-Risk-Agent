
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
python -m src.risk_agent assess \  --answers data/sample_responses.yml \  --assets  data/sample_assets.yml \  --outdir  outputs
```

Outputs:
- `outputs/report.json` – scores, heatmap, recs, audit trail
- `outputs/report.csv`  – flattened, analyst-friendly
- `outputs/summary.txt` – quick console summary

## NIST CSF v2 mapping
We use 12 lightweight questions mapped to the six CSF functions: **G/ID/PR/DE/RS/RC**.  
Weights live in `config/weights.yml`. Tweak them per org risk appetite.

## Risk formula (simple, explainable)
For each function:
```
maturity = weighted_avg(question_scores 0..5) / 5
impact   = function_impact_from_assets (0.5..1.3)
risk_f   = round((1 - maturity) * 100 * impact, 1)
```
Overall risk = weighted average of function risks.

## Optional LLM narrative
Set `OPENAI_API_KEY` in your environment to enable narrative `recommendations_llm` (future enhancement).  
If not set, rule-based recommendations are used.

## License
MIT
