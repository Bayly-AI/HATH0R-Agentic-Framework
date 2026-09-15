---
id: HATHOR-RP-013
title: HATHOR-RP-013 — Threat Model & Trust Boundaries
summary: RFC 2119 keywords apply. Requirements use prefix `AEG-THR-###`.
doc_type: RP
diataxis: explanation
audience: [architect, agent]
tags: []
version: 1.0.0
status: accepted
created: '2026-09-13'
updated: '2026-09-15'
owner: Raymond Bayly (BaylyAI)
review: {trust: unverified, reviewed_by: null, reviewed_at: null, interval: 180d, next_review: null}
stale: false
supersedes: []
superseded_by: null
amended_by: []
parent: null
sources: []
---
# HATHOR-RP-013 — Threat Model & Trust Boundaries

- **Document ID:** HATHOR-RP-013
- **Status:** ACCEPTED (design) — operator sign-off 2026-09-13 (PENDING-EDITS D5); §6 signing adoptions now applied to RP-001/RP-002; open questions tracked in §7
- **Date:** 2026-09-13
- **Author:** Oz (Agent), commissioned by Raymond Bayly (BaylyAI)
- **Companion to:** CORE §13 (SEC), RP-001/002 (signing/registry), RP-009/TS-002 (run log, waivers), RP-007/TS-001 (packs, redaction), RP-010 (identity issuance), RP-011 (brokering)
- **Amends (accepted 2026-09-13):** RP-001 §2 canonicalization (→ RFC 8785 JCS); RP-001 Q1 + RP-002 Q3 (→ TUF); TS-001 §8.6 waiver identity (→ signed human tokens, pulled forward) — all applied
- **Scope rule:** research and requirements only. No implementation authorized.

RFC 2119 keywords apply. Requirements use prefix `AEG-THR-###`.

---

## 1. Why this paper

The corpus has strong security *requirements* (SEC-001..006, zero-secret containers, human-only gates) but no enumerated adversaries. Two enforcement mechanisms in particular are weaker than their prose implies, and honesty about that is itself a security control.

## 2. Trust model v1 (normative statement)

> **AEGIS v1's mechanical guarantees hold against a *cooperative-but-fallible* agent** — one that drifts, forgets, reorders, hallucinates, or overclaims, but does not deliberately subvert the platform's local files. **A fully adversarial local process is *out of scope for v1 enforcement* and *in scope for v1 detection* (Tower-side cross-checks) and for the phased hardening in §4.**

This statement MUST appear wherever no-skip or human-only guarantees are claimed (CORE §14, RP-009 §7, TS-002 §9). Overstating the guarantee is a defect.

## 3. Adversaries & assets

| Adversary | Capability | Primary target assets |
|---|---|---|
| A1 Fallible agent (v1 focus) | reorders/skips/overclaims via normal CLI use | run integrity, claims, validation |
| A2 Malicious local process / subverted agent | arbitrary file writes in the workspace | `events.jsonl`, spool, ledgers, MBI cache |
| A3 Malicious repo content | config-driven code execution | `linters.yaml` argv, hooks, graph assets |
| A4 Compromised bot artifact | supply chain | manifests, images, packs |
| A5 Network adversary | MITM/replay on Tower/provider paths | key/CRL distribution, ingest |
| A6 Insider misusing authority | valid credentials, wrong intent | waivers, deploys, promotions |

## 4. Findings & mitigations

### 4.1 Run-log and spool forgery (A2) — the honest gap
`events.jsonl` and the telemetry spool are plain agent-writable files; "only Process-Bot appends `node.*`" is enforced only in-process. The finalize reconciler cross-checks two sources (TS-002 §9.1) — but both are locally writable, so **no-skip is provable against A1, not A2**.
**Mitigations (phased):** (P-now) §2 trust statement everywhere the guarantee is claimed. (P-hardening) *hash-chained run log*: each event carries `prev_hash`; segments periodically anchored by an HMAC whose key lives outside the workspace (machine keyring / Tower-issued), making silent insertion/deletion detectable at reconcile and Tower ingest. (P-tower) Tower-side executed-set attestation compares machine rollups against independent CI evidence where available.

### 4.2 Human-only waivers rest on TTY detection (A1/A2/A6) — pull the fix forward
TS-001 §8.6 derives `Actor.Kind=human` from "TTY + local profile" — trivially spoofable with a PTY. Waivers gate *mandatory* nodes and deploy-path graphs; this is the platform's weakest load-bearing control.
**Mitigation (v1, not "later"):** human-only operations (waive, deploy-ticket authoring authority, org-tier promotion) MUST present a **Tower-issued short-lived human identity token** (RP-010 §5/AEG-TWR-008), verified offline against distributed keys within TTL. TTY detection remains a UX hint only. This supersedes the "revisit later" stance of TS-001 open Q4.

### 4.3 Pack/graph supply chain (A3/A4)
`linters.yaml` executes repo-configured argv; graphs drive mandatory execution; adapters touch providers.
**Mitigations:** org-distributed linter packs, suites, graphs, and adapters MUST be signed and verified before load (extends RP-007 §7); repo-local unsigned packs run only under a dev profile with explicit `--allow-unsigned` (recorded on the run, surfaced degraded); subprocess linters get a no-network doctor probe in v1 and OS sandboxing (seccomp/sandbox-exec) as hardening (TS-001 Q5 lean confirmed).

