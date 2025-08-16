
import argparse, json
from pathlib import Path
import yaml
import pandas as pd

from .frameworks import QUESTIONS, default_function_impacts, NIST_FUNCTIONS
from .rules import function_weights, score_functions, recommend_lows

def load_yaml(p): 
    with open(p, "r", encoding="utf-8") as f: 
        return yaml.safe_load(f) or {}

def compute_risk(answers, assets, weights_cfg):
    q_weights = weights_cfg.get("question_weights", {})
    func_w    = function_weights(weights_cfg.get("function_weights"))
    maturity, audit = score_functions(answers, q_weights)
    impact = default_function_impacts(assets)

    func_risk = {f: round((1.0 - maturity[f]) * 100.0 * impact[f], 1) for f in NIST_FUNCTIONS}
    overall = round(sum(func_risk[f]*func_w[f] for f in NIST_FUNCTIONS), 1)

    def level(x): 
        return "High" if x>=70 else ("Medium" if x>=40 else "Low")

    summary = {
        "maturity": {f: round(maturity[f],2) for f in NIST_FUNCTIONS},
        "impact": impact,
        "function_risk": func_risk,
        "overall_risk": overall,
        "overall_level": level(overall),
    }

    recs = recommend_lows(answers, threshold=2)
    return summary, audit, recs

def to_csv(out_csv, audit, func_risk, overall):
    rows=[]
    for a in audit:
        rows.append({
            "question": a["question"],
            "function": a["function"],
            "score": a["score"],
            "weight": a["weight"],
            "text": a["text"],
        })
    for f, r in func_risk.items():
        rows.append({"question": f, "function": f, "score": "", "weight": "", "text": f"FUNC_RISK={r}"})
    rows.append({"question": "OVERALL", "function": "", "score":"", "weight":"", "text": f"OVERALL_RISK={overall}"})
    pd.DataFrame(rows).to_csv(out_csv, index=False)

def main():
    ap = argparse.ArgumentParser(description="AI Risk Assessment Agent (NIST CSF v2)")
    ap.add_argument("assess", nargs="?", default="assess")
    ap.add_argument("--answers", required=True, help="YAML of Q1..Q12 scores (0..5)")
    ap.add_argument("--assets",  required=False, help="YAML asset profile", default=None)
    ap.add_argument("--outdir",  required=False, default="outputs")
    ap.add_argument("--weights", required=False, default="config/weights.yml")
    args = ap.parse_args()

    Path(args.outdir).mkdir(parents=True, exist_ok=True)

    answers = load_yaml(args.answers)
    assets  = load_yaml(args.assets) if args.assets else {}
    weights = load_yaml(args.weights) if Path(args.weights).exists() else {}

    summary, audit, recs = compute_risk(answers, assets, weights)
    report = {
        "answers": answers,
        "assets": assets,
        "summary": summary,
        "recommendations": recs,
        "questions": [{"id": qid, "text": text, "function": func} for qid, text, func, _ in QUESTIONS],
    }

    out_json = Path(args.outdir) / "report.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    out_csv = Path(args.outdir) / "report.csv"
    to_csv(out_csv, audit, summary["function_risk"], summary["overall_risk"])

    out_txt = Path(args.outdir) / "summary.txt"
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(f"Overall Risk: {summary['overall_risk']} ({summary['overall_level']})\n")
        for fkey in NIST_FUNCTIONS:
            f.write(f"{fkey}: risk={summary['function_risk'][fkey]} maturity={summary['maturity'][fkey]} impact={summary['impact'][fkey]}\n")
        f.write("\nTop recommendations:\n- " + "\n- ".join(recs[:6]))

    print(f"✅ Wrote {out_json}, {out_csv}, {out_txt}")

if __name__ == "__main__":
    main()
