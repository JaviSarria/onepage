# Project Engineering Standards & Agent Guidelines

Monorepo fullstack: FastAPI (Backend) + Vue 3 (Frontend).  
Core philosophy: Clean Architecture, strict typing, deterministic testing, and zero coupling between domain logic and frameworks.

---

## Stack & Tooling

| Scope | Technology | Notes & Constraints |
|---|---|---|
| **Backend Runtime** | Python 3.12+ via `uv` | Dependency resolution and virtualenvs managed strictly via `uv` (`uv pip`, `uv run`). |
| **Backend Framework** | FastAPI + Pydantic v2 | Used purely as HTTP/Delivery layer; no business logic in route handlers. |
| **Data & ORM** | PostgreSQL + SQLAlchemy 2.0 (async) / Alembic | Migrations versioned with Alembic. Explicit repository patterns. |
| **Data Processing** | Pandas / Polars | Isolated to analytics/ETL application services. Vectorized operations only; no raw loops over DataFrames. |
| **Backend Testing** | Pytest, pytest-asyncio, factory-boy | TDD approach: Domain unit tests (fast, no DB) + Integration tests (isolated test DB). |
| **Frontend Runtime** | Node.js (LTS), Vite, pnpm/npm | Fast HMR, script setup, strict ESM. |
| **Frontend Framework**| Vue 3 (Composition API, `<script setup>`) + TypeScript | Strict typing (`strict: true`), Pinia for state, Vue Router. |
| **Frontend Testing** | Vitest + Vue Test Utils + Playwright | Unit/Component testing with Vitest; E2E flows with Playwright. |
| **VCS & Style** | Git, Ruff (Python), ESLint + Prettier (Vue) | Conventional Commits only. CI must pass before merging. |

---

## Architecture & Directory Structure

Enforce Screaming & Clean Architecture. The dependency rule is absolute: **Inner layers (Domain) never know about outer layers (FastAPI, SQLAlchemy, Vue UI, external APIs).**

```text
├── backend/
│   ├── src/
│   │   ├── domain/              # Enterprise Business Rules (Entities, Value Objects, Domain Exceptions)
│   │   │   └── models/          # Pure Python dataclasses or Pydantic models (NO ORM imports)
│   │   ├── application/         # Application Business Rules (Use Cases, DTOs, Ports/Interfaces)
│   │   │   ├── use_cases/       # 1 class/function per use case (e.g., RegisterUserUseCase)
│   │   │   └── interfaces/      # Protocols/Abstract repositories (e.g., UserRepository)
│   │   └── infrastructure/      # Frameworks, Drivers, Tools
│   │       ├── api/             # FastAPI routers, middleware, dependency injection
│   │       ├── database/        # SQLAlchemy models, sessions, migrations (Alembic)
│   │       ├── repositories/    # Concrete implementations of application interfaces
│   │       └── analytics/       # Pandas-based processing engines
│   └── tests/
│       ├── unit/                # Domain and pure use-case tests (zero I/O, fast)
│       └── integration/         # API routes, repository queries against test DB
│
├── frontend/
│   ├── src/
│   │   ├── core/                # Shared utilities, HTTP client (Axios/Ky), API interceptors
│   │   ├── modules/             # Feature-sliced modules (e.g., auth, reports, dashboard)
│   │   │   ├── domain/          # Frontend domain models, types, and business validation
│   │   │   ├── services/        # API communication adapters
│   │   │   ├── stores/          # Pinia stores (state orchestration only)
│   │   │   └── views/           # Page-level smart views
│   │   └── components/          # Reusable dumb/presentational UI components
│   └── tests/
│       ├── unit/                # Component & store tests (Vitest)
│       └── e2e/                 # User journeys (Playwright)
```

---

## Backend Rules (Python / FastAPI / uv)

### 1. Dependency Injection: 
- Use FastAPI's `Depends` only at the presentation boundary to inject Use Cases initialized with concrete Infrastructure Repositories.
### 2. Persistence Independence:
- SQLAlchemy models are NOT Domain models. Map ORM models to Domain Entities inside repositories.
- Never expose raw DB models in API schemas; always return Pydantic DTOs defined in the application layer.
### 3. Data Analysis with Pandas:
- Isolate Pandas logic into dedicated services/adapters.
- Avoid mutating DataFrames in place; favor method chaining and vectorized functions. Always enforce explicit schema/dtypes when loading data.
### 4. Error Handling:
- Domain errors inherit from a custom `DomainException`.
- Global exception handlers in FastAPI map domain exceptions to specific HTTP status codes. No raw 500s or leaking stack traces.
### 5. Commands:
- Add dependency: `uv add <package>`
- Run linter/formatter: `uv run ruff check . --fix && uv run ruff format .`
- Run tests: `uv run pytest`
- Run migrations: `uv run alembic upgrade head`

