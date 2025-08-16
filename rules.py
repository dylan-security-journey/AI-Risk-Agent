
from typing import Dict, List, Tuple
from .frameworks import QUESTIONS, NIST_FUNCTIONS

RECOMMENDATIONS = {
    "Q1":  "Formalize security governance (RACI, committees) and review annually.",
    "Q2":  "Deploy/maintain asset inventory with data classification and ownership.",
    "Q3":  "Enforce MFA for all privileged accounts via IdP/conditional access.",
    "Q4":  "Automate deprovisioning; run monthly access reviews for high-risk apps.",
    "Q5":  "Set patch SLAs (14/30/90), automate deployment, and verify compliance.",
    "Q6":  "Forward auth/network logs to SIEM with user/IP/timestamp; validate fields.",
    "Q7":  "Add detections for brute force, privilege abuse, and beaconing; tune alerts.",
    "Q8":  "Publish IR plan with roles, on-call rotation, runbooks, and SLAs; tabletop test.",
    "Q9":  "Require role-based training; track completion ≥98% within due dates.",
    "Q10": "Use immutable backups; perform quarterly restore testing and document results.",
    "Q11": "Establish vendor security reviews/DPAs; track critical suppliers in a register.",
    "Q12": "Define secure baselines; detect and ticket configuration drift automatically.",
}

def function_weights(custom: Dict[str, float]|None=None) -> Dict[str, float]:
    base = {f:1.0 for f in NIST_FUNCTIONS}
    if custom:
        base.update(custom)
    s = sum(base.values())
    return {k: v/s for k,v in base.items()}

def score_functions(answers: Dict[str,int], q_weights: Dict[str,float]) -> Tuple[Dict[str,float], List[dict]]:
    sums = {f:0.0 for f in NIST_FUNCTIONS}
    wts  = {f:0.0 for f in NIST_FUNCTIONS}
    audit=[]
    for qid, text, func, _ in QUESTIONS:
        score0_5 = int(answers.get(qid, 0))
        w = float(q_weights.get(qid, 1.0))
        sums[func] += score0_5 * w
        wts[func]  += w
        audit.append({"question": qid, "function": func, "score": score0_5, "weight": w, "text": text})
    maturity = {f: (sums[f]/wts[f]/5.0 if wts[f]>0 else 0.0) for f in NIST_FUNCTIONS}
    return maturity, audit

def recommend_lows(answers: Dict[str,int], threshold:int=2) -> List[str]:
    items=[]
    for qid, _, _, _ in QUESTIONS:
        if int(answers.get(qid,0)) <= threshold:
            items.append(f"{qid}: {RECOMMENDATIONS[qid]}")
    return items
