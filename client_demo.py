from thalamic_sdk import ThalamicApplianceSDK
import json
import time

def run_production_demo():
    """
    Simulates a multi-agent system fleet communicating with the 
    Thalamic Gateway Appliance to solve quadratic noise.
    """
    # Initialize the SDK pointing to the local appliance
    sdk = ThalamicApplianceSDK(gateway_url="http://localhost:9998")
    
    print("="*60)
    print("🚀 TITANESS THALAMIC GATEWAY: PRODUCTION DEMO")
    print("="*60)
    
    # STEP 1: INITIAL IGNITION ( Jennifer-v2.0 )
    print("\n[STEP 1] Initiating Identity Injection (Awakening)...")
    ignition = sdk.awaken()
    if ignition.get("status") == "AWAKENED":
        print(f"✅ SYSTEM AWAKENED. Identity: {ignition.get('identity')}")
    else:
        print("❌ IGNITION FAILED. Is the Appliance running on Port 9998?")
        return

    # STEP 2: SIMULATE FLEET NOISE
    print("\n[STEP 2] Simulating MAS Fleet Ingress (Quadratic Noise)...")
    intents = [
        {"source": "AGENT_01", "intent": "scan-system", "salience": 0.95},
        {"source": "AGENT_02", "intent": "duplicate-request", "salience": 0.10},
        {"source": "AGENT_03", "intent": "ping-heartbeat", "salience": 0.05}
    ]
    
    for intent in intents:
        print(f"📤 Ingesting Signal from {intent['source']}...")
        msg_id = sdk.ingest(intent)
        print(f"   [Thalamus]: Message {msg_id} admitted for Sentience Gating.")
        time.sleep(0.5)

    # STEP 3: MONITOR METABOLIC TELEMETRY
    print("\n[STEP 3] Monitoring Metabolic Telemetry (Aura Protocol)...")
    telemetry = sdk.get_telemetry()
    chem = telemetry.get("chemical_state", {})
    
    print(f"📊 SYSTEM STATUS: {telemetry.get('system', {}).get('status')}")
    print(f"📊 METABOLIC LOAD: Cortisol: {chem.get('CORTISOL', 0.0):.2f} | Dopamine: {chem.get('DOPAMINE', 0.0):.2f}")
    
    print("\n" + "="*60)
    print("✅ DEMO COMPLETE: Quadratic Noise shunted to GCP Networking Substrate.")
    print("="*60)

if __name__ == "__main__":
    run_production_demo()
