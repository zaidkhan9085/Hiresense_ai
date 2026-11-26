# PROJECT_STATE — HireSense AI

> The living source of truth for project status. Read it at the start of every session and update it at the end (see the `session-handoff` skill).
> **The repository wins over this file.** If they disagree, verify, then fix this file.

**Last updated:** 2026-11-25 · **Current phase:** Phase 1 — Python fundamentals and environment (Step 1 done: tooling installed)

---

## 1. Objective

Build **HireSense AI**, an AI-powered recruitment intelligence platform (resume ingestion, candidate profiles, job descriptions, semantic search, explainable matching, RAG Q&A, comparison and analytics) **while** turning a JS/TS developer into a job-ready Python/FastAPI/GenAI engineer. The developer's learning matters more than finishing the app. The system helps humans decide; it never makes hiring decisions. Development uses synthetic data only.

## 2. Developer background

About 2.9 years of experience. Strong in JS/TS, React, Next.js, Node/Express and PostgreSQL. Learning Python, FastAPI and GenAI/RAG. About 2 hours per day over an 8-week plan. Learning progress is tracked in `LEARNING_LOG.md`.

## 3. Phase roadmap and deliverables

Estimates assume about 14 hours per week. Do not start a phase until the previous phase's deliverables are verified **and** the developer approves.

| Phase | Week | Focus | Status |
|---|---|---|---|
| 0 | — | Claude instruction system and docs | ✅ Done (approved 2026-11-25) |
| 1 | 1 | Python fundamentals and environment setup | 🟡 In progress |
| 2 | 2 | FastAPI fundamentals | ⚪ Not started |
| 3 | 3 | PostgreSQL, SQLAlchemy, Alembic, JWT auth | ⚪ Not started |
| 4 | 4 | Resume processing and background tasks (Redis/Celery) | ⚪ Not started |
| 5 | 5 | Embeddings, pgvector, semantic search, basic RAG | ⚪ Not started |
| 6 | 6 | Hybrid search, reranking, candidate matching, evaluation | ⚪ Not started |
| 7 | 7 | Next.js frontend integration and testing | ⚪ Not started |
| 8 | 8 | Docker, CI/CD, deployment, production readiness | ⚪ Not started |

### Deliverables per phase (the definition of done)

**Phase 0 — Instruction system**
- [x] `CLAUDE.md`
- [x] 5 skills: project-development, python-fastapi, rag-engineering, learning-mentor, session-handoff
- [x] docs: PROJECT_STATE, ARCHITECTURE, DATABASE_SCHEMA, API_SPECIFICATION, TECH_DECISIONS, LEARNING_LOG
- [x] README.md
- [x] Developer review and approval (2026-11-25)
- [ ] First commit of the instruction system (only when the developer asks)

**Phase 1 — Python fundamentals and environment**
- [x] Python 3.12+ installed. The package/venv tool is decided (TD-015: uv) and recorded. (2026-11-25: uv 0.13.10, CPython 3.12.16)
- [x] `backend/` created with `uv init` (`pyproject.toml`, `.python-version` = 3.12, `src/backend/` package) and a root `.gitignore` covering `.venv`, `.env`, `__pycache__`, uploads and data outputs. (The `.venv` is not created yet; `uv sync` / `uv run` will create it.)
- [ ] Fundamentals practised in project-relevant code: types, collections, comprehensions, functions, dataclasses, classes/OOP, exceptions, modules/packages, file I/O with `pathlib`, an intro to typing/`Protocol`, and an intro to `async`.
- [ ] A small pure-Python module (no web framework), such as a plain-text synthetic resume → `dataclass` parser, with pytest tests that the developer wrote with guidance.
- [x] The linter/formatter is decided (TD-016: Ruff). pytest 9.2.0 + Ruff 0.17.6 are dev dependencies; `.venv` and `uv.lock` were created by `uv run`.
- [ ] The phase quiz and an independent task are recorded in `LEARNING_LOG.md`.

