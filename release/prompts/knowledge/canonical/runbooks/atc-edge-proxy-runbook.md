# Runbook: Hath0r ATC Edge Proxy & Session Operations

**Runbook ID**: `RB-HATH0R-ATC-OPS-001`  
**Classification**: Control Tower Operational Runbook  

---

## 🎯 Purpose
Maintain and troubleshoot the Hath0r ATC edge reverse proxy (`Hath0r-Edge`) and session coordinator (`Hath0r-Sessions`).

---

## 📋 Standard Procedures

### 1. Ingress Edge Health Check
```bash
curl -fsS "http://127.0.0.1:38000/healthz"
```

### 2. Verify Nginx Configuration Syntax
```bash
docker exec Hath0r-Edge nginx -t
```

### 3. Verify Redis Session Persistence
```bash
docker exec Hath0r-Sessions redis-cli ping
docker exec Hath0r-Sessions redis-cli info persistence
```

### 4. Tail Ingress Edge Logs
```bash
docker logs -f Hath0r-Edge
```
