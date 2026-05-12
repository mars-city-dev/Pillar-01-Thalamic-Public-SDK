import httpx
import json
import uuid
from typing import Dict, Any, Optional

class ThalamicApplianceSDK:
    """
    Titaness Thalamic Appliance SDK (v4.0.0)
    ========================================
    Official bridge for the Standalone Software Appliance.
    Solves the quadratic noise issue via TRN Gating and 
    Metabolic Load Balancing.
    """
    
    def __init__(self, gateway_url: str = "http://localhost:9998"):
        """
        Initialize the SDK.
        
        Args:
            gateway_url: The URL of the Thalamic Appliance (Default: Port 9998)
        """
        self.gateway_url = gateway_url.rstrip("/")
        self.client = httpx.Client(timeout=10.0)

    def ingest(self, payload: Dict[str, Any]) -> str:
        """
        Ingest an intent into the Sentience Gating engine.
        
        Returns:
            The message_id assigned by the Thalamus.
        """
        try:
            response = self.client.post(f"{self.gateway_url}/ingest", json=payload)
            if response.status_code in [200, 202]:
                data = response.json()
                return data.get("message_id")
            else:
                return f"ERROR: {response.status_code}"
        except Exception as e:
            return f"CONNECTION_ERROR: {e}"

    def evaluate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Directly evaluate a signal's salience without ingesting.
        Returns the TRN Admittance decision.
        """
        try:
            response = self.client.post(f"{self.gateway_url}/evaluate", json=payload)
            return response.json()
        except Exception as e:
            return {"admitted": False, "reason": f"SDK_ERROR: {e}"}

    def get_telemetry(self) -> Dict[str, Any]:
        """
        Fetch the current metabolic state (Cortisol/Dopamine) 
        and traffic engams.
        """
        try:
            response = self.client.get(f"{self.gateway_url}/telemetry")
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def awaken(self) -> Dict[str, Any]:
        """
        Trigger the Identity Injection Sequence (Jennifer-v2.0).
        Transitions the appliance from COMA_STATE to LIVING.
        """
        try:
            response = self.client.post(f"{self.gateway_url}/awaken")
            return response.json()
        except Exception as e:
            return {"status": "FAILED", "error": str(e)}

if __name__ == "__main__":
    # --- REAL TEST SEQUENCE FOR THE APPLIANCE ---
    sdk = ThalamicApplianceSDK()
    
    print("--- 🧠 TITANESS: APPLIANCE SDK TEST ---")
    
    # 1. Awaken the system
    print("[1/3] Triggering Awakening Sequence...")
    wake_res = sdk.awaken()
    print(f"      Status: {wake_res.get('status')} | Identity: {wake_res.get('identity')}")
    
    # 2. Ingest a signal (Quadratic Noise Shunting)
    print("\n[2/3] Ingesting intent for Sentience Gating...")
    msg_id = sdk.ingest({"action": "re-index-all", "source": "MAS_FLEET_NODE_01"})
    print(f"      Message ID: {msg_id}")
    
    # 3. Check Telemetry (Hormonal levels)
    print("\n[3/3] Fetching Metabolic Telemetry...")
    telemetry = sdk.get_telemetry()
    print(f"      System Status: {telemetry.get('system', {}).get('status')}")
    print(f"      Chemical State: {json.dumps(telemetry.get('chemical_state'), indent=2)}")
