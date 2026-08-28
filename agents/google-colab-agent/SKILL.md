---
name: google-colab-skill
description: Comprehensive Google Colab integration skill for Antigravity, VS Code, and Cursor. Build, optimize, convert, and run interactive Jupyter notebooks with Google Colab GPU/TPU runtimes, Google Drive mounting, secrets management, and Colab VS Code extension connectivity.
version: 1.0.0
author: Google Colab & Antigravity
---

# Google Colab Skill & Plugin Guide

This skill equips Antigravity with complete Google Colab capabilities: creating notebooks with Colab badges, configuring GPU/TPU runtimes, mounting Google Drive, managing Colab `userdata` secrets, and connecting notebooks to remote Colab compute directly inside Antigravity/VS Code.

---

## 🎯 Activation Triggers
- `run in colab`
- `convert to colab notebook`
- `connect to colab runtime`
- `colab gpu / tpu setup`
- `mount google drive in colab`
- `google colab extension`

---

## 🔌 VS Code / Antigravity Colab Extension Integration

The official Google Colab extension (`Google.colab`) is installed in:
- `~/.vscode/extensions/google.colab-0.9.2/`
- `~/.cursor/extensions/google.colab-0.9.2/`

### How to Connect Notebooks to Google Colab in the Editor:
1. Open any `.ipynb` notebook in Antigravity or VS Code.
2. In the top-right kernel picker, select **"Select Kernel"** $\to$ **"Jupyter Kernel..."** $\to$ **"Colab Server"**.
3. Sign in with your Google account.
4. Select your desired runtime type:
   - **Standard CPU**
   - **T4 GPU** (Default High Performance)
   - **A100 / V100 GPU** (Colab Pro)
   - **TPU v2/v3** (Deep Learning)

---

## ⚡ Core Colab Best Practices & Snippets

### 1. Open in Colab Badge
```markdown
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/<username>/<repo>/blob/main/<path-to-notebook>.ipynb)
```

### 2. GPU / Hardware Acceleration Preflight
```python
import torch
print(f"CUDA Available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"Device: {torch.cuda.get_device_name(0)}")
```

### 3. Google Drive Mount
```python
from google.colab import drive
drive.mount('/content/drive')
```

### 4. Secure API Keys via Colab UserData
```python
from google.colab import userdata
api_key = userdata.get('OPENAI_API_KEY')  # Configured in Colab Secrets tab
```

### 5. Interactive Form Parameters
```python
#@title Configuration Parameters
model_name = "glm-4.7" #@param ["glm-4.7", "claude-3.7-sonnet", "gemini-2.5-pro"]
batch_size = 32 #@param {type:"slider", min:8, max:128, step:8}
enable_fp16 = True #@param {type:"boolean"}
```

---

## 🛠️ Automation Tools

Use the bundled generator in `scripts/py_to_colab.py` to convert any standard Python file into an interactive, Colab-ready `.ipynb` notebook with preflight install cells and Colab badges.
