---
id: AEGIS-GUIDE-025
title: Objection Handling and FAQ
summary: 'For every objection:'
doc_type: GUIDE
diataxis: reference
audience: [sales, agent]
tags: []
version: 0.1.0
status: draft
created: '2026-09-14'
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
# Objection Handling and FAQ

- **Audience:** Internal sales, solutions, product, executives, and technical evaluators
- **Disclosure:** Internal answer guide; security-detail disclosure requires review
- **Maturity:** Answers reflect the documentation baseline, not future implementation

## Response pattern

For every objection:

1. answer directly;
2. state current maturity;
3. explain the target design;
4. identify the required evidence; and
5. propose a bounded next step.

## Product and maturity

### Is AEGIS available and production-ready?

No such claim is supported by the repository. HATHOR is in early formation, AEGIS is described as a greenfield implementation, and the corpus primarily contains accepted designs, draft specifications, and plans.

The safe motion is design-partner discovery or a bounded development pilot once authorized implementation evidence exists.

### Is there working technology behind the design?

The research includes verified facts about an existing `infraos-os` 9.3.0 baseline and one-machine usage history. Those facts informed AEGIS but are not greenfield AEGIS runtime evidence.

Ask product engineering for a current implementation inventory, test results, and versioned release evidence before making availability claims.

### Why is the documentation so detailed if the product is not shipped?

The corpus establishes defined-state architecture, authority boundaries, contracts, risks, and a staged roadmap. Detailed design reduces ambiguity, but it does not replace authorized code, tests, operating ownership, or customer evidence.

### What exactly are we buying?

The repository defines an Apache-2.0 project and target platform architecture. It does not define commercial packaging, enterprise features, hosted service, support, indemnity, pricing, SLA, or contract terms.

Escalate commercial questions; do not infer a package from the license.

## Category and ecosystem

### Is AEGIS another AI model or agent framework?

It is not a foundation model or agent harness. HATHOR is the agentic application framework; AEGIS is the proposed governance and control-plane realization intended to operate above models and harnesses.

### Is this another issue tracker?

No. The Ticketing Plane is intended to normalize governed work operations while Jira, Azure DevOps, GitHub, or another approved provider remains authoritative. The backup service is deliberately minimal and should not become a competing enterprise tracker.

### Does it replace source control or CI/CD?

No. It is designed to complement Git and CI/CD by connecting work authorization, validation, evidence, and human promotion to the existing delivery path.

### Is it just an orchestration engine?

No. Orchestration is one part. The target model also separates capability provenance, work authority, knowledge authority, validation, provider brokering, human decisions, and observation.

### Why a CLI instead of an API or UI?

The accepted design uses a CLI as the bounded public ingress for humans and agents, with structured machine output and schema discovery. Tower still exposes authenticated backend APIs. A browser UI is deferred.

The repository does not prove that CLI is universally superior. Existing payload research is narrow and non-equivalent.

## Security and control

### Can agents bypass AEGIS?

The v1 prevention scope covers cooperative-but-fallible actors using platform interfaces. It does not claim prevention against a malicious local process with arbitrary workspace access.

A buyer needing stronger prevention must define OS isolation, evidence anchoring, executable integrity, and independent enforcement requirements beyond the current v1 boundary.

### Is it tamper-proof?

No. Do not use that term. Local record integrity requires further hardening, and runtime artifact binding is unresolved.

### Are bots cryptographically signed?

The accepted design signs canonical capability definitions and referenced governance artifacts using standards-based mechanisms. That is design status. The current model does not yet bind executable or image bytes, so it is not complete runtime substitution protection.

### Are credentials eliminated from bots?

The target is no long-lived provider credentials in worker bots by default. Operator proxies Class-1 effects. Declared Class-2 exceptions may receive a narrow, short-lived, run-bound token in memory.

Avoid “zero secrets” as an absolute.

### How does human approval work?

The target requires short-lived Tower-issued human identity for reserved actions. The complete claims, audience, action, run, nonce, expiry, revocation, and replay contract remains to be frozen and tested.

Chat, terminal presence, or a machine identity must not be presented as sufficient proof.

### Does AEGIS guarantee that required steps cannot be skipped?

The accepted orchestration direction and draft gateway are designed to make required work and sequence explicit. A no-skip claim requires implementation, negative tests, and the cooperative-but-fallible trust qualifier.

### Does it provide exactly-once external effects?

