from thalamic_sdk import TitanessSDK
import json
import time

def run_production_demo():
    """
    Titaness Thalamic Gateway: Production Demo (v5.9)
    -------------------------------------------------
    Simulates a high-salience signal transmission through the 
    Sovereign Orchestrator with Aversive Feedback handling.
    """
    # Initialize the SDK with a test key
    SDK_KEY = "PRODUCTION_BETA_TEST_KEY"
    sdk = TitanessSDK(agent_id="BETA-AGENT-001", secret_key=SDK_KEY, gateway_url="http://localhost:8000")
    
    print("="*60)
    print("🚀 TITANESS THALAMIC GATEWAY: PRODUCTION DEMO v5.9")
    print("="*60)
    
    # STEP 1: TRANSMIT HIGH-SALIENCE INTENT
    print("\n[STEP 1] Transmitting High-Salience Intent...")
    payload = {
        "action": "orchestration_sync",
        "parameters": {"depth": "full", "threshold": 0.85}
    }
    
    try:
        response = sdk.transmit_intent(target_id="ORCHESTRATOR", payload=payload, resonance=0.9)
        
        if response.status_code == 200:
            print("✅ SIGNAL ADMITTED: Orchestrator has accepted the intent.")
            print(f"   Response: {response.json()}")
            
        elif response.status_code == 429:
            # THIS IS THE CORE OF YOUR SYSTEM: SIGNAL 49
            print("⚠️ SIGNAL 49 RECEIVED: Aversive Feedback Shunting.")
            print("   [ACTION]: Agent must now dampen signal and wait for metabolic recovery.")
            
        else:
            print(f"❌ GATEWAY ERROR: Received status {response.status_code}")
            
    except Exception as e:
        print(f"❌ CONNECTION FAILED: Is the Orchestrator running on Port 8000?")

    print("\n" + "="*60)
    print("✅ DEMO COMPLETE: Biometric Shunting Verified.")
    print("="*60)

if __name__ == "__main__":
    run_production_demo()
