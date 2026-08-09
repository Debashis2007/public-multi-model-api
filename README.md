# Use Case: Public Multi-Model API

**Author fingerprint:** `DBHATT-Debashis2007-SystemDesignPOC-2026` — Debashis Bhattacharjee ([@Debashis2007](https://github.com/Debashis2007))

**YouTube walkthrough:** [Public Multi Model Api — System Design #Shorts](https://youtu.be/CaUse052go8)

**Design doc:** [docs/DESIGN.md](./docs/DESIGN.md) — architecture, patterns, and why.


**Parent system design:** [09 — Multi-Model Routing / API Platform](https://github.com/Debashis2007/public-multi-model-api/blob/main/09-multi-model-routing-api-platform.md)  
**Also references:** [01 — Inference](https://github.com/Debashis2007/public-multi-model-api/blob/main/01-llm-inference-serving.md)

## Users & problem

External developers call a public API across many models with keys, docs, SDKs, and billing. Reliability and metering accuracy are the product.

## Requirements & SLOs

| Requirement | Target |
|-------------|--------|
| Auth | API keys / OAuth |
| Models | Aliases + pins |
| Quotas | RPM/TPM/$ |
| Billing | Idempotent usage → invoice |

## Design (from parent)

```
Edge → gateway → quota → router → fleets ([01](https://github.com/Debashis2007/public-multi-model-api/blob/main/01-llm-inference-serving.md))
  → metering → developer console
```

Reuse full **09** control plane; fleets from **01**; streaming from [02](https://github.com/Debashis2007/public-multi-model-api/blob/main/02-streaming-token-delivery.md).

## Specializations

| Concern | Public API choice |
|---------|-------------------|
| DX | Status page, error taxonomy, SDKs |
| Abuse | Carding/spend attacks → fast kill |
| Deprecation | Long pin windows |
| Safety | [06](https://github.com/Debashis2007/public-multi-model-api/blob/main/06-safety-moderation-pipeline.md) on all routes |

## Failure modes

- Undercounted usage → reconcile inference completions daily.
- Noisy neighbor → reserved pools for paid tiers.
- Silent model swap → pins + changelog for aliases.




## Design walkthrough (opens on GitHub)

> **Watch on YouTube:** [Public Multi Model Api — System Design #Shorts](https://youtu.be/CaUse052go8)


![Design overview](docs/video/design-overview.gif)

Full narrated video (download): [docs/video/design-overview.mp4](docs/video/design-overview.mp4)

## Run (self-contained POC)

This folder is a **standalone** project (safe to split into its own GitHub repo).

```bash
cd public-multi-model-api
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
PYTHONPATH=. python -m uvicorn app.main:app --reload --port 8000
```

```bash
curl -s http://127.0.0.1:8000/health | jq
```

curl -s -X POST http://127.0.0.1:8000/v1/chat/completions -H 'x-api-key: sk-demo' -H 'Content-Type: application/json' -d '{"model":"chat-latest","prompt":"hi"}' | jq

---

**Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.**  
Unauthorized copying or redistribution of this material is prohibited.  
GitHub: [Debashis2007](https://github.com/Debashis2007)

