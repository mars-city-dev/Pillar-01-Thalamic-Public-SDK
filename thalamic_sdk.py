import hmac
import hashlib
import json
import time
import httpx
from typing import Dict, Any, Optional

class ThalamicAgentSDK:
    """
    Titaness Thalamic Agent SDK (v4.3.0)
    ====================================
    Client-side SDK for Agents (AutoGPT, CrewAI, etc.).
    Enforces MHC-Class I Cryptographic Identity and Salience Gating.
    """
    
    def __init__(self, 
                 gateway_url: str = "http://localhost:8000", 
                 agent_id: str = "AGENT_01", 
                 secret_key: str = "titaness_sovereign_2026"):
        """
        Initialize the SDK with MHC-Class I Identity.
        """
        self.gateway_url = gateway_url.rstrip("/")
        self.agent_id = agent_id
        self.secret_key = secret_key
        self.client = httpx.Client(timeout=10.0)

    def _sign_packet(self, payload: dict) -> str:
        """Calculates the MHC-Class I HMAC-SHA256 signature."""
        # Use sort_keys to ensure consistent JSON string representation for hashing
        body_to_sign = json.dumps(payload, sort_keys=True)
        return hmac.new(
            self.secret_key.encode(),
            body_to_sign.encode(),
            hashlib.sha256
        ).hexdigest()

    def transmit_intent(self, 
                        target_id: str, 
                        payload: Dict[str, Any], 
                        resonance: float = 0.5, 
                        urgency: float = 0.5) -> Dict[str, Any]:
        """
        Transmits a signal to another agent via the Thalamus.
        Includes MHC Signing and Salience Metadata.
        """
        # Construct the unified packet (Isomorphic Signaling Standard)
        packet = {
            "sender_id": self.agent_id,
            "target_id": target_id,
            "resonance": resonance,
            "urgency": urgency,
            "payload": payload
        }
        
        # Calculate the MHC-Class I Signature
        signature = self._sign_packet(packet)
        
        headers = {
            "X-API-Key": "sk_live_enterprise_123",
            "X-MHC-Signature": signature,
            "Content-Type": "application/json"
        }
        
        try:
            # All traffic hits the /intercept endpoint for gating
            response = self.client.post(f"{self.gateway_url}/intercept", json=packet, headers=headers)
            
            if response.status_code in [200, 202]:
                return response.json()
            elif response.status_code == 429:
                msg = response.json().get("detail", "Please Upgrade your License.")
                return {
                    "status": "METABOLIC_SATURATION", 
                    "code": 429, 
                    "message": msg,
                    "action": "BACKOFF_REQUIRED"
                }
            else:
                return {"status": "ERROR", "code": response.status_code, "detail": response.text}
                
        except Exception as e:
            return {"status": "ERROR", "detail": f"CONNECTION_ERROR: {e}"}

    def get_telemetry(self) -> Dict[str, Any]:
        """Fetch the current metabolic state from the Gateway."""
        try:
            response = self.client.get(f"{self.gateway_url}/telemetry")
            return response.json()
        except Exception as e:
            return {"error": str(e)}

# Alias for backward compatibility
ThalamicApplianceSDK = ThalamicAgentSDK

if __name__ == "__main__":
    # --- INTERNAL SDK TEST SEQUENCE ---
    sdk = ThalamicAgentSDK()
    print("--- 🧠 TITANESS: AGENT SDK v4.3.0 LIVE ---")
    
    res = sdk.transmit_intent(
        target_id="CORTEX_01",
        payload={"task": "heartbeat-test"},
        resonance=1.0
    )
    print(f"      Result: {json.dumps(res, indent=2)}")
