# AEGIS-ADR-004 — Layout & State Residency

- **Document ID:** AEGIS-ADR-004
- **Status:** ACCEPTED — operator sign-off 2026-09-13 (PENDING-EDITS D2)
- **Date:** 2026-09-13
- **Author:** Oz (Agent), commissioned by Raymond Bayly (BaylyAI)
- **Amends:** AEGIS-REQ-CORE-001 §7.1, `AEG-REQ-CNT-003`; AEGIS-RP-003 §3.1; AEGIS-ADR-001 (repo section, `.ai/aegis` reference); containerization article/presentation (port-registry references)
- **Resolves findings:** E7 (three port-registry paths), E8 (spool residency ambiguity), E9 (stale `.ai/aegis` references), G8 (OS scope)
- **Scope rule:** decision record only. No implementation authorized by this document.

RFC 2119 keywords apply.

---

## 1. Context

Four layout/residency facts are stated differently across the corpus:

1. **Port registry path.** `AEG-REQ-CNT-003` says `.aegis/cfg/port-registry.yaml`; the Universal Project Layout (CORE §7.1) has no `.aegis/cfg/` and places `cfg/` at the repo root; the containerization article/presentation cite the InfraOS legacy `cfg/gen3-port-registry.yaml`.
2. **Telemetry spool residency.** RP-003 §3.1 places the spool under the *machine* AEGIS state dir; CORE §7.1, ARCH-001 §11, and TS-001 §2.3 place it at *project* `.aegis/state/spool/` (CORE carries a "per-machine variant may relocate" hedge). Observation-Bot's drain model differs materially between the two.
3. **Legacy layout label.** ADR-001's repo section and the CLI Research Report §1.7 still reference the outline's `.ai/aegis` layout; CORE canonicalized `.aegis/`.
4. **OS scope.** TS-001 relies on `flock`, XDG paths, and TTY semantics, and PLAN-002 CI targets mac/linux — while `ml-path-case` implies Windows relevance. No document states v1 platform support.

## 2. Decisions

### 2.1 D1 — Canonical port-registry path: `cfg/port-registry.yaml` (repo root)

The canonical registry-first identity file lives at **`<project>/cfg/port-registry.yaml`**.

- Rationale: `cfg/` is the UPL's home for "configuration not required at repo root"; the port registry is *deploy configuration consumed by humans, Compose, and linters* — not AEGIS runtime metadata/state, which is what `.aegis/` holds. `.aegis/cfg/` is not added to the UPL.
- `ml-port-registry` and `AEG-REQ-CNT-003` reference this path. Org-central registries (the InfraControl `gen3-port-registry.yaml` pattern) remain valid as an *organization-tier* source the project file must not contradict; the containerization article's references are annotated as InfraOS-legacy examples.

### 2.2 D2 — Telemetry spool residency: project-tier canonical, machine-indexed

The canonical spool location is **project-tier**: `<project>/.aegis/state/spool/` (as UPL, ARCH-001 §11, and TS-001 §2.3 already specify). RP-003 §3.1's machine-dir phrasing is amended.

- Rationale: TS-001/TS-002 are already built on the project spool; run artifacts (`findings/evidence/assumptions/events`) co-locate with their spool; Class C containers mount one run dir (TS-001 §14) without needing machine-dir access.
- **Machine index of spools:** the MBI-lite index (`${XDG_DATA_HOME:-~/.local/share}/aegis/index/`) additionally records active project roots, so a resident Observation-Bot drains N project spools from one machine-level discovery point. Cursor state is per-spool.
- **Non-project context fallback:** commands executed outside any `.aegis/` project (e.g. `aegis version` in `$HOME`) spool to `${XDG_STATE_HOME:-~/.local/state}/aegis/spool/`. This is the *only* machine-tier spool and is drained through the same index.
- Interaction with CORE §17 Q5 (cross-project MBI scope): this decision fixes the *spool* side (project-owned, machine-indexed); the MBI scope question itself remains open and is narrowed accordingly.

### 2.3 D3 — `.ai/aegis` cleanup directive

`.aegis/` is the sole canonical hidden metadata folder. All remaining `.ai/aegis` references (ADR-001 repo section; CLI Research Report §1.7) are annotated as *outline-era labels* superseded by CORE §7.1. `aegis repo init --from-infraos` remains the only sanctioned migration tool; no `.ai/` compatibility path is introduced.

### 2.4 D4 — v1 OS scope: macOS + Linux

AEGIS v1 supports **macOS and Linux** (darwin/arm64+amd64, linux/arm64+amd64). Windows is explicitly out of scope for v1 and revisited for v2.

- `flock`, XDG-style paths, and POSIX TTY semantics MAY therefore be relied on in v1 specs without Windows shims.
- `ml-path-case` is retained despite the scope: it protects case-insensitive filesystems (macOS default) today and future Windows consumers of the *repos* AEGIS governs, which is independent of where the CLI runs.
- CI matrices (PLAN-002 CVS-X-E1 and successors) are correct as mac/linux and now match a stated requirement rather than an accident.

## 3. Consequences

- **Positive:** one path per fact; the Observation-Bot drain model is specified; OS assumptions in TS-001/TS-002 become legitimate rather than implicit.
- **Negative:** RP-003 §3.1 requires a wording amendment (project spool + machine index) — tracked in `PENDING-EDITS.md`; containerization article/presentation require path annotations.
- **Edits queued:** CORE §7.1 (note port-registry location under `cfg/`), `AEG-REQ-CNT-003` path, RP-003 §3.1, ADR-001 repo note, CLI Research Report §1.7 annotation, containerization docs, new OS-scope line in CORE §1.1/§15.

## 4. Alternatives considered

| Alternative | Why rejected |
|---|---|
| `.aegis/cfg/port-registry.yaml` (as CNT-003 wrote) | Adds a config subtree to a metadata/state folder; UPL keeps human-edited config in `cfg/`; linters and Compose read it without touching `.aegis/` |
| Machine-tier spool as canonical (as RP-003 wrote) | Breaks container run-dir mounting; splits run artifacts from their telemetry; TS-001/002 already implemented against project spool |
| Per-project *and* per-machine dual spool | Two sources of truth for the same events; violates the corpus's own "status-on-record, one store" doctrine |
| Windows in v1 scope | flock/TTY/XDG assumptions permeate TS-001/002; cost lands on the critical path with no current consumer |

---

*Decision record — ACCEPTED 2026-09-13. No implementation authorized by this document.*
