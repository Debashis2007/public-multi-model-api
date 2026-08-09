# Design: Public Multi-Model API

**Project:** `public-multi-model-api`  
**Parent system design:** `09-multi-model-routing-api-platform.md`

## 1. What this POC demonstrates

Public chat completions with alias→revision map, per-key quotas, and usage log.

## 2. Architecture (POC)

```text
x-api-key → quota → alias resolve → MockLLM(revision) → usage event
```

## 3. Patterns used (and why)

| Pattern | Why used | Where in code |
|---------|----------|---------------|
| Alias vs pin map | `latest` is mutable; revisions are immutable. | `ALIASES` dict. |
| Per-key rate limit | Abuse and fairness. | `TokenBucket`. |
| Usage event log | Billing reconcile foundation. | `/v1/usage`. |

## 4. Key endpoints

`GET /health`, `POST /v1/chat/completions`, `GET /v1/usage`

## 5. Tradeoffs / POC limits

No durable billing warehouse — list in memory.

## 6. How to run

See the **Run (self-contained POC)** section in [`../README.md`](../README.md).

This folder is self-contained and can be published as its own GitHub repository.

## 7. Design walkthrough video

Narrated with **ElevenLabs Debpro voice** and Debpro still image (via [GitaProject](/Users/deb/Development/GenAI/GitaProject)):

- Video: [`video/design-overview.mp4`](./video/design-overview.mp4)
- Script: [`video/narration.txt`](./video/narration.txt)