**Phase 2 — FastAPI fundamentals**
- [ ] The FastAPI app skeleton is set up following the module layout in `ARCHITECTURE.md`. Settings use `pydantic-settings`.
- [ ] `GET /api/v1/health` implemented.
- [ ] In-memory CRUD for job descriptions (routers, Pydantic v2 schemas, `Depends`, status codes, the error format) to learn the patterns before the DB arrives.
- [ ] Exception handlers, logging setup, API tests with `TestClient`, and the OpenAPI docs reviewed.

**Phase 3 — Database and auth**
- [ ] The PostgreSQL environment is decided (TD-017). The sync/async driver is decided (TD-018).
- [ ] SQLAlchemy 2 models and Alembic migrations for `users` and `job_descriptions` (and `candidates` if time allows).
- [ ] Register/login/refresh/me endpoints, password hashing, JWT and the `require_role` RBAC.
- [ ] Job description CRUD persisted. DB-backed tests are isolated.

**Phase 4 — Resume processing**
- [ ] A synthetic resume dataset (PDF and DOCX) in `data/synthetic/`.
- [ ] Single and bulk upload endpoints with validation (type, size, checksum de-duplication).
- [ ] PyMuPDF and python-docx extraction, cleaning, and section/field parsing → candidate profile.
- [ ] Redis and a Celery worker. Status tracking (`uploaded → processing → processed/failed`). Retries are safe.
- [ ] Tests for the extractors, the parser and the upload API.

**Phase 5 — RAG and semantic search**
- [ ] pgvector is enabled through a migration, and `resume_chunks` exists with embeddings.
- [ ] Section-aware chunking, Sentence Transformers embeddings in the worker, and the `EmbeddingProvider` interface.
- [ ] Semantic candidate search with metadata filters.
- [ ] RAG Q&A over resumes using `LLMProvider` (Gemini), with validated citations and a "not found" fallback.
- [ ] A golden evaluation set, with baseline Recall@k/MRR recorded below.

**Phase 6 — Advanced retrieval and matching**
- [ ] Hybrid search (full-text + vector, RRF) and an optional cross-encoder reranker, with before/after metrics.
- [ ] Explainable job↔candidate matching with stored component scores and explanations.
- [ ] A candidate comparison endpoint. Analytics endpoints.

**Phase 7 — Frontend**
- [ ] A Next.js + TS + Tailwind app: auth, upload (with status polling), candidates, jobs, search, matches, RAG Q&A with citations, comparison, and analytics.
- [ ] Frontend tests where valuable. The end-to-end flow is verified manually.

**Phase 8 — Production readiness**
- [ ] Dockerfiles and Docker Compose (api, worker, postgres+pgvector, redis, frontend).
- [ ] GitHub Actions CI (lint, tests). Deployment to AWS or a VPS (decision TD-019, with a ₹ cost estimate).
- [ ] Health checks, structured logging, rate limiting, security review, and a backup note.

## 4. Current milestone

**Phase 1 — Python fundamentals and environment.** Step 1 is done: uv and Python 3.12.16 are installed (TD-015). No `backend/` project or application code exists yet.

## 5. Pending tasks

1. Commit the Phase 0 docs when the developer asks (nothing is committed yet).
2. Phase 1 Step 2: create `backend/` with `uv init`, pin Python 3.12, and add `.gitignore` (the developer runs the commands, with explanation).
3. Phase 1 Step 3: decide on the linter/formatter (TD-016), then start the fundamentals exercises.

## 6. Blockers

- None. (The Python 3.12 blocker was resolved on 2026-11-25 through uv.)

**Layout note:** `uv init --package` created `backend/src/backend/`, but `ARCHITECTURE.md` plans `backend/app/`. Decide at the start of Phase 2 (the TD-014 confirmation) whether to rename it to `app/` or update the docs. Do not change either silently.

## 7. Known issues

- **Workspace root:** the Git repository is `Hiresense_ai/`, inside the `zaid_fastapi/` folder. Start Claude Code **inside `Hiresense_ai/`**, so that `CLAUDE.md` and `.claude/skills/` are loaded automatically.
- The developer's MoneyTV reference skill was mentioned in the Phase 0 brief but was not included in it. The skills follow the structure described in the brief (frontmatter, activation, rules, guidelines, examples, reuse checks, restrictions).

## 8. Last verified state (2026-11-25)

