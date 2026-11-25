# HireSense AI

An AI-powered recruitment intelligence platform. Recruiters upload resumes (PDF/DOCX, single or bulk). HireSense extracts candidate profiles, enables semantic search, matches candidates to job descriptions with **explainable** scores, answers questions about resumes using **RAG with citations**, compares candidates and shows recruitment analytics.

> **Decision support only.** HireSense AI never makes autonomous hiring decisions. Every score shows its components, and every answer cites its sources. Development uses **synthetic resume data only**.

## Status

**Phase 0 — project instruction system and documentation.** No application code exists yet. See [docs/PROJECT_STATE.md](docs/PROJECT_STATE.md) for the live status.

## Tech stack

| Area | Technologies |
|---|---|
| Backend | Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy 2, Alembic, PostgreSQL, JWT, Pytest |
| AI / RAG | Sentence Transformers, pgvector, Gemini API |
| Documents | PyMuPDF, python-docx |
| Background jobs | Celery, Redis |
| Frontend | Next.js, TypeScript, Tailwind CSS |
| Infrastructure | Docker, Docker Compose, GitHub Actions, AWS or VPS |

Each technology is introduced only in the phase that needs it. The rationale is in [docs/TECH_DECISIONS.md](docs/TECH_DECISIONS.md).

## Roadmap (about 8 weeks, about 2 hours per day)

| Phase | Focus |
|---|---|
| 0 | Claude Code instruction system and docs |
| 1 | Python fundamentals and environment setup |
| 2 | FastAPI fundamentals |
| 3 | PostgreSQL, SQLAlchemy, Alembic, JWT auth |
| 4 | Resume processing and background tasks |
| 5 | Embeddings, pgvector, semantic search, RAG |
| 6 | Hybrid search, reranking, candidate matching |
| 7 | Next.js integration and testing |
| 8 | Docker, CI/CD, deployment |

## Documentation

| File | Purpose |
|---|---|
| [CLAUDE.md](CLAUDE.md) | Rules for every Claude Code session |
| [docs/PROJECT_STATE.md](docs/PROJECT_STATE.md) | Live status, phase deliverables, next task, session history |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design, module layout, RAG data flows, deployment |
| [docs/DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md) | Proposed and implemented tables, relationships, indexes |
| [docs/API_SPECIFICATION.md](docs/API_SPECIFICATION.md) | Planned and implemented endpoints |
| [docs/TECH_DECISIONS.md](docs/TECH_DECISIONS.md) | Architecture decision log |
| [docs/LEARNING_LOG.md](docs/LEARNING_LOG.md) | Evidence-based learning progress |

## Working with Claude Code

Open this folder (`Hiresense_ai/`) as the project root, so that `CLAUDE.md` and `.claude/skills/` load. Start each session with:

```
Resume HireSense AI using the session-handoff skill.
```

## Getting started

Setup instructions will be added in Phase 1, once the Python environment is configured.
