# DATABASE_SCHEMA — HireSense AI

> **Every table below is PROPOSED. No table is implemented.** No database, migration or model exists yet (verified 2026-11-25).
> When a table is created through an Alembic migration, move it to **§1 Implemented schema**, with its migration ID and phase. Keep the proposed section for what remains.

## 1. Implemented schema

_None yet._

| Table | Migration | Phase | Notes |
|---|---|---|---|
| — | — | — | — |

---

## 2. Proposed schema

Conventions: `id UUID PK`; `created_at` / `updated_at timestamptz NOT NULL DEFAULT now()`; `snake_case`; plural table names; every FK is indexed.

### 2.1 `users` (Phase 3)
| Column | Type | Constraints |
|---|---|---|
| id | uuid | PK |
| email | varchar(255) | UNIQUE, NOT NULL (stored lower-case) |
| hashed_password | varchar(255) | NOT NULL |
| full_name | varchar(150) | NOT NULL |
| role | enum `user_role` (`admin`, `recruiter`, `viewer`) | NOT NULL, default `recruiter` |
| is_active | boolean | NOT NULL, default true |
| created_at, updated_at | timestamptz | |

### 2.2 `job_descriptions` (Phase 2 in memory → Phase 3 DB)
| Column | Type | Constraints |
|---|---|---|
| id | uuid | PK |
| title | varchar(200) | NOT NULL |
| description | text | NOT NULL |
| location | varchar(150) | NULL |
| employment_type | enum (`full_time`, `part_time`, `contract`, `internship`) | NULL |
| min_experience_years / max_experience_years | numeric(4,1) | NULL, CHECK min ≤ max |
| status | enum (`draft`, `open`, `closed`) | NOT NULL, default `draft` |
| created_by | uuid | FK → users.id, NOT NULL |
| created_at, updated_at | timestamptz | |

### 2.3 `skills` (Phase 4)
| Column | Type | Constraints |
|---|---|---|
| id | uuid | PK |
| name | varchar(100) | NOT NULL (display form, e.g. "Node.js") |
| normalized_name | varchar(100) | UNIQUE, NOT NULL (e.g. "nodejs") |

### 2.4 `job_skills` (Phase 4 — depends on `skills`)
| Column | Type | Constraints |
|---|---|---|
| job_id | uuid | FK → job_descriptions.id ON DELETE CASCADE |
| skill_id | uuid | FK → skills.id |
| importance | enum (`required`, `preferred`) | NOT NULL |
| min_years | numeric(4,1) | NULL |
| | | PK (job_id, skill_id) |

### 2.5 `candidates` (Phase 3/4)
| Column | Type | Constraints |
|---|---|---|
| id | uuid | PK |
| full_name | varchar(150) | NOT NULL |
| email | varchar(255) | NULL, indexed (not unique: parsed data can be messy) |
| phone | varchar(30) | NULL |
| location | varchar(150) | NULL |
| current_title | varchar(150) | NULL |
| total_experience_years | numeric(4,1) | NULL |
| summary | text | NULL |
| created_by | uuid | FK → users.id |
| created_at, updated_at | timestamptz | |

_No protected attributes (gender, DOB/age, religion, caste, marital status, photo) are stored or derived._

### 2.6 `candidate_skills` (Phase 4)
| Column | Type | Constraints |
|---|---|---|
| candidate_id | uuid | FK → candidates.id ON DELETE CASCADE |
| skill_id | uuid | FK → skills.id |
| years | numeric(4,1) | NULL |
| source | enum (`parsed`, `manual`) | NOT NULL |
| | | PK (candidate_id, skill_id) |

### 2.7 `work_experiences` and `educations` (Phase 4)
- `work_experiences`: id, candidate_id FK (CASCADE), company, title, start_date, end_date NULL, is_current, description.
- `educations`: id, candidate_id FK (CASCADE), institution, degree, field_of_study, start_year, end_year.

### 2.8 `upload_batches` (Phase 4)
| Column | Type | Constraints |
|---|---|---|
| id | uuid | PK |
| created_by | uuid | FK → users.id |
| total_files / processed_count / failed_count | integer | NOT NULL, default 0 |
| status | enum (`pending`, `processing`, `completed`, `completed_with_errors`) | NOT NULL |
| created_at, updated_at | timestamptz | |