### 4.4 Redaction strength (A1)
Regex-only secret matching under-detects. **Mitigation:** the redactor and `ml-secrets-diff` MUST combine pattern, entropy, and known-provider verifiers (gitleaks/trufflehog-class rulesets as a bundled pack); redaction remains defense-in-depth, never the only barrier.

### 4.5 Distribution & replay (A5)
Key/CRL/policy fetches and rollup ingest MUST be signed, versioned, and monotonic (a client refuses an older snapshot than it has seen — rollback protection). Covered structurally by TUF adoption (§6).

### 4.6 Adjacent boundaries fixed here
- **Out-of-proc bot transport (target):** when validators/bots leave the single binary (TS-001 §14 / TS-002 §13 seams), the transport is **mutually-authenticated local IPC (UDS) or mTLS within the Class A boundary** — never a public listener (`AEG-BOT-TAX-006` preserved). Named now so the seams have a target.
- **Concurrent conductors (TS-002 Q3):** optimistic append + fold-as-authority is accepted for v1; the fold MUST deterministically order same-run events (`event_id` time-order) and flag conflicting concurrent transitions as `degraded` for operator review.

## 5. Requirements (AEG-THR)

### AEG-THR-001 — Trust model stated where guarantees are claimed
The §2 statement MUST accompany every no-skip/human-only guarantee claim.
**AC:** CORE/RP-009/TS-002 carry the statement or a reference to it.

### AEG-THR-002 — Signed human identity for human-only operations
Waive/deploy-authority/org-promotion MUST verify a Tower-issued short-lived human token; TTY inference alone is insufficient.
**AC:** PTY-spoof test fails to waive; waiver records carry token references.

### AEG-THR-003 — Hash-chained run log (hardening phase)
The run event log MUST support hash chaining with an externally-held anchor key; reconcile and ingest verify chain integrity.
**AC:** Silent event insertion/deletion is detected at finalize or ingest.

### AEG-THR-004 — Signed execution inputs
Org-distributed packs, suites, graphs, and adapters MUST be signature-verified before load; unsigned requires dev profile + explicit flag + degraded flag.
**AC:** Unsigned org artifact refuses; `--allow-unsigned` is recorded on the run.

### AEG-THR-005 — Layered secret detection
Redaction and secrets linters MUST use pattern + entropy + verifier layers.
**AC:** Benchmark corpus detection rate documented; entropy-only secrets caught.

### AEG-THR-006 — Rollback-protected distribution
Clients MUST refuse key/CRL/policy snapshots older than the last verified version.
**AC:** Stale-snapshot replay test refuses.

### AEG-THR-007 — No public listeners, ever
The out-of-proc transport target is authenticated UDS/mTLS inside the Class A boundary.
**AC:** `ml-no-listener` covers the new transport; no bot binds a routable interface.

### AEG-THR-008 — Deterministic concurrent folds
Same-run concurrent appends fold deterministically; conflicting transitions surface degraded.
**AC:** Two-writer contention test yields identical folds on every reader.

## 6. Signing infrastructure: adopt, don't invent

| Concern | Corpus today | Adopt | Why it exceeds (Canonical Rule 4) |
|---|---|---|---|
| JSON canonicalization for digests | ad-hoc "sorted keys, no whitespace" (RP-001 §2) | **RFC 8785 (JCS)** | Specified corner cases (numbers, unicode); interoperable digests across languages |
| Signature envelope | bare detached sig (RP-001 §2.2) | **DSSE** envelope (Ed25519 keys retained) | Payload-type binding prevents cross-protocol signature reuse |
| Key distribution, rotation, revocation, offline trust | bespoke Tower bundle + CRL + TTL (RP-002) | **TUF** roles (root/targets/snapshot/timestamp) | Solves exactly RP-002's problem incl. bootstrap (Q3) and rotation (RP-001 Q1) with survivable-compromise semantics; Tower serves the TUF repository (RP-010 §3.2) |
| Build provenance for images/bots | CVS labels only | **SLSA/in-toto attestations** as CVS extension | Verifiable builder identity, not just labels |

These adoptions **closed RP-001 Q1 and RP-002 Q3** with operator sign-off on 2026-09-13; the conforming RP-001 §2 and RP-002 §3.4 amendments are applied and tracked in `PENDING-EDITS.md`.

## 7. Open questions

1. Hash-chain anchor key custody: machine keyring vs Tower-held vs both (lean: machine keyring, Tower-escrowed).
2. Hardware-backed human keys (passkeys/security keys) for deploy-critical waivers.
3. Four-eyes policy scope (deploy-path waivers + org promotions — ties to CORE §17 Q9).
4. Sandboxing tier for subprocess linters per OS (seccomp on Linux, sandbox-exec on macOS).

---

*ACCEPTED (design) 2026-09-13. No implementation authorized by this document; open hardening questions remain tracked in §7.*
