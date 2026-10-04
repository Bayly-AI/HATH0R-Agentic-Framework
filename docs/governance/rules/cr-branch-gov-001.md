---
id: rule:cr-branch-gov-001
type: rule_policy
title: "CR-BRANCH-GOV-001: Environment Promotion Path & Branch Governance"
priority: 4
priority_name: ORG_INVARIANT
target_scope: root
restricted_actions: [direct_push_master, direct_push_staging, direct_push_testing]
governs_roles: [developer, qa-engineer, release-manager]
---
# CR-BRANCH-GOV-001: Environment Promotion Path & Branch Governance (CRITICAL — Org-Wide)

> **Rule ID:** `CR-BRANCH-GOV-001` (incorporates `CR-BAI-001`)  
> **Status:** RATIFIED & MANDATORY RUNTIME INVARIANT  
> **Applies to:** All Repositories, Workflows, Pull Requests, and Release Trains across HATH0R OpenSource & Enterprise Products.  
> **Effective Date:** 2026-09-30  

---

## 1. Main Entry Statement (CRITICAL INVARIANT)

> **All development MUST follow the strict environment promotion path (`local → development → testing → staging → master`) and issue-driven branch naming rules.**
>
> Pushing directly to `master`, `staging`, or `testing`, opening feature PRs targeted at non-development base branches, or creating work branches without a backing GitHub issue is **STRICTLY FORBIDDEN**.

---

## 2. Core Directives

1. **Issue First Rule:**
   - Every work branch MUST be preceded by an open GitHub issue. No issue $\rightarrow$ no branch.
2. **Branch Naming Standard:**
   - Work branches MUST branch off `development` and use the taxonomy:  
     `feature|bugfix|enhancement|research|fix|chore/<issue-number>-short-slug`  
     *Example:* `feature/202-codify-org-invariant-policies`
3. **Branch Validation:**
   - Validate work branches prior to PR creation using `hath0r branch validate <branch-name>`.
4. **Target Base Branch:**
   - All feature and bugfix PRs MUST target `development`. Base branches `testing`, `staging`, and `master` are reserved for promotional release trains.
5. **Environment Promotion Path:**
   - Code promotes strictly along the pipeline:  
     $$\text{local} \longrightarrow \text{development} \longrightarrow \text{testing} \longrightarrow \text{staging} \longrightarrow \text{master (Production)}$$
   - Skipping environment stages (e.g. promoting `development` directly to `staging` or `master`) is prohibited.
6. **Human Gate & Admin Approvals:**
   - Owner (`@somesayray`) may merge PRs into `development` at any time. Promotions to `staging` and `master` require passing automated CI and explicit human sign-off.

---

## 3. Enforcement & Verification

- **CI Workflow Enforcer:** `.github/workflows/enforce-promotion-path.yml` enforces base branch targeting rules.
- **Branch Bot:** `hath0r branch validate` validates branch taxonomy before pushing.