---

## Frontend Rules (Vue 3 / TypeScript / Node)

### 1. Composition API & Script Setup:
- Every component must use `<script setup lang="ts">`.
- Complex logic must be extracted into composables (`useFeature()`) following Single Responsibility.
### 2. Container / Presentational Pattern:
- `views/`: Smart components that connect to stores/composables, handle routing, and pass data down.
- `components/`: Pure presentational components receiving `props` and emitting `events`. Zero direct API or store coupling.
### 3. Typing:
- No `any` or untyped API payloads. Define shared DTO interfaces matching backend contracts.
### 4. State Management:
- Pinia stores must remain thin: hold state, getters, and basic actions calling API services. Do not put presentation UI state in global stores.
### 5. Commands:
- Install dependencies: `npm install` (or `pnpm install`)
- Typecheck: `npm run type-check`
- Run unit tests: `npm run test:unit`
- Run build: `npm run build`

---

## Testing Contract

- **Backend Rule**: No PR/feature is accepted without tests.
  - Domain Use Cases must have unit tests with mocked interfaces.
  - Endpoints must have integration tests verifying response status, payloads, and transactional rollback.
- **Frontend Rule**:
  - Test business composables and critical user interactions (emits, conditional renders).
- **Execution**: All automated tests must run isolated in CI with non-interactive, reproducible commands.

---

## Git & Workflow Standards

- **Branching**: `feat/<short-name>`, `fix/<short-name>`, `refactor/<short-name>`.
- **Commit Format**: Conventional Commits standard (`feat: ...`, `fix: ...`, `refactor: ...`, `test: ...`, `docs: ...`).
- **Forbidden**:
  - Never commit credentials, `.env` files, or local virtualenvs (`.venv/`, `node_modules/`).
  - Never bypass linters or typechecks with suppression comments (`# type: ignore`, `@ts-ignore`) without a linked issue and documented reason.

---

## Docker & Containerization Standards

The project must run deterministically across all environments via Docker and Compose. Containers are production-parity representations; local development must mirror CI/Production constraints.

### 1. Structure & Layout

```text
├── docker/
│   ├── backend/
│   │   ├── Dockerfile
│   │   └── Dockerfile.dev
│   └── frontend/
│       ├── Dockerfile
│       ├── Dockerfile.dev
│       └── nginx.conf           # Production SPA routing (fallback to index.html)
├── docker-compose.yml           # Base / Local development orchestration
└── docker-compose.override.yml  # Local overrides (volume mounts, dev tools - gitignored)
```

### 2. Image Build Rules (Best Practices)
#### 1. Multi-Stage Builds:
- Backend: Use a builder stage to resolve dependencies via uv, then copy only the installed virtualenv into a lean python:3.12-slim final image.
- Frontend: Stage 1 builds the static assets via Node/Vite (npm run build). Stage 2 serves the artifacts via an optimized, non-root nginx:alpine image.
#### 2. Security & Least Privilege:
- Never run containers as root. Define and use a non-root user (USER appuser / USER nginx).
- Do not bake credentials, .env files, or local artifacts (.venv, node_modules, dist/) into images. Enforce strict .dockerignore files for both backend and frontend.
#### 3. Layer Caching:
- Copy dependency manifests (pyproject.toml, uv.lock, package.json, pnpm-lock.yaml) and install dependencies before copying application source code.
#### 4. Healthchecks:
- Every stateful service (Postgres) and API service must expose an explicit HEALTHCHECK directive in compose/Dockerfile (e.g., querying /health or pg_isready).

### 3. Compose Orchestration Standards
- Service Separation: Separate concerns clearly (backend, frontend, db, and optional migration-runner).
- Startup Order: Use depends_on with condition: service_healthy so backend services do not attempt to connect to the database before it is accepting connections.
- Data Persistence: Always use named volumes for database persistence (e.g., postgres_data:/var/lib/postgresql/data). Never bind-mount database directories on host machines.
- Environment Variables: Use .env.example as the source of truth for required configuration. Compose must read from local .env.

### 4. Container Commands Reference
| Action | Command |
|---|---|
| Start full stack (detached) | docker compose up -d |
| View combined logs | docker compose logs -f |
| View service logs | docker compose logs -f backend |
| Run migrations inside container | docker compose exec backend uv run alembic upgrade head |
| Run backend tests inside container | docker compose exec backend uv run pytest |
| Rebuild without cache | docker compose build --no-cache |
| Stop and remove volumes (clean reset) | docker compose down -v |
