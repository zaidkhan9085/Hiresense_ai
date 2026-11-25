# TECH_DECISIONS — HireSense AI

> Architectural decision log. **Never silently edit or delete a decision.** To change one, add a new entry and mark the old one `Superseded by TD-xxx`.
> Status values: **Accepted** (agreed and in force) · **Proposed** (Claude's recommendation, needs the developer's confirmation) · **Open** (to decide at the stated phase) · **Superseded**.
> A proposed change must include the reason, the alternatives, the trade-offs and the cost impact (₹ where relevant).

## Summary

| ID | Decision | Status | Phase |
|---|---|---|---|
| TD-001 | Python 3.12+ with FastAPI | Accepted | 1–2 |
| TD-002 | Pydantic v2 for validation and settings | Accepted | 2 |
| TD-003 | PostgreSQL + SQLAlchemy 2 + Alembic | Accepted | 3 |
| TD-004 | JWT (access + refresh) with RBAC | Accepted | 3 |
| TD-005 | pgvector instead of a dedicated vector DB | Accepted | 5 |
| TD-006 | Sentence Transformers for local embeddings | Accepted | 5 |
| TD-007 | Embedding model `all-MiniLM-L6-v2` (384-d) | Proposed | 5 |
| TD-008 | Direct RAG implementation; no LangChain/LlamaIndex initially | Accepted | 5 |
| TD-009 | Gemini API as the initial LLM, behind `LLMProvider` | Accepted | 5 |
| TD-010 | PyMuPDF + python-docx for extraction | Accepted (licence noted) | 4 |
| TD-011 | Celery + Redis for background processing | Accepted | 4 |
| TD-012 | Next.js + TypeScript + Tailwind frontend | Accepted | 7 |
| TD-013 | Docker, Docker Compose, GitHub Actions | Accepted | 8 |
| TD-014 | Monorepo with a feature-module backend layout | Proposed | 2 |
| TD-015 | uv for Python install, venv and dependencies | Accepted | 1 |
| TD-016 | Linter/formatter | Open | 1 |
| TD-017 | Local PostgreSQL: Homebrew vs Docker | Open | 3 |
| TD-018 | SQLAlchemy sync vs async driver | Open | 3 |
| TD-019 | Hosting: AWS vs VPS | Open | 8 |
| TD-020 | File storage: local disk vs S3-compatible | Open | 4 / 8 |
| TD-021 | Human-in-the-loop, explainable scoring; synthetic data only | Accepted | all |

---

## Accepted

### TD-001 — Python 3.12+ with FastAPI
- **Reason:** The target roles need it. FastAPI offers type-hint–driven validation, automatic OpenAPI docs, async support and a gentle path from Express.
- **Alternatives:** Django + DRF (batteries included, heavier, less async-native); Flask (minimal, manual validation); staying on Node (does not meet the learning goal).
- **Trade-offs:** Fewer built-ins than Django (auth and admin are built by hand), which is valuable for learning.
- **Status:** Accepted.

### TD-002 — Pydantic v2
- **Reason:** It is FastAPI's native validation layer. v2 is Rust-backed and fast; `pydantic-settings` handles configuration.
- **Alternatives:** dataclasses plus manual validation; marshmallow.
- **Trade-offs:** Many tutorials still show v1 syntax, so stay alert to that.
- **Status:** Accepted.

### TD-003 — PostgreSQL + SQLAlchemy 2 + Alembic
- **Reason:** The developer already knows PostgreSQL. SQLAlchemy is the industry-standard Python ORM, and Alembic gives versioned migrations. Postgres also hosts pgvector (TD-005).
- **Alternatives:** SQLModel (simpler, less mature, hides SQLAlchemy concepts); Tortoise ORM; raw SQL with asyncpg.
- **Trade-offs:** SQLAlchemy has a steeper learning curve, but it is the skill interviewers expect.
- **Status:** Accepted.

### TD-004 — JWT (access + refresh) with RBAC
- **Reason:** Stateless API auth that suits a separate Next.js frontend. It is common in interviews.
- **Alternatives:** server sessions with cookies; an external IdP (Auth0, Cognito, Clerk).
- **Trade-offs:** Revocation is harder (needs short expiry or a denylist). The password-hashing library is chosen in Phase 3.
- **Status:** Accepted.

