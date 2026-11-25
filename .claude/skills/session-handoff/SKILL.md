---
name: session-handoff
description: Keeps HireSense AI continuous across Claude Code sessions. Defines the exact session-start procedure (read the instructions and PROJECT_STATE, inspect Git and the real implementation, identify the next task) and the session-end procedure (record work, files, commands and real test results, issues and the exact next step in docs/PROJECT_STATE.md and docs/LEARNING_LOG.md). Use it at the start of every session, when the developer says "resume", "continue", "where were we", "wrap up" or "end session", and after any meaningful unit of work.
---

# Session Handoff Skill — HireSense AI

The aim: **a new session can continue from the docs alone**, without the developer re-explaining the project, and with every claim verified against the repository.

## When to activate

- At the start of every session (or when the developer says "resume", "continue" or "what's next")
- At the end of a session, or after any meaningful unit of work ("wrap up", "handoff", "end session")
- Before switching phases

---

## A. Session start

Do these in order and report the findings briefly.

1. **Read the instructions:** `CLAUDE.md`, then `docs/PROJECT_STATE.md` (focus on the current phase, the *Next recommended task*, Known issues and Blockers).
2. **Check Git:**
   ```bash
   git status
   git branch --show-current
   git log --oneline -10
   git stash list
   ```
   Note any uncommitted changes, especially ones not mentioned in `PROJECT_STATE.md`.
3. **Verify the real implementation status.** For each item marked done in the current and previous phase, confirm that the files exist. Where cheap, run the tests (`cd backend && pytest -q`) or the app. **Treat the docs as claims to verify, not facts.**
4. **Reconcile.** If the docs and the repository disagree, the repository wins. Report the mismatch, and fix the docs as part of this session's end procedure.
5. **Read the context:** the relevant `TECH_DECISIONS.md` entries and the latest `LEARNING_LOG.md` entry (revision topics, pending exercises).
6. **Identify:** completed tasks, incomplete tasks, and the next logical task within the **current phase**.
7. **Confirm with the developer** before starting:
   > "Current phase: X. Verified: … Mismatches: … Pending exercise: … Proposed next task: … Proceed?"

Do not write code before step 7, unless the developer has already given a specific task (then still do steps 1–4).

## B. Session end

1. **Summarise the work completed**, in specific outcomes, not intentions.
2. **Record the modified files** (`git status --short` / `git diff --stat`).
3. **Record the commands and tests actually executed**, with their real outcomes (for example `pytest -q → 12 passed, 1 failed (test_x)`). If nothing was run, write "Not run".
4. **Record known issues**: bugs, TODOs, flaky behaviour and technical debt.
5. **Record incomplete work**: what is half-done, and where (file and function).
6. **Record the exact next step**: one concrete, actionable task (for example "Implement `extract_text_from_docx()` in `backend/app/modules/resumes/extractors.py`; tests are already in `tests/resumes/test_extractors.py`").
7. **Update `docs/PROJECT_STATE.md`**: the phase status, the checklists, *Last verified state*, *Verification results*, *Next recommended task*, and the session history entry.
8. **Update `docs/LEARNING_LOG.md`** if learning happened (follow the `learning-mentor` evidence rules).
9. Update `TECH_DECISIONS.md`, `DATABASE_SCHEMA.md`, `API_SPECIFICATION.md` and `ARCHITECTURE.md` **only if** they changed.
10. Remind the developer of any uncommitted changes, and suggest a commit message. Do not commit unless asked.

### Session history entry template (in `PROJECT_STATE.md`)

```markdown
### YYYY-MM-DD — Phase N — <short title>
- **Done:** …
- **Files changed:** …
- **Commands run / results:** `…` → …   (or "Not run")
- **Known issues:** …
- **Incomplete:** …
- **Next step:** …
```

---

## Integrity rules

- **Never invent progress, files or test results.** Any test you did not run is recorded as "Not run".
- Never mark a task complete because it was discussed, planned or partly written.
- Use absolute dates (YYYY-MM-DD), not "yesterday".
- Keep `PROJECT_STATE.md` current rather than growing forever. Summarise old session entries once a phase is closed (keep the last ~5 detailed entries).

## Restrictions

- Do not skip Git and repository inspection at session start.
- Do not start the next phase without verifying the current phase's deliverables and getting the developer's approval.
- Do not rewrite another session's history entries, apart from summarising entries from closed phases.
