# 🧬 Titaness Thalamic Agent SDK

## Overview
The Titaness Thalamic Agent SDK is a production-grade client library for agents (AutoGPT, CrewAI, etc.) to communicate via the **Thalamic Gateway Appliance**.

### 🧠 Core Features
- **MHC-Class I Signatures**: Every packet is cryptographically signed for identity verification.
- **Signal 49 Handling**: Built-in local back-off and dampening for aversive feedback signals.
- **Asynchronous Ingress**: High-performance signal transmission via the `/intercept` endpoint.

## 🚀 Quick Start

```python
from thalamic_sdk import TitanessSDK

# Initialize the SDK
sdk = TitanessSDK(agent_id="my-agent-001", gateway_url="http://localhost:8000")

# Transmit an intent
response = sdk.transmit_intent(
    target_id="orchestrator",
    payload={"action": "awaken", "parameters": {"level": 1.0}}
)

if response.status_code == 429:
    print("Signal 49 received: Dampening signal localy.")
```

## 🛡️ Security
This SDK enforces the **Titaness Identity Protocol**. Ensure your `X-API-KEY` is configured in your environment before initiating synapses.

---
*Production Ready: v5.9*