No guaranteed exactly-once claim is supported. The target uses idempotency, bounded retry, receipts, and reconciliation. Provider semantics, interruption, and ambiguity must be tested per integration.

### Is AEGIS compliant with a named standard?

No certification is documented. The architecture may support organization-specific controls for change authorization, separation of duties, least privilege, credential management, provenance, evidence, continuity, and audit. Compliance requires mapping, implementation, operation, evidence, and independent assessment.

## Integrations and deployment

### Does AEGIS integrate with Jira, Azure DevOps, and GitHub?

They are documented target work adapters, with Jira-first adoption sequencing. Do not call every adapter available until implementation and conformance evidence exists.

### Can it support other providers?

The design is provider-neutral and extensible through contracts and adapters. That does not make an unnamed provider supported. Qualify required operations, authentication, idempotency, rate limits, error semantics, and test scope.

### Is it language-agnostic?

HATHOR’s contracts and project model are intended to be language-agnostic. The AEGIS reference implementation direction is primarily Go. Distinguish contract portability from implementation language.

### Does it run on Windows?

Windows is outside the stated v1 client target. The accepted v1 scope names macOS and Linux.

### Is deployment EKS-only?

Developer and container documents describe EKS as a target for higher environments, but hosting remains an open organizational decision and some container material is draft. Do not present EKS-only as a settled universal product commitment.

### Is it SaaS?

The v1 target is per-organization and self-hostable. Multi-tenant SaaS is out of the stated v1 scope. Commercial hosting is not defined.

### Does Control Tower become a central availability bottleneck?

The accepted architecture keeps Tower asynchronous rather than in every local request path and uses offline-verifiable cached trust with a TTL. Authority-originating actions deliberately refuse after trust expiry.

Availability, HA, capacity, backup, tenancy, and SLOs still require implementation and operating design.

## Knowledge

### Does AEGIS use RAG or vector search?

The accepted knowledge design uses files as truth, rebuildable full-text indexes, optional vectors, tiered retrieval, and explicit confidence. The buyer value is status-honest retrieval, not a specific retrieval buzzword.

### Can agents publish their own knowledge?

Agents may create bounded drafts. Authoritative promotion is intended to require a human reviewer. Automatic promotion is outside the target.

### Does it guarantee correct answers?

No. The target explicitly supports “no confident match,” exposes provenance and status, and requires confidence calibration. Correctness and retrieval quality require evaluation data.

### Will human review become a bottleneck?

It may. Curation effort, queue age, rejection, staleness, and search value must be measured. If review cost exceeds benefit, the knowledge scope should be redesigned.

## Adoption and value

### Will governance slow developers?

It may add friction and may also reduce rediscovery, rework, and evidence assembly. The corpus provides target latency budgets, not observed outcomes.

Baseline orientation, lead time, false refusal, remediation, user effort, and bypass pressure. Start report-only and enforce only when results are acceptable.

### How long will implementation take?

The roadmap contains planning-grade engineering estimates after an interface-freeze milestone. They are not elapsed-time commitments and omit material product, security, integration, adoption, support, and audit work.

Any proposal must re-estimate from current implementation evidence and buyer scope.

### What is the ROI?

There is no validated ROI in the sources. Build a business case from baseline evidence, full cost, measurable capacity or avoided effort, and an approved risk method.

### What customer proof exists?

The repository contains no customer deployment, reference, case study, production SLA, or measured business outcome. Do not imply otherwise.

### Why start in development?

The identity, artifact, recovery, operating, and value controls must be proven before higher-risk use. Development-only scope limits blast radius while the organization learns finding quality and workflow fit.

### What would make a pilot fail?

- routine bypass;
- failed identity or artifact negative tests;
- lost or divergent authority records;
- duplicate or silent provider effects;
- high false refusal with poor remediation;
- undefined ownership or retention;
- unacceptable user effort; or
- no measurable value.

## Licensing

### Is AEGIS open source?

The repository is licensed under Apache License 2.0. The license permits broad use, modification, and distribution subject to its conditions and includes an applicable patent grant.

It does not grant trademark rights, warranty, support, indemnity, or commercial service terms. Refer legal questions to counsel.

## Sources

- [Claims, Evidence, and Source Coverage](./13-claims-evidence-and-source-coverage.md)
- [Security, Governance, and Assurance](./05-security-governance-and-assurance.md)
- [Apache License](../../LICENSE)
