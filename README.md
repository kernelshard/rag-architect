# RAG Architect

A production-grade, educational backend system implementing a Retrieval-Augmented Generation (RAG) architecture using FastAPI, async I/O, and modular design. Each module is designed to teach backend architecture clarity and reasoning — not just produce output.

## Current Phase: 3 — Implementation & Production

- Phase 1: Core scaffolding (config, logging, metrics)   ✅
- Phase 2: Ingestion pipeline (text → embeddings)         ✅
- Phase 3: Retrieval pipeline (query → top-k results)     ✅
- Phase 4: Generation chain integration                   ⏳
- Phase 5: Evaluation metrics and dashboards              ⏳
- Phase 6: Scaling, Docker, and CI/CD                     ⏳

**Goal:** Build a FAANG-grade RAG backend demonstrating clean architecture, dependency injection, observability, and testability.

## Architecture Overview

```
app/
├── core/
│   ├── config.py        # Environment config, BaseSettings
│   ├── constants.py     # App constants and defaults
│   ├── exceptions.py    # Custom exception types and handlers
│   ├── interfaces.py    # Abstract repository contracts
│   ├── logging.py       # structlog setup
│   ├── metrics.py       # Prometheus metrics and middleware
│   └── repositories.py  # Shared in-memory vector repository
├── ingestion/
│   ├── api.py           # /api/v1/ingestion/ingest endpoint
│   ├── service.py       # Handles embedding generation and persistence
│   ├── deps.py          # Dependency provider for shared repo
│   └── models.py        # Pydantic request/response models
├── retrieval/
│   ├── api.py           # /api/v1/retrieval/query endpoint
│   ├── service.py       # Executes vector similarity search
│   ├── deps.py          # Uses same global vector repo as ingestion
│   ├── repository.py    # InMemoryVectorRepo implementation
│   └── models.py        # RetrievalRequest and RetrievalResponse
├── api/
│   └── router.py        # /api/v1 router and /ping route
└── main.py              # App factory, middleware, metrics endpoint
```

## Key Ideas

1. **Async-first:** All services use async functions to avoid I/O blocking.
2. **Modular monolith pattern:** Code organized like microservices but deployed as one.
3. **Shared repository:** Ingestion and retrieval share the same in-memory vector store.
4. **Structured logging:** Via structlog.
5. **Prometheus metrics:** For observability.
6. **Deterministic mock embeddings:** For testing reproducibility.
7. **FastAPI dependency injection:** For repositories and services.

## Current Endpoints

- `GET /api/v1/ping`                # Health check
- `POST /api/v1/ingestion/ingest`   # Accepts document and stores embeddings
- `POST /api/v1/retrieval/query`    # Queries top-k similar documents
- `GET /metrics`                    # Prometheus metrics exposition

## Example Run

```bash
curl localhost:8000/api/v1/ping
# => {"status": "ok", "message": "pong"}

curl -X POST localhost:8000/api/v1/ingestion/ingest \
  -H "Content-Type: application/json" \
  -d '{"doc_id":"doc_1","text":"hello"}'
# => {"doc_id":"doc_1","status":"accepted","message":"Document accepted for ingestion."}

curl -X POST localhost:8000/api/v1/retrieval/query \
  -H "Content-Type: application/json" \
  -d '{"query":"hello"}'
# => {"query":"hello","results":[{"doc_id":"doc_1","score":0.791,"metadata":{}}]}

curl localhost:8000/metrics
# => Prometheus metrics (including app_requests_total)
```

## Design Principles

- **One repo, one truth:** Ingestion and retrieval share the same in-memory object.
- **Every code file doubles as documentation.**
- **Logs explain intent, not just execution.**
- **Commits represent complete, single thoughts.**
- **Metrics measure what matters: latency and throughput.**

## Next Steps

1. Add retrieval and ingestion integration tests under `tests/`
2. Implement generation chain (Phase 4)
3. Add recall@k and faithfulness evaluation (Phase 5)
4. Docker + CI/CD setup (Phase 6)
5. Optional: Hybrid retrieval and re-ranking (Phase 7)
