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
import hmac
import hashlib
from fastapi import FastAPI, Request, HTTPException, Security, Depends, Header
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import JSONResponse
import uvicorn

from spline_watcher import SplineWatcher

# --- MHC-Class I Identity Registry (Mocked for Demo) ---
SIGNET_REGISTRY = {
    "AGENT_01": "sk_titaness_secret_key",
    "AGENT_02": "sk_titaness_secondary_key",
    "FEDERATION_AGENT_01": "sk_titaness_secret_key",
    "SUBSTRATE_SENTINEL": "sk_sentinel_internal_key"
}

def verify_mhc_signature(
    payload: Dict[str, Any],
    signet_id: str = Header(..., alias="X-MHC-Signet"),
    timestamp: str = Header(..., alias="X-MHC-Timestamp"),
    signature: str = Header(..., alias="X-MHC-Signature")
):
    """
    Verifies the MHC-Class I Cryptographic Identity of the signal.
    """
    if signet_id not in SIGNET_REGISTRY:
        raise HTTPException(status_code=403, detail="MHC Identity Unknown: Access Denied")
    
    secret = SIGNET_REGISTRY[signet_id]
    
    # 1. Prevent Replay Attacks (10-second window)
    if abs(time.time() - int(timestamp)) > 10:
        raise HTTPException(status_code=401, detail="Signet Expired: Potential Replay Attack Detected")

    # 2. Re-calculate Signature
    message = f"{signet_id}:{timestamp}:{json.dumps(payload, sort_keys=True)}"
    expected_sig = hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(expected_sig, signature):
        raise HTTPException(status_code=403, detail="MHC Signature Mismatch: Signal Spoofing Detected")
    
    return signet_id

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

async def orchestrate_signal(packet: Dict[str, Any]) -> Dict[str, Any]:
    """
    Coordinates the 3-stage appliance pipeline.
    Extracts salience metadata from the SDK packet.
    """
    async with httpx.AsyncClient() as client:
        try:
            # 1. TRN EVALUATION (Gating & Aversion)
            # The TRN uses resonance/urgency for the Z-Score calculation
            trn_resp = await client.post(TRN_URL, json=packet, timeout=2.0)
            decision = trn_resp.json()
            
            if decision["status"] == "GATED":
                return decision # Returns the Signal 49 Aversive Feedback
            
            # 2. METABOLIC PULSE (Dopamine Spike on Admission)
            # Higher salience signals create a stronger dopamine response.
            intensity = packet.get("resonance", 0.5) * packet.get("urgency", 0.5)
            
            # Map "DOPAMINE" to ID 21 and pulse the metabolism
            await client.post(f"{VNEURO_URL}/peptide/21/pulse", params={"intensity": intensity})
            
            return {
                "status": "ADMITTED",
                "reason": decision["reason"],
                "mhc_verification": "SUCCESS"
            }
        except Exception as e:
            # High-availability Fallback: If appliances are down, we fail-safe to GATED
            return {"status": "GATED", "reason": f"Internal Appliance Error: {str(e)}"}

@app.post("/intercept")
async def intercept_api(
    request: Request, 
    api_key: str = Depends(get_api_key)
):
    """REST Ingress for External Federation Nodes."""
    try:
        payload = await request.json()
    except:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    # MHC-Class I Verification
    signet_id = verify_mhc_signature(
        payload, 
        request.headers.get("X-MHC-Signet"),
        request.headers.get("X-MHC-Timestamp"),
        request.headers.get("X-MHC-Signature")
    )
    
    result = await orchestrate_signal(payload)
    result["mhc_verification"] = f"VERIFIED: {signet_id}"
    
    if result["status"] == "GATED":
        return JSONResponse(status_code=202, content=result)
    
    return result

@app.on_event("startup")
async def startup_event():
    """Launch the Hardware-Accelerated Spline Watcher (Fast-Twitch Ear)."""
    optane_path = os.getenv("OPTANE_PATH", "C:/SubCortices/Mars-City-Stargazer/neural_synapses")
    
    # Simple wrapper to handle the async orchestrator from a sync thread
    def sync_gateway(payload):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(orchestrate_signal(payload))

    print(f"🚀 [GATEWAY] Starting Spline Watcher (Fast-Twitch Ear) on {optane_path}...")
    watcher = SplineWatcher(cortex_id="VNN:STARGAZER", neural_synapses_path=optane_path)
    
    # Note: In a real implementation, we would bridge the watcher.watch() loop 
    # but for the Public SDK, we provide the module as a reference.
    w_thread = threading.Thread(target=watcher.watch, daemon=True)
    w_thread.start()
    print("✨ [GATEWAY] Unified Sovereign Triad is ACTIVE.")

if __name__ == "__main__":
    print("TITANESS THALAMIC GATEWAY APPLIANCE v5.9 ONLINE")
    uvicorn.run(app, host="0.0.0.0", port=8000)
