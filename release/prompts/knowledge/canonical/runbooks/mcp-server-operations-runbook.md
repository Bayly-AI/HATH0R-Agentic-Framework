# Runbook: Hath0r MCP Server Operations & Re-indexing

**Runbook ID**: `RB-HATH0R-MCP-OPS-001`  
**Classification**: Service Operational Runbook  

---

## 🎯 Purpose
Operate, inspect, and synchronize the Hath0r MCP knowledge server.

---

## 📋 Standard Procedures

### 1. Health & Readiness Verification
```bash
# Check readiness probe (200 OK)
curl -fsS "http://127.0.0.1:38083/ready"

# Check detailed status
curl -fsS "http://127.0.0.1:38083/health"
```

### 2. Full Knowledgebase Synchronization
When new canonical documentation, rules, or architecture files are added:
```bash
docker exec Hath0r-MCP python -m knowledgebase.cli.main sync --force
```

### 3. Container Restart & Lifecycle
```bash
docker restart Hath0r-MCP
docker logs --tail 50 Hath0r-MCP
```
