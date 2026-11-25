---
name: python-fastapi
description: Python 3.12+ and FastAPI conventions for HireSense AI, with comparisons to JavaScript/Node.js. Covers PEP 8, type hints, functions, classes and OOP, async/await, FastAPI routing, Pydantic v2, dependency injection, SQLAlchemy 2, PostgreSQL, Alembic migrations, JWT and RBAC, exception handling, configuration, logging and pytest. Use it whenever you write, review or explain Python or backend code in this repository.
---

# Python & FastAPI Skill — HireSense AI

## When to activate

- Writing or reviewing any Python file in `backend/`
- Designing endpoints, schemas, models, migrations or auth
- Explaining a Python or FastAPI concept to the developer

The developer knows JS/TS, Express and PostgreSQL well. **Anchor new concepts to what they already know**, and explain any advanced construct before you use it.

---

## 1. General rules

1. Target **Python 3.12+**. Use modern syntax: `list[str]`, `X | None`, `match` where it is clearer, and `type` aliases.
2. Follow PEP 8 (4-space indentation, `snake_case`, a line length of about 100 characters), and keep the style consistent across files.
3. Type hints on **every** function signature and class attribute.
4. Prefer plain functions. Use classes when there is state or a clear interface (services, providers).
5. Write small modules with one responsibility. No circular imports.
6. Prefer the standard library. Do not add a package for something `pathlib`, `dataclasses`, `enum`, `logging` or `hashlib` can do.
7. **Do not introduce an advanced abstraction (generic repository base class, metaclass, custom decorator, plugin registry) without explaining its purpose and getting agreement.**

## 2. Python vs JavaScript/Node.js — quick map

| Concept | JS/TS / Node | Python |
|---|---|---|
| Package manifest | `package.json` | `pyproject.toml` |
| Local deps | `node_modules/` | virtual environment `.venv/` (must be activated or run through the tool) |
| Import | `import { x } from './a'` | `from app.a import x` (absolute imports from package root) |
| Types | TS types are erased at compile time | type hints are **not enforced at runtime**; Pydantic enforces them at the boundaries |
| Interfaces | `interface` | `typing.Protocol` (structural) or `abc.ABC` (nominal) |
| Object literal | `{a: 1}` | `dict` for raw data; `dataclass` / Pydantic model for structured data |
| `null/undefined` | two values | one value: `None` |
| Truthiness | `[]` is truthy | `[]`, `{}`, `""`, `0` and `None` are **falsy** |
| Equality | `===` | `==` (value); `is` only for `None` / identity |
| Array methods | `.map/.filter` | list comprehensions `[f(x) for x in xs if cond]` |
| Async | single-threaded event loop; everything is non-blocking by default | `asyncio` event loop; **blocking calls inside `async def` freeze the loop** |
| Errors | `throw` / `try/catch` | `raise` / `try/except/else/finally` |
| Middleware | Express `app.use` | FastAPI middleware plus **dependencies** (`Depends`), which are more granular |
| Validation | Zod / Joi | Pydantic v2 |
| ORM | Prisma / TypeORM / Sequelize | SQLAlchemy 2 |
| Migrations | Prisma migrate / Knex | Alembic |
| Test runner | Jest / Vitest | pytest (fixtures instead of `beforeEach`) |
| Env config | `dotenv` + `process.env` | `pydantic-settings` `BaseSettings` |

## 3. Functions, classes and OOP

- Use keyword-only arguments (`def f(*, limit: int)`) for clarity on functions with many parameters.
- **Never use mutable default arguments** (`def f(x: list = [])` is a classic bug; use `None` and create the list inside).
- `@dataclass(slots=True)` suits internal value objects. Pydantic models are for validation and serialisation at boundaries.
- `@property` for computed attributes, `@classmethod` for alternative constructors, `@staticmethod` rarely.
- Use `Protocol` for swappable providers (`EmbeddingProvider`, `LLMProvider`), not deep inheritance trees.
- Dunder methods (`__init__`, `__repr__`, `__eq__`) are covered under `learning-mentor` when they first appear.

## 4. Async and await

- FastAPI runs `async def` endpoints on the event loop, and **plain `def` endpoints in a threadpool**. Both are valid.
- Use `async def` only when everything awaited inside is truly async (async DB driver, `httpx.AsyncClient`).
- **CPU-heavy or blocking work** (PDF parsing, embedding generation, synchronous SDK calls) must not run directly inside `async def`. Offload it to Celery (Phase 4+) or `run_in_threadpool`.
- Compared with Node: Python does not auto-parallelise I/O for you. Use `asyncio.gather` for concurrent awaits, which is like `Promise.all`.

## 5. FastAPI routing

```python
# app/modules/candidates/router.py  (illustrative)
router = APIRouter(prefix="/candidates", tags=["candidates"])

@router.get("/{candidate_id}", response_model=CandidateRead)
async def get_candidate(
    candidate_id: UUID,
    service: Annotated[CandidateService, Depends(get_candidate_service)],
    _: Annotated[User, Depends(require_role(Role.RECRUITER))],
) -> CandidateRead:
    return await service.get(candidate_id)
```

