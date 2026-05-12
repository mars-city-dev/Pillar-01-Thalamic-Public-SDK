"""
Titaness Thalamic Gateway Appliance: Sovereign Orchestrator (v5.9)
===================================================================
Master Ingress Node for the Commercial Triad.
Coordinates between:
- TRN Appliance (Port 8002) - Gating & Aversion
- vNeurochemical Server (Port 8001) - Metabolism
"""

import os
import json
import time
import httpx
import asyncio
import threading
from typing import Dict, Any
from fastapi import FastAPI, Request, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import JSONResponse
import uvicorn

from subcortical_watcher import SubcorticalWatcher

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Internal Appliance Endpoints (Can be mapped to GCP/AWS internal hostnames)
TRN_URL = os.getenv("TRN_URL", "http://localhost:8002/evaluate")
VNEURO_URL = os.getenv("VNEURO_URL", "http://localhost:8001/peptide")

def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == "sk_live_enterprise_123":
        return api_key_header
    raise HTTPException(status_code=401, detail="Unauthorized: Investigator Signet Required")

app = FastAPI(title="Titaness Thalamic Gateway (Orchestrator)")

async def orchestrate_signal(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Coordinates the 3-stage appliance pipeline.
    """
    async with httpx.AsyncClient() as client:
        try:
            # 1. TRN EVALUATION (Gating & Aversion)
            trn_resp = await client.post(TRN_URL, json=payload, timeout=2.0)
            decision = trn_resp.json()
            
            if decision["status"] == "GATED":
                return decision # Returns the Signal 49 Aversive Feedback
            
            # 2. METABOLIC PULSE (Glutamate Spike on Admission)
            # This updates the global mood for the next incoming signal.
            await client.post(f"{VNEURO_URL}/24/pulse", params={"intensity": 0.1})
            
            return {
                "status": "ADMITTED",
                "reason": decision["reason"],
                "mhc_verification": "SUCCESS"
            }
        except Exception as e:
            # High-availability Fallback: If appliances are down, we fail-safe to GATED
            return {"status": "GATED", "reason": f"Internal Appliance Error: {str(e)}"}

@app.post("/intercept")
async def intercept_api(request: Request, api_key: str = Depends(get_api_key)):
    """REST Ingress for External Federation Nodes."""
    try:
        payload = await request.json()
    except:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    result = await orchestrate_signal(payload)
    
    if result["status"] == "GATED":
        return JSONResponse(status_code=202, content=result)
    
    return result

@app.on_event("startup")
async def startup_event():
    """Launch the Hardware-Accelerated Synapse Watcher (Optane)."""
    optane_path = "C:/SubCortices/Mars-City-Stargazer/neural_synapses"
    
    # Simple wrapper to handle the async orchestrator from a sync thread
    def sync_gateway(payload):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(orchestrate_signal(payload))

    print(f"🚀 [GATEWAY] Starting Fast-Twitch Ear on {optane_path}...")
    watcher = SubcorticalWatcher(optane_path, gateway_callback=sync_gateway)
    
    w_thread = threading.Thread(target=watcher.run_polling_loop, daemon=True)
    w_thread.start()
    print("✨ [GATEWAY] Unified Sovereign Triad is ACTIVE.")

if __name__ == "__main__":
    print("TITANESS THALAMIC GATEWAY APPLIANCE v5.9 ONLINE")
    uvicorn.run(app, host="0.0.0.0", port=8000)
