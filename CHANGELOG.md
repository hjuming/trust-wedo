# Trust WEDO Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure
- Core documentation (README.md, PRODUCT.md, CLI.md, ACCEPTANCE_TESTS.md)
- JSON Schema definitions for all data structures
- Sample data files and expected outputs
- CLI framework with 6 core commands
- Python package configuration (pyproject.toml)

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A

---

## [0.2.0] - 2026-02-06

### Added
- Unified Metadata: All JSON outputs now include a `meta` block with `generated_at`, `tool_version`, and `input_source`.
- Unified Gate Behavior: `tw afb build` now produces a JSON with `eligibility: "fail"` instead of exiting when EC is low.
- Comprehensive Test Suite: Added unit tests for EC, CCS, Graph, and Report modules, plus integration tests for Gate behavior.
- Standards Compliance: All commands now strictly follow the v0.2 Engineering Decisions.

### Changed
- CLI: Updated `tw afb build` to handle low-trust entities by producing a failure AFB object.
- Scorer: Adjusted `EntityScorer` heuristics to be more consistent with MVP requirements.
- Core: Standardized module return values and metadata integration.

## [0.1.0] - 2026-02-06

### Added
- MVP release with basic CLI functionality
- Site scanning capability (Issue #1)
- Entity trust scoring (Issue #3)
- AFB generation (Issue #2)
- Citation evaluation (Issue #4)
- Entity graph and risk detection (Issue #5)
- Report generation (Issue #6)