- Mount routers under `/api/v1` in `main.py`.
- Always declare `response_model` (or a return type) so that output is filtered and documented.
- Use status codes deliberately: 201 for create, 202 for accepted async jobs, 204 for delete.
- Path params identify a resource; query params filter or paginate; the body carries data.
- Keep handlers thin (see the `project-development` architecture section).

## 6. Pydantic v2

- Use separate schemas per purpose: `XCreate`, `XUpdate` (all fields optional), `XRead`.
- `model_config = ConfigDict(from_attributes=True)` on read schemas built from ORM objects (this replaced v1's `orm_mode`).
- Use `Field(..., min_length=, max_length=, ge=)` constraints, `EmailStr`, and `@field_validator` / `@model_validator`.
- v1 → v2 renames to watch for in old tutorials: `.dict()` → `.model_dump()`, `.parse_obj()` → `.model_validate()`, `@validator` → `@field_validator`.
- Never return ORM objects that carry sensitive fields (such as `hashed_password`) without a filtering schema.

## 7. Dependency injection

- `Depends()` resolves per request: DB session, current user, role checks, services.
- Use the `Annotated[T, Depends(fn)]` style and define reusable aliases (`DbSession`, `CurrentUser`).
- Use `yield` dependencies for setup/teardown (the DB session is opened, yielded, then closed), which is like Express middleware that runs code after `next()`.
- Tests replace dependencies through `app.dependency_overrides`.

## 8. SQLAlchemy 2 and PostgreSQL

- Use the **2.0 style only**: `DeclarativeBase`, `Mapped[...]`, `mapped_column()`, and `select()` statements. Do not use the legacy `session.query()`.
- Use one session per request through a dependency. Commit in the service or unit-of-work, not in the repository helpers.
- Use UUID primary keys (`uuid4` or DB-generated) and `created_at`/`updated_at` timestamps (`timestamptz`).
- Avoid N+1 queries with `selectinload` / `joinedload`. Explain the N+1 problem when it first appears.
- The sync vs async driver choice is an open decision (`TECH_DECISIONS.md`). Follow whatever is recorded there.
- Use parameterised queries only. Never build SQL with f-strings.

## 9. Alembic migrations

- Every schema change goes through a migration. Never call `Base.metadata.create_all()` in app code.
- Run `alembic revision --autogenerate -m "add candidates table"`, then **read and edit** the generated file, because autogenerate misses things (enums, pgvector types, server defaults, data migrations).
- Every migration must have a working `downgrade()`. Verify both: `alembic upgrade head`, `alembic downgrade -1`, `alembic upgrade head`.
- Never edit a migration that has been applied or shared. Create a new one.
- Update `docs/DATABASE_SCHEMA.md` (Proposed → Implemented).

## 10. JWT and RBAC

- Hash passwords with a maintained library (bcrypt/argon2 through `pwdlib` or `passlib`; choose in Phase 3 and record the choice). Never store plain text or use a fast hash.
- Use short-lived access tokens (about 15–30 minutes) and longer refresh tokens. The secret and algorithm come from settings or environment variables.
- Token claims are minimal: `sub` (user id), `role`, `exp`, `iat`, `type`. **No PII in the JWT.**
- RBAC uses a dependency factory, `require_role(...)`. Roles are defined in `docs/API_SPECIFICATION.md`.
- Return 401 for a missing or invalid token and 403 for an authenticated user without permission.

## 11. Exception handling

- Raise domain exceptions from services, and register handlers in `main.py` that map them to the standard error body.
- Use `HTTPException` only in routers or dependencies, never in services.
- Do not catch `Exception` broadly unless you log it and re-raise or convert it at a boundary.

## 12. Configuration management

- Use one `Settings(BaseSettings)` class in `app/core/config.py` that reads environment variables and `.env`. Load it once (`@lru_cache` getter) and inject it.
- `.env.example` is committed with placeholders only. `.env` is gitignored.
- No `os.getenv` calls scattered through the code.

## 13. Logging

- Use the standard `logging` module with a module-level `logger = logging.getLogger(__name__)`. Configure it once at startup.
- No `print()` in application code.
- Log events and IDs, not PII or resume text. Use `logger.exception` inside `except` blocks to keep tracebacks.
- Structured (JSON) logging can come in Phase 8 if needed.

## 14. Pytest

- Tests live in `backend/tests/`, mirroring the app structure. Shared fixtures go in `conftest.py`.
- Fixtures replace `beforeEach`. Use their scope (`function`, `session`) deliberately.
- Use `pytest.mark.parametrize` for input tables, and `pytest.raises` for exceptions.
- Async tests need `pytest-asyncio` or `anyio` (add it when the first async test needs it).
- Do not call the network in tests. Mock the LLM, embedding and external services.

---

## Reuse checks

Before writing new code, check for an existing `Settings` field, `deps.py` dependency, shared schema (pagination, error) or domain exception (see `project-development` §3).

## Restrictions

- No `session.query()` legacy API, no Pydantic v1 syntax and no `print()` debugging left in code.
- No secrets in code. No `create_all()` in place of migrations.
- No blocking I/O or CPU-heavy work inside `async def` handlers.
- No advanced abstractions without explanation and agreement.
