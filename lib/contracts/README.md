# HATHOR machine-readable contracts

This directory holds **canonical, machine-readable contracts** owned by the
HATHOR Agentic Framework. Downstream products (CLI, POC, adapters) consume
these artifacts as the source of truth for shared behavior — they must not
fork or redefine the semantics here.

## Purpose

Prose in technical specs (for example HATHOR-TS-005) describes intent.
Contracts under `lib/contracts/` make that intent **executable**:

- CI and unit tests can assert exit/envelope/diagnostic agreement against a
  single YAML file instead of hard-coding tables.
- Adapters can map process results without re-interpreting docs.
- Versioned `schema` fields let consumers detect breaking vs additive changes.

## Artifacts

| File | Schema | Description |
|------|--------|-------------|
| `exit-codes.yaml` | `hath0r.cli.exit-codes/1` | CLI process exit codes 0–7, allowed envelope states, diagnostic-code mappings, and contract rules (HATHOR-TS-005 §6 / §14, HATHOR-REQ-002). |

## How consumers should reference these files

### CLI (`Bayly-AI/HATH0R-CLI`)

- Treat `exit-codes.yaml` as the authority for process exits and diagnostic
  code → exit class pairing.
- Load the file in tests (and optionally at runtime) from a pinned Framework
  revision or a vendored copy kept in lockstep with Framework releases.
- When implementing `--output` envelopes and the pytest suite, assert that
  every raised diagnostic code maps to the exit listed here, and that
  envelope `state` values are in the allowed `envelope_states` for that exit.
- Do not invent new public exit numbers without a Framework contract update.

### POC (`Bayly-AI/HATH0R-Agentic-POC`)

- Use this contract when normalizing CLI results: map `process.exit` +
  diagnostic code into POC-facing states using the same tables.
- Prefer reading the Framework artifact (or a released package that embeds it)
  over copying tables into POC source. If a local copy is required for offline
  builds, pin the Framework commit and document the sync path.

### Suggested load pattern

```python
from pathlib import Path
import yaml

contract = yaml.safe_load(
    Path("lib/contracts/exit-codes.yaml").read_text(encoding="utf-8")
)
assert contract["schema"] == "hath0r.cli.exit-codes/1"
by_code = {row["code"]: row for row in contract["exits"]}
```

Path resolution depends on how the consumer obtains Framework sources
(submodule, release tarball, installed package). Always resolve relative to
the Framework root, not the consumer repo root, unless you vendor the file.

## Versioning

- The `schema` field is the **major** contract identity
  (`hath0r.cli.exit-codes/1`).
- **Additive** changes (new optional fields, new diagnostic codes on an
  existing exit, clarifying notes) keep `/1` and bump `updated_at`.
- **Breaking** changes (renumbered exits, removed codes, changed meaning of an
  exit, incompatible rule changes) require a new major schema id
  (for example `hath0r.cli.exit-codes/2`) and coordinated consumer migration.
- Consumers should fail fast on an unrecognized `schema` rather than guessing.

## Authority and non-goals

- **Authority**: Framework repo (`Bayly-AI/HATH0R-Agentic-Framework`).
- **Derived from**: HATHOR-TS-005 §6 (process exits + rules), §14 (error /
  diagnostic table), and HATHOR-REQ-002 (HT-CLI-005).
- **Not in scope here**: JSON Schema for response envelopes (see
  `lib/schemas/` when published), CLI flag UX, or product-specific exit
  extensions beyond this table.
