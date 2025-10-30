# Changelog

Simple changelog for rag-architect project.

## Unreleased

### Added
- Document ingestion pipeline
  - API endpoint `/api/v1/ingestion/ingest`
  - Service layer with mock embeddings
  - In-memory repository
  - Tests for API and service

### Fixed
- MyPy errors in ingestion module
- Import paths and type annotations

### Changed
- Core improvements: logging, interfaces, config

## [0.1.0] - 2024-06-15

### Added
- Initial project setup with FastAPI
- Basic core modules and testing

[0.1.0]: https://github.com/kernelshard/rag-architect/releases/tag/v0.1.0