### TD-005 — pgvector instead of a dedicated vector DB
- **Reason:** One database to run, SQL joins between vectors and metadata, transactions, and no extra cost. It is ample for thousands to low millions of chunks.
- **Alternatives:** Qdrant, Weaviate, Pinecone (managed, paid), Chroma, FAISS (a library, not a DB).
- **Trade-offs:** Less specialised tuning than a dedicated vector DB, and filtered ANN search needs care. It can migrate later behind the retrieval interface.
- **Cost:** ₹0 extra (it runs inside Postgres).
- **Status:** Accepted.

### TD-006 — Sentence Transformers for local embeddings
- **Reason:** Free, runs offline on a CPU, keeps resume text local, and is educational (you see the vectors).
- **Alternatives:** Gemini/OpenAI/Voyage embedding APIs (better quality, cost per token, data leaves the machine).
- **Trade-offs:** CPU embedding is slower and pulls in PyTorch (a large install of roughly 1 GB+). It must run in workers, not request handlers.
- **Status:** Accepted.

### TD-008 — Direct RAG implementation first
- **Reason:** The learning goal is to understand chunking, retrieval, context building and citations without framework abstractions hiding them.
- **Alternatives:** LangChain, LlamaIndex, Haystack.
- **Trade-offs:** More code to write. Adopting a framework later requires a new TD entry with a concrete justification.
- **Status:** Accepted.

### TD-009 — Gemini API as the initial LLM, behind `LLMProvider`
- **Reason:** A low-cost, free-tier option for development.
- **Alternatives:** Claude, OpenAI, local models through Ollama (free, needs RAM/GPU, lower quality).
- **Trade-offs:** Free-tier quotas and rate limits can change. Free-tier data-usage terms must be checked, which is one reason only synthetic data is sent. The provider interface keeps switching cheap.
- **Cost:** Expected ₹0 during development on the free tier, but verify the quotas in Phase 5. Paid usage needs approval.
- **Status:** Accepted.

### TD-010 — PyMuPDF + python-docx
- **Reason:** PyMuPDF offers fast, accurate PDF text extraction with page information. python-docx is the standard for DOCX.
- **Alternatives:** pypdf (BSD licence, simpler, weaker layout handling); pdfplumber (MIT, good for tables, slower); unstructured (heavy).
- **Trade-offs:** **PyMuPDF is AGPL-3.0** (or a commercial licence). This is fine for a personal or open-source learning project. Review it before any closed-source or commercial use; switching to pypdf or pdfplumber would be the fallback.
- **Status:** Accepted, with the licence caveat.

### TD-011 — Celery + Redis
- **Reason:** Bulk resume parsing and embedding are CPU-heavy and must not block the API. Celery is the most widely asked-about Python task queue.
- **Alternatives:** FastAPI `BackgroundTasks` (in-process, no retries or durability); RQ (simpler); Dramatiq; Arq (async-native).
- **Trade-offs:** More moving parts. Celery is synchronous, which interacts with TD-018 (an async DB driver needs care inside workers).
- **Status:** Accepted.

### TD-012 — Next.js + TypeScript + Tailwind
- **Reason:** The developer's existing strength, and it fits the target role of a Python + React full-stack developer.
- **Status:** Accepted.

### TD-013 — Docker, Docker Compose, GitHub Actions
- **Reason:** Reproducible environments, a CI that is standard in the industry, and simple deployment on a single host.
- **Note:** Docker is **not currently installed** (verified 2026-11-25). See TD-017 for how Postgres runs before Phase 8.
- **Status:** Accepted.

### TD-021 — Human-in-the-loop, explainable results; synthetic data only
- **Reason:** Ethical and legal risk in automated hiring. Explainability is also a product strength.
- **Rules:** No autonomous decisions. Component scores and citations are always shown. No protected attributes. Synthetic resumes only in development.
- **Status:** Accepted.

---

## Proposed (needs the developer's confirmation)

