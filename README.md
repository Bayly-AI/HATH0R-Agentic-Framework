<p align="center">
  <img src="lib/assets/images/hathor-logo-1.png" alt="HATHOR logo" width="280" />
</p>

# HATHOR

**Agentic Application Framework**

HATHOR is a language-agnostic agentic framework for optimizing how agents work inside real projects. It is part of the **AEGIS** platform and defines the shared contract between agents, the CLI, project layout, knowledge infrastructure, governance, and credentials.

> Agents should spend less time rediscovering a codebase and more time shipping correct work.

---

## Why HATHOR

Most agent tooling assumes a chat session and a pile of files. HATHOR assumes a **durable operating environment**:

- A standard project shape every agent can navigate
- A single CLI as the agent’s first interface
- Layered knowledge (project → machine → organization → public)
- Provenance, freshness, and governance on what agents read and write
- Credential mediation that never dumps secrets into source control

---

## Architecture at a Glance

```text
Agent ──► CLI ──► Universal Project Layout
              │
              ├─ Knowledge Infrastructure (MCP / CLI / Project)
              ├─ Governance & Rules
              └─ Security & Credentials
```

### Agent

The agent is the worker. It does not own the project layout or secret store. It discovers authority, knowledge, and tools through HATHOR’s interfaces.

### CLI

The CLI is a **globally installed** application on every machine that uses AEGIS. It is the first thing agents consent to interface with.

It provides:

- Commands, models, research, and context access
- Elevation of authority across trust tiers: **guest → elevated → sovereign**
- Mediation of credentials and knowledge lookups
- A stable boundary between agent intent and host capabilities

### Universal Project Layout

The project layout is code- and framework-agnostic. It lets file agents (and humans) orient quickly **before** building out any application. In practice this also sets up a git-ignore project of full angels’ projects where appropriate.

Significant folders always mean the same thing. That keeps the root clean and keeps agent files out of source clutter.

| Path | Role |
| --- | --- |
| **CFG** | All project configuration files that aren’t required at the root |
| **BIN** | Executables and scripts, organized by folder, allowing us to organize all of the scripts we use at the singular project level. If a binary is only used for this project, it goes here. Standard wrapper scripts always live here. |
| **LIB** | Static assets, files, images, etc., organized in folders. Reports, artifacts, and documents that are not docs live here. |
| **docker** | Docker files kept alongside us to keep the deployment files out of the main repo root noise |
| **SRC** | Application source. All code writes happen here prior to building and testing. |
| **DIST** | Build output. When the application is transpiled/compiled, it is placed here, where it can be tested, built, and (when relevant) used to build the app on the container. |
| **Test** | Unit, pre- and post-deploy tests, as well as bad files, test cases, and testing document scripts like selenium or playwright files |
| **docs** | Human- and agent-facing documentation about the project |

#### Hidden agent configuration

Local agent/tool configuration (including **angels**) lives under hidden configuration folders. Everything angels would historically keep in an `.ai` (or older tool-specific) directory consolidates under HATHOR’s agent configuration layout (for example `.ai.angels`).

- The agent reads local **AGENTS** and is pointed to places of interest for the agent, including the location of the other **AGENTS** files under it.
- Every significant folder has an **AGENTS** md file that covers that folder and its information.
- This keeps automatic agent files out of source clutter while remaining discoverable.

---

## Knowledge Infrastructure

HATHOR keeps a **clear tier separation** between knowledge levels.

### Search order (all through CLI)

```text
Project  →  Machine  →  Organization  →  Public
```

If a higher-priority tier answers the query, lower tiers are not required. Missing tiers **degrade gracefully**.

| Level | Surface | Purpose |
| --- | --- | --- |
| **Organization** | MCP server | Shared org knowledge agents can always reach when configured |
| **Machine** | CLI knowledge | Small local library that allows agent knowledgebases standard to the machine (or project you join with) |
| **Project** | Project knowledge / MCP | The only place project-specific knowledge is authoritative |

### Knowledge properties

HATHOR treats knowledge as infrastructure, not chat history:

| Concern | Intent |
| --- | --- |
| **Knowledge discoverability** | Agents can find what exists without tribal memory |
| **Digital provenance** | Every knowledge base article can carry a bridge, cryptographic timestamped identity, and a triple ID trail |
| **Micro limiters** | Guardrails that constrain retrieval and action scope |
| **Standardized communication** | The CLI, bots, and agents speak a shared protocol language (agent and CLI stay in sync) |
| **Machine-readable manifest** | Ensure the agent can always locate folder purposes, agent scopes, build/test/setup commands, and shared daily abstract lines |
| **TTL / staleness** | Add TTL/staleness flags so an article that hasn’t been touched for *N* months gets a “stale” marker so agents treat it with intention |
| **Retrieval quality** | Hybrid search (keyword + vector) as needed; semantic similarity measured when useful; hierarchical preference to local context over external fragments and self-identified noise |
| **Graceful degradation** | If a system or service is not available, look to see if there are other known options for the connection/type/service; if not, the agent marks it and continues |
| **Draft / verified status** | Status signals so agents know whether content is draft, verified, or authoritative |

### Knowledge priority order (conceptual)

1. Project-local, verified knowledge  
2. Machine-local knowledge relevant to the current work  
3. Organization knowledge via MCP  
4. Public / external sources (lowest trust, highest need for citation and caution)

Agents are expected to **cite article IDs** in their reasoning when knowledge infrastructure is available.

### “The Tower of Power”

Every project has a pointer to the central tower — a known location for core truth that every agent is expected to go to for orientation when available. When unavailable, agents degrade gracefully rather than inventing structure.

---

## Governance and Rules

Governance is not optional decoration. HATHOR expects:

- Rules and policies that agents must respect
- Clear separation of what agents may read, write, execute, or escalate
- Consistent application of project and org constraints across tools

Governance packages sit alongside the layout so both humans and agents can inspect the contract.

---

## Security and Credentials

**The CLI mediates credential issues** in a fixed priority order:

1. **AWS Secrets Manager** — first priority when available  
2. **User root credentials file** — if Secrets Manager is not available and the secret is expected there  
3. **Project repo `.env` file** — if it cannot find the secret higher up  
4. **Sibling repos’ `.env` files** — walk nearby project envs if configured/allowed  

If no credential exists, the CLI will walk you through adding it rather than inventing insecure shortcuts.

Principles:

- Secrets stay out of `SRC` and out of agent chatter  
- Agents request capability through the CLI; they do not scrape the filesystem for keys by default  
- Missing credentials are an operable workflow, not a silent failure  

---

## Design Principles

1. **Language agnostic** — layout and contracts are not tied to one runtime  
2. **Agent-first navigation** — every important folder explains itself  
3. **CLI as control plane** — one elevation and mediation path  
4. **Local context wins** — project truth beats generic model memory  
5. **Provenance over vibes** — cite, timestamp, and mark staleness  
6. **Degrade, don’t die** — missing MCP/org/machine services still allow useful work  
7. **Secure by mediation** — credentials flow through policy, not copy-paste  

---

## Status

HATHOR is in early formation. This repository currently holds the framework identity, license, and foundational assets. Implementation of the CLI, layout scaffolding, knowledge services, and governance packs will land iteratively.

---

## License

Licensed under the [Apache License, Version 2.0](LICENSE).

---

## Part of AEGIS

HATHOR is the agentic application framework within the broader **AEGIS** ecosystem — standardizing how agents interface with projects, knowledge, and secure host capabilities.
