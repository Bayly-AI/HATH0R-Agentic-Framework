# Archive — frozen pre-migration provenance

This tree holds **verbatim pre-migration Markdown** captured when the corpus was imported into OpenSource HATHOR.

## Policy

| Concern | Live `docs/**` | `archive/**` |
|---|---|---|
| Document IDs | **`HATHOR-*`** (public OpenSource namespace) | **`AEGIS-*`** retained (private-era snapshot) |
| Mutability | Active corpus; edited under change control | **Frozen** — do not rewrite IDs or bodies |
| Purpose | Authoritative current documentation | Provenance / diff baseline / audit |

## Why AEGIS IDs remain here

The archived files are a historical snapshot from the private AEGIS-era corpus. They intentionally keep original `AEGIS-*` document IDs and wording so SHA-256 manifests stay valid and the migration is reconstructable.

Live OpenSource docs were remapped to `HATHOR-*` (see `docs/architect/id-namespace-map-20260915.json`). **Do not “fix” archive IDs.**

## Manifest

- Human: [`MANIFEST.md`](./MANIFEST.md)
- Machine: [`MANIFEST.json`](./MANIFEST.json)

Each row links archived path → live counterpart path + content hash of the **pre-migration** bytes.

## Authority

- OpenSource documentation framework: **`HATHOR-CANON-001`**
- Historical private documentation framework import (live copy): **`HATHOR-CANON-012`** (was AEGIS-CANON-003)
- Archive itself is not a second source of truth for current product behavior.
