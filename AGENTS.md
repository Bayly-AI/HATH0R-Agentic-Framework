# AGENTS.md — HATH0R Agentic Framework

> Role: **OpenSource HATHOR framework + docs corpus** · member of **OpenSource Project** (`hath0r-opensource`)  
> Updated: 2026-09-15

## Group membership (CRITICAL)

| Field | Value |
|-------|-------|
| Group | `hath0r-opensource` |
| Project | **OpenSource Project** |
| Group root | `/Users/raybayly/Development/OpenSource` |
| **Control tower** | `/Users/raybayly/Development/OpenSource/HATH0R-CLI` (`Bayly-AI/HATH0R-CLI`) |
| This product | `HATH0R-Agentic-Framework` |
| GitHub | `Bayly-AI/HATH0R-Agentic-Framework` |
| Local path | `/Users/raybayly/Development/OpenSource/hath0r` |
| Canonical KB | `/Users/raybayly/Development/OpenSource/.hath0r/knowledgebase` |
| Operator CLI | `hath0r` |
| Docs | `docs/` (canonical OpenSource documentation corpus) |

### Canonical siblings (all under OpenSource are project members)

- **Control tower / CLI**: `/Users/raybayly/Development/OpenSource/HATH0R-CLI` → `Bayly-AI/HATH0R-CLI`
- Framework: `/Users/raybayly/Development/OpenSource/hath0r` → `Bayly-AI/HATH0R-Agentic-Framework`
- POC: `/Users/raybayly/Development/OpenSource/hath0r-poc` → `Bayly-AI/HATH0R-Agentic-POC`

Group rules: `/Users/raybayly/Development/OpenSource/AGENTS.md`  
Group policy: `/Users/raybayly/Development/OpenSource/WARP.md`

## Framework hidden root (CRITICAL — cr-hath0r-root-001)

Use **only** `.hath0r/` for framework-created / modified / saved project metadata.

Do **not** use `.ai/`, `.aegis/`, or `.infraOS/`.

## Knowledgebase (CRITICAL — cr-kb-tower-001)

1. Point local knowledgebase operations at the OpenSource group hub.
2. Keep member `.hath0r/knowledgebase` as stub/pointer only.
3. Resolve control-tower / suite orientation to **HATH0R-CLI**.
4. Framework `docs/` is the **canonical OpenSource documentation** corpus.
5. Do **not** treat private internal product trees as OpenSource canonical sources.

## Open issues tracking (group-wide)

Use the verified multi-repo search (all three OpenSource products):

```text
is:issue state:open repo:Bayly-AI/HATH0R-Agentic-Framework repo:Bayly-AI/HATH0R-Agentic-POC repo:Bayly-AI/HATH0R-CLI
```

Canonical definition: group `AGENTS.md` (*Open issues tracking*). Also listed in `docs/README.md`.

## Branch & PR targets (CRITICAL — cr-branch-gov-001)

1. **Issue first**: create a GitHub issue before any work branch. No issue → no branch.
2. Branch from `development` only, using:
   `feature|bugfix|enhancement|research|fix|chore/<issue-number>-short-slug`
   Example: `chore/4-control-tower-cli`
3. Open the PR with **base = `development`** (feature work never targets testing/staging/master).
4. **Owner (`@somesayray`) may merge any PR at any time** (admin bypass enabled; approvals not required).
5. Merge into **`development` only** for feature work.
6. Promote via `development → testing → staging → master` — do not skip stages.
7. **PR CI failures notify `@somesayray`** via `.github/workflows/notify-pr-failure.yml` (PR comment + optional Slack `SLACK_WEBHOOK_URL`).

### Canonical branches (locked)

`development` (default), `testing`, `staging`, `master`

- Must not be deleted
- Must not be used as feature/work branches
- Must not be merged into each other except along the promotion path above
- Branch protection: PR required (0 approvals), no code-owner gate, admin bypass on, no force-push, no deletions, `validate-promotion-path` required (non-strict; admin can bypass)

Forbidden: feature PRs targeting `master`, `testing`, or `staging`; PRs without an issue number in the branch name; merging canonical branches sideways.

## CR-BAI-001: Environment Promotion Path (CRITICAL — org-wide)

Canonical policy: `/Users/raybayly/Development/BAI/WARP.md` (org-wide). Group mirror: `/Users/raybayly/Development/OpenSource/WARP.md`.

Required order (never skip):

```text
local → development → testing → staging → master (Production)
```

CI enforcement: `.github/workflows/enforce-promotion-path.yml`

- PRs into `testing` must come from `development`
- PRs into `staging` must come from `testing`
- PRs into `master` must come from `staging`
- Each stage needs deploy + URL validation before the next promote

## Credentials

`/Users/raybayly/Development/.credentials/<service>/.env` — never hardcode or print secrets.

## CR-HATH0R-INIT-001: Hath0r repo initialization entry gate (CRITICAL — org-wide)

**Main entry statement:** Before initializing (or re-initializing) any repository with Hath0r, agents MUST:

1. **Setup playbook** — Locate and follow the canonical Hath0r setup playbook:
   - `/Users/raybayly/Development/OpenSource/hath0r/docs/developers/hathor-playbook-001-repo-init-setup-20260919.md`
   - If the playbook is missing or incomplete, **create or update it first**, then proceed.
2. **Same-technology runbook** — Locate a runbook for an **individual repo with the same technology stack** (e.g. React+Vite UXP, Python CLI):
   - Prefer a sibling/product `docs/runbook.md` (or `docs/*runbook*`) in that tech family.
   - If none exists, **create a tech-appropriate runbook in the target repo** before finishing init.
3. Only after (1) and (2) are satisfied: apply fileset/layout, `.hath0r/`, `cfg/`, contracts pin, `AGENTS.md` identity, and `./bin/hath0r-bootstrap.sh`.

Do not skip the playbook/runbook gate. Layout scaffolding without a documented ops path is incomplete initialization.

## Branch rules (pointer)

See `docs/governance/branch-rules.md` (cr-branch-gov-001 / CR-BAI-001). Work PRs → `development` only; release trains use `release/x.x.x`.
## PR workflow hardening

See `docs/governance/pr-workflow.md`. Work PRs → `development` (agents + CODEOWNERS). **Human gate** before staging/master.
## SonarCloud Quality Gate (CRITICAL)

- Canonical thresholds: SonarCloud Quality Gate only — do not modify gate thresholds ad hoc.
- PR check **SonarCloud Quality Gate** is a hard stop on failure.
- See `docs/governance/sonarcloud-quality-gates.md`
- Secret required: `SONAR_TOKEN`
## Documentation → MCP

Docs are published to the **proper group MCP** via control-tower
`python3 scripts/publish-docs-to-mcp.py` (`cfg/mcp-doc-publish.json`).
See HATH0R-CLI `docs/governance/mcp-doc-publish.md`.
