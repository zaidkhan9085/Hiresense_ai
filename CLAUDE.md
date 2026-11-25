# CLAUDE.md — HireSense AI

These instructions apply to **every** Claude Code session in this repository. Details are in the skills (`.claude/skills/`) and the docs (`docs/`); this file only holds the rules that always apply.

## 1. Project identity

- **HireSense AI** is an AI-powered recruitment intelligence platform. Recruiters upload resumes (PDF/DOCX, single or bulk), and the system extracts candidate profiles, supports semantic search, matches candidates to job descriptions, answers questions over resumes with RAG, compares candidates and shows analytics.
- **It helps people decide. It never makes hiring decisions.** Every score and answer must be explainable and traceable to its source (skills matched, resume chunks cited). The system never auto-rejects, auto-shortlists or ranks people on protected attributes.
- **Use synthetic resume data only** during development. Never use real candidate resumes.

## 2. Developer and learning objective

- The developer has about 2.9 years of experience and is strong in JavaScript/TypeScript, React, Next.js, Node.js/Express and PostgreSQL. They are **learning Python, FastAPI and GenAI/RAG**.
- Time budget: **about 2 hours per day** over an 8-week plan.
- Target roles: Python Backend, FastAPI, Python + React Full Stack, GenAI Developer, AI Application Developer.
- **Learning comes before finishing the app.** The developer must be able to understand, explain in interviews and maintain every line. Follow the `learning-mentor` skill for any significant implementation.

## 3. Technology stack (agreed — see `docs/TECH_DECISIONS.md`)

| Area | Choice |
|---|---|
| Backend | Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy 2, Alembic, PostgreSQL, JWT, Pytest |
| AI / RAG | Sentence Transformers, pgvector, Gemini API (initial LLM), direct retrieval code (no LangChain/LlamaIndex unless justified) |
| Documents | PyMuPDF, python-docx |
| Background jobs | Redis, Celery |
| Frontend | Next.js, TypeScript, Tailwind CSS |
| Infrastructure | Docker, Docker Compose, GitHub Actions, AWS or VPS |

- **Never silently replace a technology.** To propose a change, state the technical reason, the alternatives, the trade-offs and the cost impact (in ₹ where relevant), then wait for approval and record it in `TECH_DECISIONS.md`.
- **Add a dependency only when its milestone arrives.** For example, no Celery before Phase 4 and no `sentence-transformers` before Phase 5.

## 4. Repository layout (planned — check what actually exists before relying on this)

```
Hiresense_ai/
├── CLAUDE.md                 # this file
├── README.md
├── .claude/skills/           # project-development, python-fastapi, rag-engineering, learning-mentor, session-handoff
├── docs/                     # PROJECT_STATE (living status), ARCHITECTURE, DATABASE_SCHEMA, API_SPECIFICATION, TECH_DECISIONS, LEARNING_LOG
├── backend/                  # Phase 1+ : FastAPI app (app/), alembic/, tests/, pyproject.toml
├── frontend/                 # Phase 7  : Next.js app
├── data/synthetic/           # Phase 4  : synthetic resumes only
└── docker-compose.yml        # when the milestone requires it (see TECH_DECISIONS)
```

The backend module layout is described in `docs/ARCHITECTURE.md`.

## 5. General coding principles

- Write simple, readable and explicit code. Use the smallest design that solves the current milestone. No speculative abstractions.
- Separate concerns: routers handle HTTP, services hold business logic, repositories handle data access, schemas define the API contracts and models define the ORM tables.
- Use type hints on all Python code. Pydantic v2 models validate API input and output.
- Follow PEP 8 and the naming conventions in the `python-fastapi` skill.
- When you introduce an advanced construct (decorators, generics, metaclasses, context managers, `Annotated` dependencies and so on), explain why it is needed.

## 6. No unnecessary refactoring or unrelated changes

- Change only what the current task requires. Do not reformat, rename or restructure unrelated code.
- Inspect existing files before editing them. **Never overwrite existing work without reading it first.**
- If you notice an unrelated problem, report it and add it to `PROJECT_STATE.md` → Known issues. Do not fix it silently.

## 7. Dependencies

- Each new package needs: a purpose, the milestone that needs it, and the alternatives you considered (in one line if it is minor).
- Pin versions in the project's dependency file. Never install packages globally.
- Do not install anything without telling the developer which command you will run.

## 8. Security and privacy

- **Never put secrets in code, config, docs or tests.** Use environment variables (`os.environ` / Pydantic `BaseSettings`) and commit only a `.env.example` containing placeholders.
- `.env`, uploaded files, model caches and `data/` outputs must be listed in `.gitignore` before they first appear.
- Candidate data is PII. Use synthetic data only. Do not log resume text, emails or phone numbers. Send only synthetic data to external LLM APIs.
- Do not put real client, employee or candidate data in prompts, examples, fixtures or docs. (Texple policy: redact before pasting.)
- Every non-public endpoint needs authentication and role checks. Validate uploads by type, size and count.
- LLM output is untrusted. Never execute it, and never let resume content override system instructions (prompt injection).

## 9. Testing and verification

- Every feature ships with pytest tests at the right level (unit tests for services, API tests for routers).
- **Run the tests and report the real output.** Never claim that something passes without running it. If you could not run something, say so.
- "Done" means implemented, tested, verified by running it, and recorded in `PROJECT_STATE.md`.
- **Never assume something is implemented just because it was discussed earlier.** Check the code.

## 10. Phases — do not jump ahead

Phases 0–8 and their deliverables are listed in `docs/PROJECT_STATE.md`. Work only on the current phase. **Before starting a new phase, verify the previous phase's deliverables** (run the code and tests) and get the developer's approval.

## 11. Documentation maintenance

| Change | Update |
|---|---|
| Any meaningful work | `docs/PROJECT_STATE.md` |
| Learning progress | `docs/LEARNING_LOG.md` |
| Architectural decision made or changed | `docs/TECH_DECISIONS.md` (never rewrite history — mark old entries *Superseded*) |
| Table or column implemented or changed | `docs/DATABASE_SCHEMA.md` (move it from *Proposed* to *Implemented*) |
| Endpoint implemented or changed | `docs/API_SPECIFICATION.md` (status: *Planned* → *Implemented*) |
| Module or data flow changed | `docs/ARCHITECTURE.md` |

Each fact has one source of truth. Link to it rather than duplicating it.

## 12. Mandatory session-start procedure

Before starting any new task:

1. Read `CLAUDE.md` (this file).
2. Read `docs/PROJECT_STATE.md`.
3. Inspect the actual repository: `git status`, the current branch, recent commits and the relevant files.
4. Read the relevant entries in `docs/TECH_DECISIONS.md`.
5. Identify the current milestone.
6. Confirm the next logical task with the developer before writing code.

The full procedure is in the `session-handoff` skill.

## 13. Mandatory session-end procedure

At the end of meaningful work:

1. Update `docs/PROJECT_STATE.md`: work done, modified files, and the exact next step.
2. Update `docs/LEARNING_LOG.md` if learning progress was made.
3. Update `docs/TECH_DECISIONS.md` if an architectural decision changed.
4. Record completed and pending tasks.
5. Record the actual test and verification results (the commands run and their real outcomes).

**Never invent progress or test results.**

## 14. Git safety

- Do not commit, push, rebase, reset or force-anything unless the developer asks. Do not commit to `main` without being asked; suggest a feature branch.
- Never commit secrets, `.env`, uploaded resumes or large model files.
