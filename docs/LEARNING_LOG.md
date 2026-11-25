# LEARNING_LOG — HireSense AI

> Maintained under the `learning-mentor` skill. **Record only evidence-based progress.** Claude explaining a concept moves it to Level 1 at most; higher levels require the developer's own demonstrated work.

## Evidence scale

| Level | Meaning | Evidence required |
|---|---|---|
| 0 | Not started | — |
| 1 | Introduced | Explanation given |
| 2 | Understands | Correctly explains or predicts code that Claude wrote (✅ answers) |
| 3 | Independent | Implemented or modified it without help (optional in the current learning mode) |
| 4 | Interview-ready | Explains trade-offs; passed the understanding checks and the phase quiz |

## Baseline (self-reported, 2026-11-25)

- **Strong:** JavaScript, TypeScript, React, Next.js, Node.js, Express, PostgreSQL (SQL).
- **Some:** general backend development.
- **Learning:** Python, FastAPI, GenAI, RAG.
- No Python, FastAPI or RAG competencies have been assessed yet.

---

## 1. Competency tracker

### Python
| Concept | Level | Evidence / date |
|---|---|---|
| Environment: venv, pip/uv, pyproject.toml | 2 | 2026-11-25: ran uv init/run/add --dev with guidance; explained .venv vs uv.lock correctly |
| Core types, truthiness, `None` | 2 | 2026-11-25: explained falsy None/"" correctly (Q2 ✅); `-> None` partial |
| Lists/dicts/sets/tuples, comprehensions | 0 | — |
| Functions: args, kwargs, keyword-only, defaults pitfalls | 0 | — |
| Modules, packages, imports | 0 | — |
| Exceptions: try/except/else/finally, custom exceptions | 0 | — |
| Classes, OOP, dataclasses, dunder methods | 0 | — |
| Type hints, `Protocol`, generics basics | 0 | — |
| Iterators, generators, `yield` | 0 | — |
| Decorators | 0 | — |
| Context managers (`with`) | 0 | — |
| File I/O with `pathlib` | 0 | — |
| `async`/`await`, asyncio basics | 0 | — |
| Logging | 0 | — |
| Pytest: fixtures, parametrize, mocking | 0 | — |

### FastAPI and backend
| Concept | Level | Evidence / date |
|---|---|---|
| Routing, path/query/body params | 0 | — |
| Pydantic v2 models, validators | 0 | — |
| Dependency injection (`Depends`, `yield` deps) | 0 | — |
| Settings with pydantic-settings | 0 | — |
| Exception handlers, error format | 0 | — |
| SQLAlchemy 2 models, sessions, queries | 0 | — |
| Relationships, N+1, eager loading | 0 | — |
| Alembic migrations | 0 | — |
| Password hashing, JWT, RBAC | 0 | — |
| File uploads | 0 | — |
| Celery + Redis tasks | 0 | — |
| API testing (TestClient), DB test isolation | 0 | — |

### AI and RAG
| Concept | Level | Evidence / date |
|---|---|---|
| Text extraction (PDF/DOCX), cleaning | 0 | — |
| Chunking strategies | 0 | — |
| Embeddings and vector similarity | 0 | — |
| pgvector, HNSW indexes | 0 | — |
| Metadata filtering, hybrid search, RRF | 0 | — |
| Reranking (cross-encoder) | 0 | — |
| Context construction, prompting | 0 | — |
| Citations and hallucination mitigation | 0 | — |
| RAG evaluation (Recall@k, MRR, faithfulness) | 0 | — |

### Infrastructure
| Concept | Level | Evidence / date |
|---|---|---|
| Docker, Docker Compose | 0 | — |
| GitHub Actions CI | 0 | — |
| Deployment (AWS/VPS) | 0 | — |

---

## 2. Concepts I can independently implement

_None recorded yet. A concept appears here only at Level 3 or above, with evidence._

## 3. Topics requiring revision

- `None` and return-type hints (Python has one `None`; functions without `return` return `None`)
- What `.venv` contains and how `uv.lock` rebuilds it
- `dict[key]` (KeyError) vs `dict.get(key)` (None)
- `str.partition()` always returns a 3-tuple; tuple unpacking

## 4. Practical exercises

| Date | Phase | Exercise | Difficulty | Status | Notes |
|---|---|---|---|---|---|
| 2026-11-25 | 1 | Ex 1: `parse_resume()` → `Resume` dataclass (9 tests in `backend/tests/test_resume_parser.py`) | easy–medium | implemented by Claude | Learning mode changed: Claude writes, the developer answers questions. Questions pending |

Status values: assigned · attempted · completed · reviewed.

## 5. Interview questions

| Date | Topic | Question | Assessment (✅/🟡/🔴) | Follow-up |
|---|---|---|---|---|
| 2026-11-25 | Environment | Why commit `uv.lock` but not `.venv/`? | ✅ | — |
| 2026-11-25 | Environment | What happens if `.venv/` is deleted and `uv run` is run? | 🟡 | Missing: uv rebuilds `.venv` from `uv.lock` |
| 2026-11-25 | Types | What does `-> None` mean? | 🟡 | `None` is not `undefined`; it is like TS `: void`; hints are not enforced at runtime |

---

## 6. Session entries

### 2026-11-25 — Phase 0 — Setup
- **Topics studied:** None. This session created the instruction system and docs only.
- **Concepts introduced:** None.
- **Exercises:** None.
- **Next learning focus (Phase 1):** Python environment (venv/pyproject compared with node_modules/package.json), core types and truthiness, comprehensions, functions and their pitfalls.

### 2026-11-25 — Phase 1 — Environment and tooling
- **Topics studied:** uv, `.venv`, `pyproject.toml`, `uv.lock`, `[project.scripts]`, dev dependencies.
- **Understanding check:** Q1 ✅, Q2 🟡, Q3 🟡 (see the interview table).
- **Exercise assigned:** Ex 1, `parse_resume()`.

### 2026-11-25 — Learning mode changed
- The developer chose to learn by reading Claude's code and answering questions (limited time). Claude implemented Ex 1 and explained it. The evidence scale Level 2 is now "Understands" (correct explanations/predictions).
- **Concepts introduced (Level 1):** dicts and `.get()`, `str.partition/strip/lower/split/splitlines`, sets, dataclasses + `default_factory`, falsy values, `try/except` + `raise ... from`, private-by-convention `_functions`.
- **Questions asked:** Q1 `d[k]` vs `d.get(k)` 🟡 (missed KeyError); Q2 why `if not name` covers None and "" ✅; Q3 `str.partition()` output 🔴.
