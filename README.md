# WhatIF Factory — Architecture Showcase

**Multi-Model AI Orchestration System**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-junebay-blue?style=flat&logo=linkedin)](https://linkedin.com/in/junebay)

---

## Overview

Multi-model AI orchestration system that integrates multiple external AI APIs (GPT-4o, Gemini, ElevenLabs, Flux, etc.) into a single automated pipeline. Designed for operational resilience and cost control — not content volume.

Currently operating across **2 YouTube channels**.

### At a Glance

| Item | Detail |
|------|--------|
| **AI Models** | GPT-4o, Gemini, ElevenLabs, Flux |
| **Pipeline** | Stateful, save/load/rollback |
| **Error Handling** | Cost-aware error classification |
| **Recovery** | Exponential backoff auto-recovery |
| **Design** | HITL (Human-in-the-Loop) |
| **Status** | Production, 2 YouTube channels |

---

## Architecture

```
┌─────────────────────────────────────────────┐
│         Human-in-the-Loop (HITL)            │
│  Topic Input → Quality Review → Approve     │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         Stateful Pipeline Engine            │
│  - Save/Load/Rollback at any stage          │
│  - Cost-aware error classification          │
│  - Exponential backoff recovery             │
├─────────────────────────────────────────────┤
│  GPT-4o    Gemini    ElevenLabs    Flux     │
│  (Script)  (Alt)     (Voice)       (Image)  │
├─────────────────────────────────────────────┤
│         FFmpeg Post-Processing              │
│  - SRT-driven timing                        │
│  - Resolution unification                   │
└─────────────────────────────────────────────┘
```

---

## Key Technical Decisions

### Stateful Pipeline
- Save/load/rollback at any production stage
- No full restart needed — edit and resume from any checkpoint
- Ensures workflow continuity across long production runs

### Cost-Aware Error Classification
- Errors classified into recoverable vs. unrecoverable
- Prevents wasteful API retries on permanent failures (e.g., content policy, invalid prompt)
- Protects operational budget from runaway API costs

### Exponential Backoff Recovery
- Automatic retry with increasing delays for transient failures
- Handles API rate limits and server errors gracefully
- Zero manual intervention for common failure modes

### HITL (Human-in-the-Loop) Design
- Not full automation — structured for human intervention at critical decision points
- Topic selection, quality review, and final approval require human judgment
- Balances automation efficiency with output quality

---

## Tech Stack

- **Python** — pipeline orchestration
- **Streamlit** — operator interface
- **GPT-4o / Gemini** — content generation
- **ElevenLabs** — voice synthesis
- **Flux** — image generation
- **FFmpeg** — video processing, SRT timing
- **n8n** — workflow automation

---

## Related

- **Profile**: [github.com/JuneBay](https://github.com/JuneBay)
- **LinkedIn**: [linkedin.com/in/junebay](https://linkedin.com/in/junebay)
- **Contact**: Via LinkedIn only
