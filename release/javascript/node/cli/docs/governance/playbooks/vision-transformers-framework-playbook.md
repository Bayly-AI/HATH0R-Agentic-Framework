# Playbook: Operating Multimodal Perception & Vision Transformers

> Operational Playbook for Hath0r Framework Vision Engine  
> Product: `HATH0R-Agentic-Framework` · Group: `hath0r-opensource` · Issue: #149 · CLI Alignment: #219 / #221

---

## 📋 Overview

This playbook describes how agents and developers configure, invoke, and test the `VisionEngine` in the Hath0r Agentic Framework.

---

## 💻 Python API Usage

### 1. Initializing the Vision Engine

```python
from hath0r_engine.vision import VisionEngine

# Create vision engine with automatic backend resolution
vision = VisionEngine()
```

### 2. Inspecting an Image or Mockup

```python
result = vision.inspect("docs/assets/system-architecture.png", prompt="Analyze component relationships")
print(result["description"])
```

### 3. Parsing Architecture Diagrams into Structured ASTs

```python
parsed = vision.parse_document("diagrams/cloud-topology.png")
for section in parsed["document_structure"]["sections"]:
    print(f"- {section}")
```

### 4. Grounding UI Elements for Browser Automation

```python
grounded = vision.ground("screenshots/login-page.png", target="Sign In with GitHub")
center = grounded["grounded_target"]["center_coordinates"]
print(f"Click target at: ({center['x']}, {center['y']})")
```

### 5. Synthesizing Code from Visual Mockup

```python
code_res = vision.synthesize_code("designs/dashboard-widget.png", framework="react_tailwind")
print(code_res["generated_code"])
```

---

## ⚙️ Configuration (`cfg/vision.yaml`)

```yaml
version: "1.0"
provider: "auto" # auto | pytorch | ollama | remote | fallback
pytorch:
  device: "auto" # auto | mps | cuda | cpu
local:
  backend: "ollama"
  model: "llava"
  host: "http://localhost:11434"
embedding:
  model: "clip-vit-base-patch32"
  dimensions: 512
```
