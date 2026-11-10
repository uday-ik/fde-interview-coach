# Guide: The Agentic System-Design Round

Design an AI system under enterprise constraints, and defend reliability, cost,
and latency.

**A reliable pattern to reach for**
- **Ground it** — retrieval over the customer's real data; cite sources.
- **Constrain it** — schemas/tools instead of free text; validate outputs.
- **Evaluate it** — an eval set + LLM-as-judge as a deploy gate, not vibes.
- **Guardrail it** — PII handling, cost controls (caching, model routing),
  human-in-the-loop where the cost of error is high.

**Defend:** how you measure accuracy, what you do when the model is unsure, and
how cost scales with usage.
