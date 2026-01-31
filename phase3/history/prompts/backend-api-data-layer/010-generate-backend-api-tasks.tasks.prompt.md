---
id: 010
title: Generate Backend API Tasks
stage: tasks
date: 2026-01-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: backend-api-data-layer
branch: 001-backend-api-data-layer
user: Claude Code
command: /sp.tasks
labels: ["backend", "api", "tasks", "fastapi", "sqlmodel", "jwt"]
links:
  spec: /mnt/c/Users/NLN/Desktop/phase2/specs/001-backend-api-data-layer/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - /mnt/c/Users/NLN/Desktop/phase2/specs/001-backend-api-data-layer/tasks.md
tests:
 - /mnt/c/Users/NLN/Desktop/phase2/specs/001-backend-api-data-layer/tasks.md
---

## Prompt

# /sp.tasks – Spec 2 Backend (FastAPI + SQLModel + Neon)

Status: Planning / Early Implementation Phase
Last updated: Jan 2026

## Active / Pending Tasks (priority order)

1. Project bootstrap
   - backend/ folder structure
   - pyproject.toml + uv / poetry init
   - .env.example + .gitignore

2. Core dependencies
   fastapi uvicorn sqlmodel python-jose[cryptography] alembic psycopg[binary] python-dotenv pydantic-settings

3. Configuration & env loading
   - settings.py (pydantic Settings)
   - JWT_SECRET, DATABASE_URL, JWT_ALGORITHM=HS256

4. SQLModel Task model
   - models/task.py
   - fields: id, title, description?, completed, owner_id (str), created_at, updated_at

5. Alembic + initial migration
   - alembic init
   - env.py → use SQLModel metadata + async engine
   - Generate & apply Task table migration

6. JWT verification logic
   - auth/jwt.py → decode validate HS256 with secret
   - Handle expired / invalid → raise 401

7. Current user dependency
   - auth/dependencies.py
   - get_current_user() → Depends(HTTPBearer) → return str(user_id / sub)

8. Tasks APIRouter
   - routers/tasks.py
   - prefix = "/api/{user_id}/tasks"
   - all routes depend on current_user: str = Depends(get_current_user)

9. CRUD + complete endpoints (with strict ownership)
   - GET / → list (filter owner_id)
   - POST / → create (set owner_id = current_user)
   - GET /{id} → 404 if not owned
   - PUT /{id} → replace
   - PATCH /{id}/complete → set completed=True
   - DELETE /{id} → delete if owned

10. Pydantic schemas
    - TaskCreate, TaskUpdate, TaskRead (exclude owner_id in output)

11. Database session dependency
    - db.py → async sessionmaker + get_db()

12. Main app
    - main.py → FastAPI() + include_router + lifespan / engine setup

13. Error handling consistency
    - 401, 403, 404, 422 handlers
    - JSON {"detail": "..."}

14. README backend section
    - run command, env vars, JWT note

15. Optional smoke / integration test stubs
    - tests/ with TestClient + mock JWTs

## Completed / In Progress (mark when done)

- [ ] 1–3 (bootstrap + deps + config)
- [ ] 4–5 (model + migration)
- [ ] 6–7 (auth)
- [ ] 8–10 (router + endpoints + schemas)
- [ ] 11–13 (wiring + errors)
- [ ] 14–15 (docs + tests)

Next command examples:
  /sp.implement 1 2 3
  /sp.implement 4 5
  /sp.implement phase-auth   # = tasks 6–7
  /sp.implement tasks-router # = 8–10

## Response snapshot

Successfully generated comprehensive implementation tasks for the Backend API & Data Layer feature. The tasks.md file has been created with 50 individual tasks organized across 8 phases:

1. **Phase 1: Project Setup** (T001-T005) - Project structure and dependencies
2. **Phase 2: Configuration & Foundation** (T006-T010) - Settings, database connections, and models
3. **Phase 3: User Story 1 - Secure API Access** (T011-T016) - JWT authentication and validation
4. **Phase 4: User Story 2 - User-Specific Data Operations** (T017-T026) - CRUD operations with ownership enforcement
5. **Phase 5: User Story 3 - Data Persistence & Integrity** (T027-T032) - Database integrity and validation
6. **Phase 6: Error Handling & Response Consistency** (T033-T038) - Standardized error responses
7. **Phase 7: Main Application & Wiring** (T039-T044) - Main app integration
8. **Phase 8: Testing & Documentation** (T045-T050) - Tests and documentation

Tasks follow the required checklist format with sequential IDs (T001-T050), parallelization markers ([P]), and user story labels ([US1], [US2], [US3]). Dependencies are clearly defined between phases, and parallel execution opportunities are identified. The MVP scope includes Phases 1-4 for a working authenticated API.

## Outcome

- ✅ Impact: Complete task breakdown with 50 specific, actionable tasks organized by user story
- 🧪 Tests: Test tasks included in Phase 8 with contract, integration, and unit test specifications
- 📁 Files: tasks.md created with comprehensive task list following required format
- 🔁 Next prompts: Ready for implementation with /sp.implement commands
- 🧠 Reflection: Tasks organized by user story enabling independent implementation and testing

## Evaluation notes (flywheel)

- Failure modes observed: None - all tasks follow required format and dependencies are properly mapped
- Graders run and results (PASS/FAIL): PASS - all requirements met
- Prompt variant (if applicable): Standard task generation workflow
- Next experiment (smallest change to try): Begin implementation with Phase 1 tasks