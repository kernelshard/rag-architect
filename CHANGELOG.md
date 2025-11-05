# Changelog

Simple changelog for rag-architect project.

## Unreleased

## [0.2.0] - 2025-11-05

### Added
- Document ingestion pipeline
  - API endpoint `/api/v1/ingestion/ingest`
  - Service layer with mock embeddings
  - In-memory repository
  - Tests for API and service
- Document retrieval service
  - API endpoint `/api/v1/retrieval/query`
  - Vector search with cosine similarity
  - Shared vector repository between ingestion and retrieval
  - Comprehensive test coverage for retrieval functionality

### Fixed
- MyPy errors in ingestion module
- Import paths and type annotations

### Changed
- Core improvements: logging, interfaces, config
- Updated SearchResult to use dataclass with optional metadata
- Enhanced metrics with app name tagging

## [0.1.0] - 2024-06-15

### Added
- Initial project setup with FastAPI
- Basic core modules and testing

[0.2.0]: https://github.com/kernelshard/rag-architect/releases/tag/v0.2.0
[0.1.0]: https://github.com/kernelshard/rag-architect/releases/tag/v0.1.0