### TD-007 — Embedding model `all-MiniLM-L6-v2` (384 dimensions)
- **Reason:** Small (~80 MB), fast on a CPU, well documented, and a good baseline.
- **Alternatives:** `BAAI/bge-small-en-v1.5` (384-d, often better retrieval quality); `all-mpnet-base-v2` (768-d, better quality, slower).
- **Trade-offs:** Lower quality than larger models. Changing models means re-embedding and possibly changing the vector dimension (a migration).
- **Plan:** Start with MiniLM, evaluate against bge-small on the golden set in Phase 5/6, and record the result.
- **Status:** Proposed.

### TD-014 — Monorepo with a feature-module backend layout
- **Reason:** Each feature (`modules/candidates/`) holds its own router, schemas, service, repository and models. This keeps related code together and scales better than global `routers/`, `models/` and `schemas/` folders. The `backend/` and `frontend/` folders sit in one repository.
- **Alternatives:** Layer-based layout (common in tutorials, simpler at first); separate repositories for the frontend and backend.
- **Trade-offs:** Slightly more structure on day one, so introduce it gradually in Phase 2.
- **Status:** Proposed. Confirm at the start of Phase 2.

---

## Open (decide when the phase arrives)

_TD-015 was decided on 2026-11-25. It is kept below in its original position, with the status Accepted._

### TD-015 — uv for Python install, virtual environment and dependencies (Phase 1) — Accepted 2026-11-25
- **Decision:** `uv` (installed through Homebrew) manages the Python version (3.12), the project `.venv`, `pyproject.toml` dependencies and the `uv.lock` lockfile.
- **Reason:** One fast tool that covers the jobs of nvm + npm + package-lock. It is reproducible through the lockfile, and it is becoming common in the industry. The developer asked for the setup to be installed directly ("install whatever is needed").
- **Alternatives:** `pyenv` + `venv` + `pip` (classic, more steps); Homebrew `python@3.12` + `venv` + `pip`; Poetry.
- **Trade-offs:** uv is a newer tool, so some tutorials show `pip`/`venv` instead. The underlying concepts (venv, `site-packages`, `pyproject.toml`) are still taught explicitly in Phase 1, and `uv pip` / `python -m venv` equivalents are shown so that the knowledge transfers.
- **Verified:** `uv 0.13.10`; `uv python install 3.12` → CPython 3.12.16 at `~/.local/share/uv/python/`. The system Python 3.9.6 is left untouched.
- **Status:** Accepted.

### TD-016 — Linter/formatter (Phase 1)
- **Options:** Ruff (lint and format in one fast tool); Black + isort + flake8; plus optional mypy or pyright for type checking.

### TD-017 — Local PostgreSQL: Homebrew vs Docker (Phase 3)
- **Context:** `psql` is available through Homebrew. Docker is not installed, and Docker is scheduled for Phase 8.
- **Options:** Homebrew PostgreSQL + pgvector (no Docker needed until Phase 8); install Docker early and use Compose for Postgres and Redis (closer to production).
- **Trade-offs:** Learning-curve timing against environment parity. Redis in Phase 4 raises the same question.

### TD-018 — SQLAlchemy sync vs async (Phase 3)
- **Options:** sync (`psycopg` 3) with `def` endpoints, which is simpler and shares code easily with Celery; async (`asyncpg` / `psycopg` async) with `async def` endpoints, which is more scalable and modern but adds complexity, especially in Celery workers.
- **To decide:** In Phase 3, after the async concepts in Phase 1–2.

### TD-019 — Hosting: AWS vs VPS (Phase 8)
- **Options:** A VPS (Hetzner, DigitalOcean, Hostinger and similar) running Docker Compose, roughly ₹500–₹2,000 per month; AWS (EC2/Lightsail, optionally RDS), more resume-relevant and can use the free tier, with costs varying. Sentence Transformers needs about 2 GB+ of RAM.
- **To decide:** In Phase 8, with current pricing in ₹.

### TD-020 — File storage (Phase 4 / 8)
- **Options:** Local disk behind a `FileStorage` interface (development); S3 or another S3-compatible store in production.
