---
name: project-development
description: Engineering workflow for building any feature, fix or change in HireSense AI. Covers inspecting the repository before coding, checking for existing code to reuse, layered architecture, naming, dependency management, error handling, testing, Git safety and verification. Use it whenever you are about to create, modify or review code or config files in this repository.
---

# Project Development Skill — HireSense AI

## When to activate

Use this skill when you:
- implement a feature, endpoint, model, migration, service, worker or UI component
- fix a bug or change behaviour
- add or upgrade a dependency
- review code (yours or the developer's)

This skill is about **how** to work safely. For Python/FastAPI conventions, see `python-fastapi`. For AI/RAG components, see `rag-engineering`. For explaining things to the developer, see `learning-mentor`.

---

## 1. General rules

1. **Inspect before you write.** Never create or overwrite a file without checking whether it exists and reading it first.
2. **Reuse before you create.** Search for an existing helper, schema, dependency or service before writing a new one.
3. **Stay in scope.** Change only what the current task needs. No drive-by refactors, renames or reformatting.
4. **Stay in phase.** Do not build features from a later phase (see `docs/PROJECT_STATE.md`).
5. **Make small, verifiable steps.** Each step should leave the code runnable and the tests passing.
6. **Do not change the stack silently.** Technology changes go through `docs/TECH_DECISIONS.md` with approval.
7. **Be honest about verification.** Report only commands you actually ran and their real output.

---

## 2. Repository inspection (before coding)

Run or check the following:

```bash
git status && git branch --show-current
git log --oneline -10
```

- Read `docs/PROJECT_STATE.md` → current milestone and known issues.
- List the relevant directories (for example `backend/app/modules/<feature>/`).
- Read the files you will touch **in full**, plus their tests.
- Check `docs/DATABASE_SCHEMA.md` and `docs/API_SPECIFICATION.md`: is the item *Planned* or *Implemented*? Then confirm against the code, because the docs may lag behind it.

## 3. Reuse checks

Before creating something new, search for:

| Creating… | Search for |
|---|---|
| A Pydantic schema | an existing `schemas.py` in the module, plus shared schemas (pagination, errors) |
| A DB query | existing repository functions for that model |
| A dependency (`Depends`) | `app/core/deps.py` / `app/api/deps.py` (current user, DB session, role checks) |
| A config value | the `Settings` class in `app/core/config.py` |
| An exception | the custom exceptions in `app/core/exceptions.py` |
| A utility | `grep -rn "def <likely_name>" backend/app` |
| A package | `pyproject.toml`. Is it already installed? Does the standard library cover it? |

If something similar exists, extend it. If you create a new one anyway, explain why the existing one does not fit.

## 4. Feature development workflow

1. **Clarify.** Restate the task, its acceptance criteria and the phase it belongs to.
2. **Inspect.** Do sections 2 and 3 above.
3. **Design.** Briefly describe the files, layers, data flow and DB/API changes. For significant work, follow `learning-mentor` (explain first and offer the developer the chance to attempt it).
4. **Implement incrementally.** Usual order: schema/model → migration → repository → service → router → tests.
5. **Test.** Write or extend the tests, then run them.
6. **Verify.** Start the app or call the endpoint where relevant, and check the migration with `alembic upgrade head` and `downgrade -1`.
7. **Document.** Update the docs listed in the CLAUDE.md §11 table.
8. **Hand off.** Follow the `session-handoff` end procedure.

## 5. Clean architecture and separation of concerns

```
HTTP request
  → router (app/modules/<feature>/router.py)     # parse/validate, auth deps, call service, return schema
  → service (…/service.py)                        # business rules, orchestration, no FastAPI imports
  → repository (…/repository.py)                  # SQLAlchemy queries only, no business rules
  → models (…/models.py)                          # ORM tables
schemas.py                                        # Pydantic request/response contracts
```

Rules:
- Routers do not contain SQL or business logic.
- Services do not import `fastapi` (other than raising domain exceptions that are mapped to HTTP elsewhere). This keeps them testable and reusable from Celery workers.
- Repositories do not decide business outcomes.
- The AI layer (`app/ai/`) exposes plain Python interfaces such as `EmbeddingProvider` and `LLMProvider`. Business code never calls a vendor SDK directly.
- Do not add layers you do not need. A trivial health endpoint does not need a repository.

## 6. Naming conventions

| Item | Convention | Example |
|---|---|---|
| Python modules/files | `snake_case` | `resume_parser.py` |
| Functions, variables | `snake_case`, verb-first for functions | `extract_text_from_pdf()` |
| Classes | `PascalCase` | `CandidateService` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_UPLOAD_SIZE_MB` |
| Pydantic schemas | `<Entity><Purpose>` | `CandidateCreate`, `CandidateRead`, `CandidateUpdate` |
| ORM models | singular `PascalCase` | `Candidate`; table name is plural snake: `candidates` |
| DB columns | `snake_case`; FKs as `<entity>_id` | `candidate_id`, `created_at` |
| API paths | plural nouns, kebab-case, versioned | `/api/v1/job-descriptions/{job_id}/matches` |
| Tests | `test_<unit>_<behaviour>` | `test_login_rejects_wrong_password` |
| Branches | `<type>/<short-desc>` | `feat/resume-upload`, `fix/jwt-expiry` |
| Commits | Conventional Commits | `feat(resumes): add PDF text extraction` |

## 7. Dependency management

Before adding a package:
1. Confirm the current milestone needs it (CLAUDE.md §3 and the phase list).
2. Check whether the standard library or an existing dependency already covers the need.
3. State: the package, its purpose, its licence (flag GPL/AGPL), its size and the alternatives.
4. Show the exact install command and wait for approval.
5. Pin the version and record any significant choice in `TECH_DECISIONS.md`.

Separate runtime and dev dependencies (pytest and linters are dev-only).

## 8. Error handling

- Define domain exceptions (`CandidateNotFoundError`, `DuplicateResumeError`, `UnsupportedFileTypeError`) in the service layer.
- Map them to HTTP responses in **one place** (FastAPI exception handlers). Use the standard error body from `docs/API_SPECIFICATION.md`.
- Never use bare `except:` or swallow exceptions. Catch specific exceptions, log them with context (no PII) and re-raise or convert them.
- Validate at the boundary (Pydantic). Trust validated data inside.
- External calls (LLM, embeddings, Redis) need timeouts and clear failure messages. Retries belong in workers, not in request handlers.
- Do not expose stack traces or internal errors in API responses.

## 9. Testing

- **Unit tests** for services and pure functions (chunking, scoring, parsing).
- **API tests** with FastAPI's `TestClient`/`httpx.AsyncClient` for routers, including auth failures and validation errors.
- **DB tests** run against a test database and are isolated per test (transaction rollback or a fresh schema).
- **AI tests** mock the LLM and use deterministic fixtures. Do not call paid or quota-limited APIs in the test suite.
- Each bug fix gets a regression test.
- Run `pytest -q` (or the narrower path) and paste the summary line into the handoff.

## 10. Git safety

- Check `git status` before and after the work. Never discard uncommitted changes you did not make.
- Do not commit, push, amend, rebase, reset or force-push without an explicit request.
- Suggest a feature branch rather than committing to `main`.
- Never stage `.env`, secrets, uploaded resumes, `data/` outputs or model weights.
- Keep commits focused: one logical change per commit.

## 11. Avoiding unrelated changes

- No mass reformatting. If a formatter is adopted later, run it in its own commit.
- No renaming or moving of files unless the task requires it.
- Note unrelated issues under *Known issues* in `PROJECT_STATE.md` instead of fixing them.

## 12. Code review and verification checklist

Before declaring a task done, check:
- [ ] The scope matches the task, with no unrelated diffs (`git diff --stat`).
- [ ] Type hints are complete, and names follow the conventions above.
- [ ] Layers are respected (no SQL in routers, no FastAPI in services).
- [ ] No secrets, PII or real data appear in code, tests or logs.
- [ ] Inputs are validated, and errors are mapped consistently.
- [ ] Tests were added and **run**, and the real results are recorded.
- [ ] Migrations upgrade and downgrade cleanly (if any).
- [ ] The docs are updated (CLAUDE.md §11).
- [ ] The developer received an explanation (`learning-mentor`).

---

## Examples

**Good:** "Task: add `GET /api/v1/candidates/{id}`. I inspected `modules/candidates/`: `CandidateRead` and `get_by_id()` already exist, so I will reuse both. I will add a `get_candidate()` service with a not-found exception, a router, and 3 tests (200, 404, 401). Here is the test output."

**Bad:** Creating a new `utils/helpers.py` with a duplicate DB session factory, reformatting `main.py`, and saying "tests should pass".

---

## Restrictions

- Never overwrite or delete existing files without reading them first.
- Never implement work from a later phase or add dependencies early.
- Never fabricate test results, command output or progress.
- Never commit or push without being asked.
- Never introduce real candidate, client or employee data.
