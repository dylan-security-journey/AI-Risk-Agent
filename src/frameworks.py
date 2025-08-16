
# NIST CSF v2 "functions" and a compact questionnaire.

NIST_FUNCTIONS = ["G", "ID", "PR", "DE", "RS", "RC"]

QUESTIONS = [
    ("Q1",  "Do you have a defined security governance/RACI approved in the last 12 months?", "G",  "Governance/Roles"),
    ("Q2",  "Do you maintain a current asset inventory incl. data classification?",            "ID", "Asset Inventory"),
    ("Q3",  "Do all privileged accounts enforce MFA?",                                         "PR", "AC/IA"),
    ("Q4",  "Is joiner/mover/leaver (deprovision ≤ 24h) consistently applied?",                "PR", "AC-2"),
    ("Q5",  "Are endpoints/servers patched within policy (e.g., 14/30 days)?",                 "PR", "Vuln Mgmt"),
    ("Q6",  "Do critical systems forward auth/network logs to SIEM with required fields?",     "DE", "AU/Logging"),
    ("Q7",  "Do you have detections for brute force, admin misuse, and malware beaconing?",    "DE", "Detection Eng"),
    ("Q8",  "Do you run a documented incident response plan with on-call & SLAs?",             "RS", "IR-Plan"),
    ("Q9",  "Is phishing/awareness training completed ≥98% within due dates?",                 "PR", "AT-2"),
    ("Q10", "Are backups immutable and last restore test ≤ 90 days?",                           "RC", "Backups/DR"),
    ("Q11", "Do you track third-party risk (security reviews/DPAs) for critical vendors?",     "G",  "TPRM"),
    ("Q12", "Is configuration baseline defined and drift monitored/ticketed?",                  "PR", "CM-2"),
]

def default_function_impacts(assets: dict) -> dict:
    """Impact multipliers by CSF function based on asset profile.
    1.0 = neutral; >1 amplifies risk if function fails."""
    critical = int(assets.get("critical_systems", 0))
    has_cui   = bool(assets.get("handles_cui", False))
    has_pii   = bool(assets.get("handles_pii", False))

    impact = {f: 1.0 for f in ["G","ID","PR","DE","RS","RC"]}
    impact["PR"] += 0.2 if has_cui or has_pii else 0.0
    impact["DE"] += 0.2 if critical >= 5 else 0.0
    impact["RS"] += 0.1 if critical >= 3 else 0.0
    impact["RC"] += 0.3 if critical >= 3 else 0.0
    impact["ID"] += 0.1 if critical >= 5 else 0.0
    impact["G"]  += 0.1 if (has_cui or has_pii) else 0.0
    for k,v in impact.items():
        impact[k] = max(0.5, min(1.3, round(v,2)))
    return impact
