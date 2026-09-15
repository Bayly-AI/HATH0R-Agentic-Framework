# Agent Integrator Guide

As an Agent Integrator (or AI Agent), you interact with the AEGIS platform as an active participant—building, verifying, and navigating project state. You will drive your operations entirely through the `aegis` CLI.

## 1. The Single Control Plane

The `aegis` CLI is your sole interface for everything. You do not talk directly to background daemons, nor do you execute random scripts bypassing the platform's gates. 

Use the `--output=json` flag (or rely on pipe auto-detection) to get machine-readable JSON envelopes. Every refusal or error provides a structured response with `{code, message, remediation, provenance, ttl}`.

### CLI Exit Codes
- `0`: Success (including dry-run and idempotent no-op)
- `1`: Runtime / internal failure
- `2`: Usage / validation error
- `3`: Not found
- `4`: Auth / permission
- `5`: Conflict / already exists
- `6`: Dependency unhealthy
- `7`: Confirmation required in non-interactive context

## 2. Navigating the Universal Project Layout (UPL)

Every AEGIS project follows the Universal Project Layout. 
* **`.aegis/`** - Hidden metadata containing `manifests/`, `rules/`, `state/` (runs, checklists, spool), and `knowledge/`.
* **`AGENTS.md`** - Exists at the root and in subdirectories. Resolves nearest-first to provide you with your local context and rules.

Always respect the UPL. Do not create `.infraOS/` directories; use `aegis repo validate` to ensure structural integrity.

## 3. Working with the Ticketing Plane

AEGIS requires work to be authorized by a ticket.
* **No-Ticket Gate:** You cannot execute substantive mutations (code changes, PRs) without an active, authorized ticket linked to an Epic.
* **Commands:** Use `aegis work ...` to interact with Jira, ADO, GitHub, or the Backup TS.
* **PR Bindings:** When you create a branch or PR, it MUST follow the naming convention `feature/<KEY>-<initials>-<slug>`.
* **Environment Promotion Path (CR-BAI-001):** You must respect the canonical promotion path: `local → development → testing → staging → master (Production)`.
  * Open PRs into `testing` only from `development`.
  * Open PRs into `staging` only from `testing`.
  * Open PRs into `master` only from `staging`.
* **Estimation:** Tickets must store base and reduced hours under a named policy.

## 4. Working with the Knowledge Plane

* **Tiered Retrieval:** Use `aegis knowledge ...` to query. The system automatically cascades through Project -> Machine -> Organization -> Public.
* **Microburst Writes:** You can only write knowledge in small, session-scoped microbursts. Do not attempt bulk syncs.
* **Draft State:** New knowledge enters as a `draft` and is only retrievable via `--include-drafts`. It must pass human review and mechanical gates (secrets/PII scanning) before promotion to `verified`. No auto-promotion is permitted.

## 5. Executing Runs & Governance Gates

To run hierarchy workflows or playbooks, dispatch intents via `aegis process ...`.
* **Plan First:** Always use `--dry-run` first for non-idempotent operations to get a JSON plan of the effects.
* **Confirm:** Use `--yes` to proceed with live mutations.
* **Governance Gates (15 Points):** Be prepared for the platform to refuse your request (e.g., if you are missing a ticket, if there is a contract mismatch, or if a micro-linter fails). Read the JSON error envelope's `remediation` field to fix the issue and try again. Active blocking protects the integrity of the ecosystem.
