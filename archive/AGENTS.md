---
id: archive-subsystem
type: subsystem
title: Archive Subsystem
depends_on: [hath0r-framework]
governed_by: [CR-CLI-ENTRY-001, CR-RAG-RETRIEVAL-001, cr-branch-gov-001]
---
# Archive Subsystem — AGENTS Context

> **Subsystem Role:** Historical repository assets, legacy POC implementations, and historical migration artifacts preserved for provenance.

## 1. Operating Rules
- Files in `archive/` are read-only and preserved for historical reference and auditability.
- Do not import active runtime code from `archive/`. Active modules belong in `src/hath0r_engine/` or `lib/`.
- Query historical context via `hath0r kb` or `hath0r memory search`.
