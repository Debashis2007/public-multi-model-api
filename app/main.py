# Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.
# Unauthorized copying, modification, or distribution is prohibited.
# https://github.com/Debashis2007

"""Public Multi-Model API — thin self-contained FastAPI POC."""

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from poc_core import MockLLM, TokenBucket, health_payload, AUTHOR_NAME, AUTHOR_FINGERPRINT, AUTHOR_GITHUB
from poc_core.safety import SafetyPlane
from poc_core.stores import InMemoryStore, MockVectorIndex

USE_CASE = "Public Multi-Model API"
app = FastAPI(title=USE_CASE)
llm = MockLLM()
store = InMemoryStore()
safety = SafetyPlane()

@app.get("/health")
def health():
    return health_payload(
        USE_CASE,
        {
            "author": AUTHOR_NAME,
            "author_github": AUTHOR_GITHUB,
            "fingerprint": AUTHOR_FINGERPRINT,
        },
    )

@app.get("/author")
def author():
    return {
        "author": AUTHOR_NAME,
        "github": AUTHOR_GITHUB,
        "fingerprint": AUTHOR_FINGERPRINT,
        "notice": "Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.",
    }


ALIASES = {"chat-latest": "chat-r2026.04.01", "chat-old": "chat-r2025.12.01"}
buckets: dict[str, TokenBucket] = {}
usage_log: list[dict] = []

class ChatIn(BaseModel):
    model: str = "chat-latest"
    prompt: str

@app.post("/v1/chat/completions")
async def completions(body: ChatIn, request: Request):
    key = request.headers.get("x-api-key", "anon")
    buckets.setdefault(key, TokenBucket(20, 2))
    if not buckets[key].allow():
        raise HTTPException(429, detail="rate limited")
    rev = ALIASES.get(body.model, body.model)
    text = await MockLLM(model=rev).complete(body.prompt, max_tokens=16)
    evt = {"key": key, "model": rev, "tokens": len(text.split())}
    usage_log.append(evt)
    return {"revision": rev, "text": text, "usage": evt}

@app.get("/v1/usage")
def usage():
    return {"events": usage_log}
