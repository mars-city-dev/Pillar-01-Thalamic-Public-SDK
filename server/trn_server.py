"""
Titaness TRN Appliance (v1.0 - Commercial Service)
===================================================
Standalone Gating & Aversive Learning Service.
Handles Identity Verification, Deduplication, and Salience Filtering.
"""

import os
from fastapi import FastAPI, HTTPException
from typing import Dict, Any
from thalamic_reticular_nucleus import ThalamicReticularNucleus

app = FastAPI(title="Titaness TRN Gating Appliance")

# Initialize the core TRN logic
trn = ThalamicReticularNucleus()

@app.post("/evaluate")
async def evaluate_signal_ingress(payload: Dict[str, Any]):
    """
    Evaluates a sensory signal for admission into the federation.
    Returns ADMITTED or GATED (with Aversive Feedback).
    """
    admitted, reason = trn.evaluate_signal(payload)
    
    if not admitted:
        # Commercial Innovation: Active Aversive Feedback (Signal 49)
        # This trains the agent to self-regulate its throughput.
        return {
            "status": "GATED",
            "reason": reason,
            "aversive_feedback": {
                "signal_id": 49,
                "name": "KAPPA_OPIOID",
                "intensity": 0.85,
                "instruction": "LOCALLY_DAMPEN_THROUGHPUT_BY_50_PERCENT",
                "cooldown_sec": 30
            }
        }
    
    return {
        "status": "ADMITTED",
        "reason": reason,
        "metadata": {
            "mhc_verification": "SUCCESS",
            "deduplication": "PASSED"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "ACTIVE", "logic_version": "5.5-Enterprise"}

if __name__ == "__main__":
    import uvicorn
    print("🛡️ TITANESS TRN APPLIANCE ONLINE (Port 8002)")
    uvicorn.run(app, host="0.0.0.0", port=8002)
