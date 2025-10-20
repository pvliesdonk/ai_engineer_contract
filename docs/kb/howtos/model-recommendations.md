---
doc_type: kb_howto
doc_version: 2025-10-20.r2
title: AI Model Recommendation Playbook
---

# AI Model Recommendation Playbook

Document AI assistance plans using shared provider families, task routes, and manifest metadata. Use these examples as a baseline and tailor them to your organization’s approved model catalog.

## Provider Families

Use this YAML block to describe the preferred provider families during planning. Reference it from design docs and cross-link in the manifest.

```yaml
ai_assist:
  providers:
    openai:
      primary: gpt-5
      thinking: gpt-5-thinking
      fast: o4-mini
      long_context: gpt-4.1
    google:
      primary: gemini-2.5-flash
      thinking: gemini-2.5-pro
      fast: gemini-2.5-flash-lite
      long_context: gemini-2.5-pro
    ollama:
      primary: llama3.1:8b-instruct-q4_K_M
      thinking: deepseek-r1:7b
      fast: mistral:7b-instruct
      long_context: mistral:7b-instruct
  notes: >
    Document families in planning; pin exact SKUs only in deployable config.
    For local models on 8 GB GPUs, prefer Q4_K_M quantizations for stability.
```

- **OpenAI** — gpt-5 as the default “smart” model, gpt-5-thinking for deep reasoning, o4-mini for cheap/fast scaffolds, and gpt-4.1 for 1M-token context.
- **Google AI Studio** — gemini-2.5-flash (cost-effective generalist), gemini-2.5-pro for thinking/long context, and gemini-2.5-flash-lite for high throughput.
- **Ollama (local)** — tuned for an RTX 4060 (8 GB) using Q4_K_M weights: llama3.1:8b-instruct (generalist), deepseek-r1:7b (reasoning-style), and mistral:7b-instruct for fast scaffolds/32k context.

## Task-Based Routes

Route requests to providers per task type. Teams may add fields (for example, latency budgets) as needed.

```yaml
routes:
  - when: { task: "scm_c_advise" }
    openai: gpt-5
    google: gemini-2.5-flash
    ollama: llama3.1:8b-instruct-q4_K_M
    notes: "Low-latency, high-reliability responses for checklists and summaries."

  - when: { task: "policy_edit", risk: "high" }
    openai: gpt-5-thinking
    google: gemini-2.5-pro
    ollama: deepseek-r1:7b
    set: { reasoning_required: true }
    notes: "Escalate to reasoning variants for nuanced contract or policy edits."

  - when: { task: "bulk_scaffold" }
    openai: o4-mini
    google: gemini-2.5-flash-lite
    ollama: mistral:7b-instruct
    notes: "Optimize for throughput when generating many small artifacts."

  - when: { task: "long_context" }
    openai: gpt-4.1
    google: gemini-2.5-pro
    ollama: mistral:7b-instruct
    notes: "GPT-4.1 and Gemini 2.5 Pro handle ~1M tokens; local models rely on RAG for >32k."

  - when: { task: "bulk_narration" }
    openai: gpt-5
    google: gemini-2.5-flash
    ollama: gemma2:9b-instruct-q4_K_M
    notes: "Gemini Flash balances style and cost; Gemma 2 9B is a strong local narrator."

  - when: { task: "bulk_programming" }
    openai: gpt-5
    google: gemini-2.5-pro
    ollama: llama3.1:8b-instruct-q4_K_M
    notes: "Prefer stable 8–9B-class locals unless you have >12 GB VRAM; consider DeepSeek Coder Lite if available."
```

### Local route notes for 8 GB GPUs

| Lane              | Suggested route                           | Approx VRAM | Context |
|-------------------|-------------------------------------------|------------:|--------:|
| Bulk narration    | gemma2:9b-instruct-q4_K_M                 |     ~7–8 GB |   8–16k |
| Bulk programming  | llama3.1:8b-instruct-q4_K_M               |     ~6–7 GB |   8–16k |
| Reasoning (light) | deepseek-r1:7b                            |     ~6–7 GB |     8k |
| Throughput        | mistral:7b-instruct                       |     ~5–6 GB |    32k |

## Manifest Example

Extend ai/manifest.json so automation can detect the approved providers and routes.

```json
{
  "ai_assist": {
    "providers": {
      "openai": {
        "primary": "gpt-5",
        "thinking": "gpt-5-thinking",
        "fast": "o4-mini",
        "long_context": "gpt-4.1"
      },
      "google": {
        "primary": "gemini-2.5-flash",
        "thinking": "gemini-2.5-pro",
        "fast": "gemini-2.5-flash-lite",
        "long_context": "gemini-2.5-pro"
      },
      "ollama": {
        "primary": "llama3.1:8b-instruct-q4_K_M",
        "thinking": "deepseek-r1:7b",
        "fast": "mistral:7b-instruct",
        "long_context": "mistral:7b-instruct"
      }
    },
    "routes": [
      { "when": { "task": "scm_c_advise" },     "openai": "gpt-5", "google": "gemini-2.5-flash",      "ollama": "llama3.1:8b-instruct-q4_K_M" },
      { "when": { "task": "policy_edit", "risk": "high" }, "openai": "gpt-5-thinking", "google": "gemini-2.5-pro", "ollama": "deepseek-r1:7b", "set": { "reasoning_required": true } },
      { "when": { "task": "bulk_scaffold" },    "openai": "o4-mini", "google": "gemini-2.5-flash-lite", "ollama": "mistral:7b-instruct" },
      { "when": { "task": "long_context" },     "openai": "gpt-4.1", "google": "gemini-2.5-pro",       "ollama": "mistral:7b-instruct" },
      { "when": { "task": "bulk_narration" },   "openai": "gpt-5", "google": "gemini-2.5-flash",       "ollama": "gemma2:9b-instruct-q4_K_M" },
      { "when": { "task": "bulk_programming" }, "openai": "gpt-5", "google": "gemini-2.5-pro",        "ollama": "llama3.1:8b-instruct-q4_K_M" }
    ],
    "review_on_release": true
  }
}
```

## Maintenance Tips

- Review provider lists each release cycle; replace models when new GA versions ship or when org policy changes.
- Document hardware assumptions for local deployments (for example, 8 GB VRAM for Q4_K_M quantizations).
- Encourage teams to add telemetry (latency, cost, tool usage) in project-specific docs so recommendations stay data informed.
