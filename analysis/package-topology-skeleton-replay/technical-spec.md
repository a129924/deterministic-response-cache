# package-topology-skeleton-replay — Technical Specification

## Fixed topology

| BC | Fixed directory | Status in this topic |
| --- | --- | --- |
| Identity | `src/deterministic_response_cache/identity/` | topology only |
| Response Reuse | `src/deterministic_response_cache/response_reuse/` | topology only |
| Loaded Runtime Cache | `src/deterministic_response_cache/loaded_runtime_cache/` | topology only |
| Model Execution | `src/deterministic_response_cache/model_execution/` | topology only |
| Provider Adapter | `src/deterministic_response_cache/provider_adapter/` | topology only |

Each fixed directory contains exactly one `.gitkeep` created by this topic. No child package marker, executable Python source, public symbol, or re-export is created.

## Documentation alignment

The implementation subject updates these authoritative and synchronized architecture surfaces:

1. `docs/business-capability-architecture.md` is the text source of truth for the BC-to-directory mapping and topology-only meaning.
2. `docs/evolution-roadmap.md` fixes the ordered implementation sequence and removes its conflicting Response-Reuse-first statement.
3. `docs/architecture/business-capability/architecture-brief.md` synchronizes the map, topology-only status, boundaries, and Identity-first sequence.
4. `docs/architecture/business-capability/scene.js` and `docs/architecture/business-capability/index.html` synchronize the visual labels so Identity is the first future implementation topic and Response Reuse is second.

## Preserved boundaries

- Identity alone establishes model identity and complete request identity.
- Response Reuse consumes confirmed identity; CacheStore remains its future internal component.
- Loaded Runtime Cache owns neither response storage nor identity policy.
- Model Execution owns neither identity nor reuse policy.
- `provider_adapter/` reserves the BC's topology and contract location only; concrete local or remote provider integrations remain outside the core library and replaceable.
