# Hath0r Framework Compliance Report

**Generated:** 2026-09-23T20:08:36Z
**Spec:** HATHOR-PLAYBOOK-001 / CR-HATH0R-INIT-001
**Framework:** `Bayly-AI/HATH0R-Agentic-Framework` @ `OpenSource/hath0r` (branch `development`)
**Operator CLI:** `{"schema":"hath0r.cli.response/1","command":"version","generated_at":"2026-09-23T20:08:45Z","state":"ok","data":{"binary":"hath0r","package":"hath0r-cli","version":"0.2.0"},"diagnostics":[],"meta":{"cli_version":"0.2.0","duration_ms":0}}`
**Suite doctor:** exit `0` (HATH0R_GROUP_ROOT=OpenSource)

## Summary

- **12/12** in-scope repos meet playbook done criteria (layout + bootstrap exit 0).
- Group hub: `OpenSource/AGENTS.md`, `OpenSource/WARP.md`, `OpenSource/.hath0r/knowledgebase/`.
- Compatibility symlink: `OpenSource/HATH0R-CLI` → `hathor-cli`.
- Legacy `.ai/` migrated to `.hath0r/legacy-from-ai/` for `1-Nation/MCP` and `BAI/MCP`.
- Contracts pinned from framework `lib/schemas` + `lib/contracts` at fileset **0.2.0**.

## Per-repo matrix

| Repo | Layout | INIT + runbook | No legacy roots | Bootstrap | Compliant |
|------|--------|----------------|-----------------|-----------|-----------|
| `1-Nation/ATC` | ✅ | ✅ | ✅ | ✅ (0) | ✅ |
| `1-Nation/MCP` | ✅ | ✅ | ✅ | ✅ (0) | ✅ |
| `BAI/MCP` | ✅ | ✅ | ✅ | ✅ (0) | ✅ |
| `OpenSource/hathor-cli` | ✅ | ✅ | ✅ | ✅ (0) | ✅ |
| `OpenSource/hath0r-poc` | ✅ | ✅ | ✅ | ✅ (0) | ✅ |
| `OpenSource/hath0r-atc` | ✅ | ✅ | ✅ | ✅ (0) | ✅ |
| `OpenSource/hath0r-mcp` | ✅ | ✅ | ✅ | ✅ (0) | ✅ |
| `1-Nation/UXP` | ✅ | ✅ | ✅ | ✅ (0) | ✅ |
| `BAI/UXP` | ✅ | ✅ | ✅ | ✅ (0) | ✅ |
| `BAI/UXP/BAI-BaylyAI` | ✅ | ✅ | ✅ | ✅ (0) | ✅ |
| `Websites/bayly-consulting/UXP` | ✅ | ✅ | ✅ | ✅ (0) | ✅ |
| `OpenSource/hath0r` | ✅ | ✅ | ✅ | ✅ (0) | ✅ |

## Playbook done criteria

| Criterion | Status |
|-----------|--------|
| Framework checkout at `OpenSource/hath0r` | ✅ |
| `hath0r --version` works (0.2.0) | ✅ |
| Same-tech `docs/runbook.md` per repo | ✅ |
| AGENTS includes CR-HATH0R-INIT-001 + runbook link | ✅ |
| Only `.hath0r/` hidden root | ✅ |
| `cfg/product|suite|knowledge-tower.yaml` | ✅ |
| `MANIFEST.json` + contracts + VERSION + NOTICE | ✅ |
| `./bin/hath0r-bootstrap.sh` exits 0 | ✅ |
| OpenSource suite `hath0r doctor` healthy | ✅ |

## Remediation performed

1. Cloned latest HATH0R-Agentic-Framework into empty `OpenSource/hath0r` (preserved usage report).
2. Reinstalled hath0r-cli 0.2.0 editable for `/usr/local/bin/hath0r`.
3. Applied UPL pins, contracts, bootstrap, runbooks, and INIT blocks across all in-scope repos.
4. Migrated forbidden `.ai/` trees under `.hath0r/legacy-from-ai/`.
5. Seeded OpenSource group hub docs, suite catalog, tower cfg, and `HATH0R-CLI` symlink.
6. Aligned tower path strings to doctor-expected `.../OpenSource/HATH0R-CLI`.

## Out of scope

- Non-git placeholders: `Websites/doctor-sleep`, `Websites/knithappens`, `Websites/docs`, `BAI/docs`.
- No git commits created; working-tree changes only.

## Bootstrap evidence

- `1-Nation/ATC`: bootstrap exit `0` compliant=True
- `1-Nation/MCP`: bootstrap exit `0` compliant=True
- `BAI/MCP`: bootstrap exit `0` compliant=True
- `OpenSource/hathor-cli`: bootstrap exit `0` compliant=True
- `OpenSource/hath0r-poc`: bootstrap exit `0` compliant=True
- `OpenSource/hath0r-atc`: bootstrap exit `0` compliant=True
- `OpenSource/hath0r-mcp`: bootstrap exit `0` compliant=True
- `1-Nation/UXP`: bootstrap exit `0` compliant=True
- `BAI/UXP`: bootstrap exit `0` compliant=True
- `BAI/UXP/BAI-BaylyAI`: bootstrap exit `0` compliant=True
- `Websites/bayly-consulting/UXP`: bootstrap exit `0` compliant=True
- `OpenSource/hath0r`: bootstrap exit `0` compliant=True
