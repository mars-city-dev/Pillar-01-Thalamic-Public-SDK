from thalamic_sdk import ThalamicAgentSDK
import json
import time

def run_thalamic_demo():
    print("="*60)
    print("🧠 TITANESS: THALAMIC GATEWAY APPLIANCE - LANDMARK DEMO")
    print("="*60)
    
    # 1. Initialize the Agent SDK
    # Represents a 'Sentient Agent' in the Titaness Federation.
    sdk = ThalamicAgentSDK(
        gateway_url="http://localhost:8000",
        agent_id="FEDERATION_AGENT_01",
        secret_key="sk_titaness_secret_key"
    )
    
    # 2. Transmit a High-Salience Intent
    print("\n[STEP 1] Transmitting High-Salience Intent...")
    success = sdk.transmit_intent(
        target_id="ORCHESTRATOR",
        payload={"action": "re-index-all"},
        resonance=0.9,
        urgency=1.0
    )
    
    if success:
        print("✅ SUCCESS: Signal Admitted via MHC-Class I Identity.")
    else:
        print("❌ FAILED: Signal Gated or Identity Denied.")

    # 3. Simulate a Spoofing Attempt (The "Man-in-the-Middle" failure)
    print("\n[STEP 2] Simulating Unauthorized 'Spoof' Attempt...")
    malicious_sdk = ThalamicAgentSDK(
        gateway_url="http://localhost:8000",
        agent_id="FEDERATION_AGENT_01", 
        secret_key="HACKED_KEY" # Signature verification will fail
    )
    
    spoof_success = malicious_sdk.transmit_intent(
        target_id="DATABASE",
        payload={"action": "drop_tables"}
    )
    
    if not spoof_success:
        print("✅ SECURITY WIN: Unauthorized signal was severed at the Gateway.")

    print("\n" + "="*60)
    print("✨ MISSION COMPLETE: QUADRATIC NOISE SHUNTED | IDENTITY SECURED")
    print("="*60)

if __name__ == "__main__":
    run_thalamic_demo()