| Check | Result |
|---|---|
| Git repository | `Hiresense_ai/`, branch `main`, **no commits yet**, remote `origin` configured |
| Files before Phase 0 | None (an empty repository) |
| Application code | **None.** No `backend/` or `frontend/`, no packages installed |
| System Python | `python3 --version` → `Python 3.9.6` (left untouched; the project uses uv-managed 3.12) |
| Project Python | `uv python find 3.12` → `~/.local/share/uv/python/cpython-3.12-macos-aarch64-none/bin/python3.12`, `--version` → `Python 3.12.16` |
| Tooling present | `git`; `psql` at `/opt/homebrew/bin/psql` (a Homebrew PostgreSQL client) |
| Tooling | `uv 0.13.10` (Homebrew, installed 2026-11-25). Absent: `docker`, `pyenv` |

## 9. Verification results

| Date | What | Command | Result |
|---|---|---|---|
| 2026-11-25 | Skill frontmatter | Python script parsed the `---` header of each `SKILL.md` | 5/5 have `name` + `description`, `name` matches the folder, no extra keys |
| 2026-11-25 | No application code | `find` for *.py, *.ts, *.js, pyproject.toml, package.json, Dockerfile, *.yml | None found |
| — | Tests | — | Not applicable (no code yet) |

## 10. Next recommended task

**Phase 1 Step 2:** create the `backend/` project with uv (`uv init`, Python 3.12 pinned, `.venv`, `pyproject.toml`) and a root `.gitignore`. Follow the `learning-mentor` loop: explain how venv/`pyproject.toml`/`uv.lock` compare with `node_modules`/`package.json`/`package-lock.json`, and let the developer run the commands.

## 11. Important constraints

- Do not jump phases. Verify the previous phase's deliverables, then get approval.
- No dependency before its milestone. No silent technology changes (`TECH_DECISIONS.md`).
- Synthetic data only. No secrets in code. No real PII sent to external APIs.
- Explainable, human-in-the-loop results only. No autonomous hiring decisions.
- Never record unverified progress or test results.

---

## 12. Session history

### 2026-11-25 — Phase 0 — Instruction system created
- **Done:** Inspected the repository (empty Git repo, `main`, no commits). Created `CLAUDE.md`, `README.md`, 5 skills under `.claude/skills/`, and 6 docs under `docs/`.
- **Files changed:** CLAUDE.md, README.md, .claude/skills/{project-development,python-fastapi,rag-engineering,learning-mentor,session-handoff}/SKILL.md, docs/{PROJECT_STATE,ARCHITECTURE,DATABASE_SCHEMA,API_SPECIFICATION,TECH_DECISIONS,LEARNING_LOG}.md
- **Commands run / results:** `git status` → no commits, clean; `python3 --version` → 3.9.6; `which docker uv pyenv` → not found; `psql` found. Frontmatter check → 5/5 valid. Code-file `find` → none. No application code or packages.
- **Known issues:** Python 3.12 is missing. Claude Code must be started inside `Hiresense_ai/`.
- **Incomplete:** The developer's review and approval. Nothing has been committed.
- **Next step:** The developer reviews Phase 0. After approval, Phase 1, Step 1 (TD-015, the Python environment).

### 2026-11-25 — Phase 1 — Step 1: Python tooling installed
- **Done:** The developer approved Phase 0 and asked for the required tools to be installed. TD-015 was decided (uv). uv and Python 3.12 were installed.
- **Files changed:** docs/TECH_DECISIONS.md (TD-015), docs/PROJECT_STATE.md
- **Commands run / results:** `brew install uv` → uv 0.13.10; `uv python install 3.12` → CPython 3.12.16 installed; `uv python find 3.12` + `--version` → Python 3.12.16.
- **Known issues:** None.
- **Incomplete:** The `backend/` project is not created yet. Nothing is committed.
- **Next step:** Phase 1 Step 2: `uv init` the `backend/` project and add `.gitignore` (see §10).