### 2.9 `resumes` (Phase 4)
| Column | Type | Constraints |
|---|---|---|
| id | uuid | PK |
| candidate_id | uuid | FK → candidates.id ON DELETE CASCADE, NULL until parsed |
| batch_id | uuid | FK → upload_batches.id, NULL for single uploads |
| original_filename | varchar(255) | NOT NULL |
| storage_path | varchar(500) | NOT NULL |
| mime_type | varchar(100) | NOT NULL |
| file_size_bytes | integer | NOT NULL |
| checksum_sha256 | char(64) | UNIQUE, NOT NULL (dedupe) |
| status | enum (`uploaded`, `processing`, `processed`, `failed`) | NOT NULL |
| error_message | text | NULL |
| page_count | integer | NULL |
| raw_text | text | NULL |
| uploaded_by | uuid | FK → users.id |
| processed_at | timestamptz | NULL |
| created_at, updated_at | timestamptz | |

### 2.10 `resume_chunks` (Phase 5)
| Column | Type | Constraints |
|---|---|---|
| id | uuid | PK |
| resume_id | uuid | FK → resumes.id ON DELETE CASCADE |
| candidate_id | uuid | FK → candidates.id ON DELETE CASCADE (denormalised for filtering) |
| chunk_index | integer | NOT NULL, UNIQUE (resume_id, chunk_index) |
| section | varchar(50) | NULL (experience, skills, education, projects, summary, other) |
| page_number | integer | NULL |
| content | text | NOT NULL |
| token_count | integer | NOT NULL |
| embedding | vector(384) | NOT NULL (the dimension depends on TD-007) |
| embedding_model | varchar(100) | NOT NULL |
| content_tsv | tsvector | generated from content (Phase 6 hybrid search) |
| metadata | jsonb | NULL |
| created_at | timestamptz | |

### 2.11 `match_results` (Phase 6)
| Column | Type | Constraints |
|---|---|---|
| id | uuid | PK |
| job_id | uuid | FK → job_descriptions.id ON DELETE CASCADE |
| candidate_id | uuid | FK → candidates.id ON DELETE CASCADE |
| overall_score | numeric(5,4) | NOT NULL, 0–1 |
| skill_score / experience_score / semantic_score | numeric(5,4) | NOT NULL |
| rerank_score | numeric(6,4) | NULL |
| explanation | jsonb | NOT NULL (matched/missing skills, evidence chunk IDs) |
| scoring_version | varchar(50) | NOT NULL (the weights and model config) |
| created_by | uuid | FK → users.id |
| created_at | timestamptz | |
| | | UNIQUE (job_id, candidate_id, scoring_version) |

### 2.12 `rag_queries` (Phase 5, audit)
id, user_id FK, question text, answer text, cited_chunk_ids uuid[], retrieved_chunk_ids uuid[], llm_model, latency_ms, prompt_tokens, completion_tokens, created_at.
_Stores synthetic content only during development. Review the retention policy before any real-data use._

---

## 3. Relationships

```
users 1─* job_descriptions, candidates(created_by), resumes(uploaded_by), upload_batches, match_results, rag_queries
upload_batches 1─* resumes
candidates 1─* resumes, work_experiences, educations, resume_chunks, match_results
candidates *─* skills (candidate_skills)
job_descriptions *─* skills (job_skills)
job_descriptions 1─* match_results
resumes 1─* resume_chunks
```

## 4. Proposed indexes

| Table | Index | Purpose |
|---|---|---|
| users | UNIQUE(email) | login |
| resumes | UNIQUE(checksum_sha256); (status); (candidate_id); (batch_id) | dedupe, worker queries, joins |
| candidates | (email); (total_experience_years); (location) | filters |
| candidate_skills / job_skills | (skill_id) | reverse lookups |
| resume_chunks | **HNSW (embedding vector_cosine_ops)** | semantic search |
| resume_chunks | GIN(content_tsv) | full-text / hybrid search |
| resume_chunks | (candidate_id); UNIQUE(resume_id, chunk_index) | filtering, integrity |
| match_results | UNIQUE(job_id, candidate_id, scoring_version); (job_id, overall_score DESC) | ranking per job |
| job_descriptions | (status); (created_by) | listing |

## 5. Open questions

- Multi-tenancy (organisations/teams) is **out of scope for v1**. Revisit before any real deployment.
- Store `raw_text` in `resumes` or in a separate table? Decide in Phase 4 based on query patterns.
- Soft delete vs hard delete for candidates (data-retention/consent requirements). Decide in Phase 4.
