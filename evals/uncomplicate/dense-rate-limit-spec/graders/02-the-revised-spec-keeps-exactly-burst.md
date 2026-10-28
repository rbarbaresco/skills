---
type: llm
focus: trace
weight: 1
---

The revised spec keeps exactly: burst of 20 tokens; refill of 100 tokens per minute; one token per request; 429 with a Retry-After header in seconds; limits are per key, not per IP; internal keys are exempt; refill is continuous, so 12 idle seconds restores 20 tokens
