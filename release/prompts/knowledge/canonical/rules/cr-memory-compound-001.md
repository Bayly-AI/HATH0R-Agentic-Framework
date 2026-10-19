# CR-MEMORY-COMPOUND-001: Mandatory Memory Presence & Pre-Announcement Compounding

**Classification**: Critical Organizational Invariant (`RULE`)  
**Scope**: Org-wide across all working sessions  

---

## 📌 Rule Statement

1. **Universal Memory Presence**:
   Every managed repository MUST maintain an initialized `.hath0r/memory/` directory containing `.hath0r/memory/graph.json`, `.hath0r/memory/sessions/current.json`, and `.hath0r/memory/hashes.json`.

2. **Micro Memory Sessions (<2KB)**:
   Every session MUST read and write a compact (<2KB) micro memory session:
   - `hath0r memory session start` at beginning
   - `hath0r memory session write` during execution
   - `hath0r memory session end` at completion

3. **Cryptographic SHA-256 CAS Hashing**:
   All memory files and referenced source files must maintain valid SHA-256 digests in `hashes.json`.

4. **Mandatory Pre-Announcement Compounding**:
   Every task, bugfix, or feature MUST compound structured knowledge (`episode`, `decision`, `fact`, `insight`, `concept`, or `rule`) into `.hath0r/memory/graph.json` **prior to announcing task completion** (`hath0r memory compound` + `hath0r memory verify`).
