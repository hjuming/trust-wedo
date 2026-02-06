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

## [0.4.0] - 2026-02-06

### Added
- Diff Analysis: New `tw diff` command to compare AFB answers with AI captures.
- Similarity Calculation: Integrated `difflib.SequenceMatcher` for calculating similarity scores.
- Hallucination Risk Detection: Basic logic to identify low, medium, and high risk based on similarity.
- Diff Schema: Defined `schemas/diff.schema.json` for analysis reports.
- Comprehensive Analysis Reports: Aggregate comparisons across multiple AI sources (e.g., best/worst source).

### Changed
- CLI: Integrated `tw diff` and updated `schema_validator` to support new schemas.
- Meta: All diff reports include standard metadata.

## [0.3.0] - 2026-02-06

### Added
- AI Capture: New `tw capture` command to manually record AI outputs for specific AFBs.
- Capture Schema: Defined `schemas/capture.schema.json` to store AI responses and metadata.
- Incremental IDs: Automatically assigns unique, ordered IDs to captures (e.g., `cap:001`).
- Metadata Integration: Captures now track source, timestamp, and tool version.

### Changed
- CLI: Expanded CLI with capture capabilities and validation.
- Pipeline: Content → AFB → Capture flow is now fully operational.

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