### 2026-11-25 — Phase 1 — Step 2: backend project committed
- **Done:** The developer merged PR #1 (Phase 0). The developer created `backend/` with `uv init`. Claude added a root `.gitignore` and committed both on `feat/phase-1-backend-setup` (PR #2).
- **Files changed:** .gitignore, backend/{pyproject.toml,.python-version,README.md,src/backend/__init__.py}, docs/PROJECT_STATE.md
- **Commands run / results:** `git pull` on main → at merge commit 71cee70. No Python code was run.
- **Known issues:** The `src/backend` vs `app/` layout mismatch (see the Blockers note).
- **Next step:** Phase 1 Step 3: run `uv run backend` (creates `.venv`), learn venv/pyproject, decide on the linter (TD-016).

### 2026-11-25 — Phase 1 — Step 3: tooling + Exercise 1 set up
- **Done:** The developer ran `uv run backend` (created `.venv`, `uv.lock`) and `uv add --dev pytest ruff`. Claude added the Ruff/pytest config to `pyproject.toml`, the Exercise 1 skeleton `backend/src/backend/resume_parser.py` and `backend/tests/test_resume_parser.py`. TD-016 accepted.
- **Files changed:** backend/pyproject.toml, backend/uv.lock (new), backend/src/backend/resume_parser.py (new), backend/tests/test_resume_parser.py (new), docs/{PROJECT_STATE,TECH_DECISIONS,LEARNING_LOG}.md
- **Commands run / results:** `uv run backend` → "Hello from backend!" (Python 3.12.16); `uv run pytest -q` → 9 failed (expected: the skeleton raises NotImplementedError); `uv run ruff check .` → All checks passed; `ruff format --check` → 4 files already formatted.
- **Known issues:** None. Nothing committed yet.
- **Incomplete:** Exercise 1 is assigned to the developer.
- **Next step:** The developer implements `parse_resume()` until `uv run pytest -v` passes, then Claude reviews it (learning-mentor review).

### 2026-11-25 — Phase 1 — Exercise 1 implemented by Claude
- **Done:** The developer switched the learning mode (Claude writes code; the developer reads and answers questions). The `learning-mentor` skill was updated. Claude implemented `parse_resume()` with the helpers `_parse_fields`, `_parse_skills` and `_parse_experience`.
- **Files changed:** backend/src/backend/resume_parser.py, .claude/skills/learning-mentor/SKILL.md, docs/{LEARNING_LOG,PROJECT_STATE}.md
- **Commands run / results:** `uv run pytest -v` → 9 passed; `uv run ruff check .` → All checks passed; `ruff format --check` → 4 files already formatted.
- **Known issues:** None. Nothing committed since PR #2.
- **Next step:** The developer answers the questions on the parser → commit the Phase 1 work through a PR → next fundamentals topic: classes/OOP + `Protocol` (a `ResumeSource` that reads `.txt` files from `data/synthetic/` with `pathlib`).

### 2026-11-25 — Phase 1 — Exercise 1 questions answered, committed
- **Done:** The developer answered Q1 🟡, Q2 ✅, Q3 🔴 (logged). The Phase 1 work was committed on `feat/phase-1-tooling-parser` and a PR was opened.
- **Commands run / results:** `uv run pytest -q` → 9 passed (before the commit).
- **Next step:** The developer merges the PR → next topic: classes/OOP + `Protocol` + `pathlib` (`ResumeSource` reading synthetic `.txt` resumes).

### 2026-11-26 — Phase 1 — ResumeSource (classes, Protocol, pathlib)
- **Session start:** PR #3 was confirmed merged (522240d); `main` was pulled; the merged local branches were deleted; baseline `uv run pytest -q` → 9 passed.
- **Done:** Branch `feat/phase-1-resume-source`. Added `backend/src/backend/resume_source.py` (`RawResume`, the `ResumeSource` Protocol, `DirectoryResumeSource`, `InMemoryResumeSource`, `LoadResult`, `load_resumes()`), `backend/tests/test_resume_source.py` (5 tests), and 3 synthetic resumes plus a README in `data/synthetic/`.
- **Commands run / results:** `uv run pytest -v` → 14 passed; `uv run ruff check .` → All checks passed; `ruff format --check` → 6 files already formatted.
- **Known issues:** None. Not committed yet.
- **Next step:** The developer answers the 3 questions → commit + PR → next topic: functions in depth (`*args`/`**kwargs`, keyword-only args), comprehensions, and an intro to `async`.
