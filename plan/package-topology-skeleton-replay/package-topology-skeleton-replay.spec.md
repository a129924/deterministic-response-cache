# package-topology-skeleton-replay Specification

## Acceptance Criteria

1. The five fixed BC directories each contain a `.gitkeep`, and no other new path is created below `src/deterministic_response_cache/`.
2. No fixed BC directory contains `__init__.py`, any `.py` source, or a `cache_store/` directory.
3. Architecture prose and visual surfaces use the same five names, directory mapping, topology-only meaning, boundaries, and Identity-first evolution order.
4. Root package import behavior remains unchanged.

## Behavioral Scenarios

### Scenario 1: inspect reserved BC topology

- **Given** the topic implementation subject is checked out.
- **When** a maintainer lists `src/deterministic_response_cache/`.
- **Then** the five fixed BC directories are present only as `.gitkeep` reservations and cannot be interpreted as implemented child packages.

### Scenario 2: inspect architecture source of truth

- **Given** the updated architecture documents and visual scene are checked out.
- **When** a maintainer follows the documented BC order.
- **Then** Identity precedes Response Reuse, and CacheStore is shown only inside Response Reuse.

### Scenario 3: retain the baseline package import

- **Given** the reserved directories exist.
- **When** `import deterministic_response_cache` runs.
- **Then** the existing root package import succeeds unchanged. The child directories remain topology-only reservations: their BCs are neither implemented nor usable, and they add no executable Python module, public symbol, or re-export.

## Error / Edge Cases

- A proposed `cache_store/` directory, child `__init__.py`, Python source file, dynamic import, or public API is scope drift and must fail plan alignment.
- Any document or visual label that continues to name Response Reuse as the first implementation topic is an architecture-order conflict and must be corrected in the declared implementation subject.
- Any implementation change outside the ten declared paths requires return to Planner before it is written.
