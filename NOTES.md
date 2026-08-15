## Groq Model Migration (llama-3.1-8b-instant → gpt-oss-20b)

**Problem:** Groq announced deprecation of `llama-3.1-8b-instant` effective August 16, 2026 — production endpoints (`/ask`, `/agent-ask`) would start failing after that date.

**Why this solution:** Groq's recommended replacement is `openai/gpt-oss-20b`, served on the same API endpoint — no SDK, auth, or base URL changes needed, making it a low-risk swap under a tight (2-day) deadline.

**Alternatives considered:** Switching to a different provider entirely (OpenAI, Anthropic) was rejected — too much rework (auth, SDK, pricing changes) for a deadline this tight, with no functional benefit.

**Implementation:**
- Found hardcoded model references in `agent.py` and `app.py` via `findstr`
- Replaced `model="llama-3.1-8b-instant"` with `model="openai/gpt-oss-20b"` in both files
- Tested `/ask` (simple RAG) and `/agent-ask` (agentic LangGraph loop) locally to confirm tool-calling and loop-termination logic still worked correctly with the new model
- Verified response format and source citations remained consistent

**Trade-offs:** `gpt-oss-20b` is a reasoning model — behavior and latency can differ from Llama. Existing retrieval-accuracy issue (wrong fee/duration info) was confirmed to pre-date this migration, so it's tracked separately, not conflated with the model swap.

**Interview questions:**
- How do you handle a production dependency deprecation with a hard deadline?
- What's your process for verifying a model swap doesn't silently break downstream logic (e.g. agentic tool-calling)?