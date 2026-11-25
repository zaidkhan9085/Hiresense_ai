# API_SPECIFICATION — HireSense AI

> **All endpoints are PLANNED. None is implemented** (verified 2026-11-25).
> Status legend: 📝 Planned · 🚧 In progress · ✅ Implemented (with the phase and test file). Update the status when an endpoint is built.

## 1. Conventions

- Base path: `/api/v1`. JSON in and out (multipart for uploads).
- Auth: `Authorization: Bearer <access_token>` on every endpoint except health and auth login/register/refresh.
- IDs are UUIDs. Timestamps are ISO-8601 UTC.
- Pagination (list endpoints): `?page=1&page_size=20` (max 100) → `{ "items": [...], "total": n, "page": 1, "page_size": 20 }`.
- Status codes: 200 OK · 201 Created · 202 Accepted (async processing) · 204 No Content · 400/422 validation · 401 unauthenticated · 403 forbidden · 404 not found · 409 conflict (e.g. duplicate resume) · 413 payload too large · 429 rate limited · 500.
- **Standard error body:**
  ```json
  { "error": { "code": "CANDIDATE_NOT_FOUND", "message": "Candidate not found", "details": null } }
  ```

## 2. Roles (RBAC)

| Role | Permissions |
|---|---|
| `admin` | everything, including user management |
| `recruiter` | manage their jobs, upload resumes, view and search candidates, run matching and RAG |
| `viewer` | read-only: candidates, jobs, matches, analytics |

## 3. Endpoints

### Health
| Status | Method | Path | Auth | Phase | Notes |
|---|---|---|---|---|---|
| 📝 | GET | `/health` | none | 2 | `{status, version}`; DB/Redis checks are added later |

### Auth
| Status | Method | Path | Auth | Phase | Request → Response |
|---|---|---|---|---|---|
| 📝 | POST | `/auth/register` | none (or admin-only: decide in Phase 3) | 3 | `{email, password, full_name}` → 201 `UserRead` |
| 📝 | POST | `/auth/login` | none | 3 | `{email, password}` → `{access_token, refresh_token, token_type}` |
| 📝 | POST | `/auth/refresh` | refresh token | 3 | → new access token |
| 📝 | GET | `/auth/me` | any role | 3 | → `UserRead` (never includes the password hash) |

### Users (admin)
| Status | Method | Path | Auth | Phase | Notes |
|---|---|---|---|---|---|
| 📝 | GET | `/users` | admin | 3 | paginated `UserRead` |
| 📝 | PATCH | `/users/{user_id}` | admin | 3 | role / is_active |

### Job descriptions
| Status | Method | Path | Auth | Phase | Notes |
|---|---|---|---|---|---|
| 📝 | POST | `/job-descriptions` | recruiter, admin | 2 (memory) / 3 (DB) | `JobCreate` → 201 `JobRead` |
| 📝 | GET | `/job-descriptions` | any | 2/3 | filters: status, q |
| 📝 | GET | `/job-descriptions/{job_id}` | any | 2/3 | |
| 📝 | PATCH | `/job-descriptions/{job_id}` | owner recruiter, admin | 2/3 | `JobUpdate` |
| 📝 | DELETE | `/job-descriptions/{job_id}` | owner recruiter, admin | 2/3 | 204 |

### Resumes
| Status | Method | Path | Auth | Phase | Notes |
|---|---|---|---|---|---|
| 📝 | POST | `/resumes` | recruiter, admin | 4 | multipart `file` (PDF/DOCX, max ~5 MB) → 202 `{resume_id, status}`; 409 on a duplicate checksum |
| 📝 | POST | `/resumes/bulk` | recruiter, admin | 4 | multipart `files[]` (max ~50) → 202 `{batch_id, resumes:[{resume_id, filename, status}]}` |
| 📝 | GET | `/resumes/{resume_id}` | any | 4 | metadata + status + error_message |
| 📝 | GET | `/resumes/batches/{batch_id}` | any | 4 | batch progress counts |
| 📝 | GET | `/resumes` | any | 4 | filters: status, batch_id |
| 📝 | DELETE | `/resumes/{resume_id}` | recruiter, admin | 4 | deletes the file, the row and the chunks |

### Candidates
| Status | Method | Path | Auth | Phase | Notes |
|---|---|---|---|---|---|
| 📝 | GET | `/candidates` | any | 4 | filters: skills, min/max experience, location, q; paginated |
| 📝 | GET | `/candidates/{candidate_id}` | any | 4 | profile + skills + experience + education + resumes |
| 📝 | PATCH | `/candidates/{candidate_id}` | recruiter, admin | 4 | correct parsed fields |
| 📝 | DELETE | `/candidates/{candidate_id}` | admin | 4 | cascades |
| 📝 | POST | `/candidates/compare` | any | 6 | `{candidate_ids:[2–5], job_id?}` → side-by-side skills, experience, scores, cited evidence |

### Search
| Status | Method | Path | Auth | Phase | Notes |
|---|---|---|---|---|---|
| 📝 | POST | `/search/candidates` | any | 5 (semantic) / 6 (hybrid) | `{query, filters?, top_k?, mode: "semantic"\|"hybrid"}` → ranked candidates with `score` and `matched_chunks[]` |

### Matching
| Status | Method | Path | Auth | Phase | Notes |
|---|---|---|---|---|---|
| 📝 | POST | `/job-descriptions/{job_id}/matches` | recruiter, admin | 6 | runs matching (sync for small sets, 202 for large ones) |
| 📝 | GET | `/job-descriptions/{job_id}/matches` | any | 6 | ranked list; each item has `overall_score`, the component scores and a summary explanation |
| 📝 | GET | `/job-descriptions/{job_id}/matches/{candidate_id}` | any | 6 | full explanation: matched/missing skills, evidence chunks |

_Responses include the disclaimer field `"decision_support_only": true`._

### RAG Q&A
| Status | Method | Path | Auth | Phase | Notes |
|---|---|---|---|---|---|
| 📝 | POST | `/rag/ask` | any | 5 | `{question, candidate_ids?, job_id?, top_k?}` → `{answer, citations:[{chunk_id, resume_id, candidate_id, section, snippet}], retrieved_chunks:[...], model, latency_ms}`; when the context is insufficient, the answer says "not found in the provided resumes" |

### Analytics
| Status | Method | Path | Auth | Phase | Notes |
|---|---|---|---|---|---|
| 📝 | GET | `/analytics/overview` | any | 6 | counts: candidates, resumes by status, open jobs, matches |
| 📝 | GET | `/analytics/skills` | any | 6 | top skills in the pool; skill gaps against open jobs |
| 📝 | GET | `/analytics/pipeline` | any | 6 | upload/processing throughput and failure rates over time |

## 4. Non-functional requirements

- Upload limits (size, count, MIME) are configurable through settings.
- Rate limiting on auth and RAG endpoints (Phase 8).
- No PII in logs. LLM calls use synthetic data only during development.
