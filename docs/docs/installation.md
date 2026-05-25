---
sidebar_position: 2
---

# Installation Guide

## Prerequisites

- **Python** 3.11 or later
- **Node.js** 20 or later
- **Rust** (for Tauri builds)
- **2GB RAM minimum** (4GB recommended)

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Sarkar009765/HANTER.git
cd HANTER
```

### 2. Run Setup Script

**Windows:**
```bash
scripts\setup.bat
```

**Linux/macOS:**
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### 3. Configure API Keys

HANTER works without API keys in mock mode. For full functionality:

```bash
# Set your preferred LLM provider
export GROQ_API_KEY="your-groq-key"
# or
export TOGETHER_API_KEY="your-together-key"
```

### 4. Start Development

```bash
./scripts/dev.sh  # or scripts\dev.bat on Windows
```

## Platform-Specific Notes

### Windows
- Install Python from [python.org](https://python.org)
- Install Rust from [rustup.rs](https://rustup.rs)
- Install Node.js from [nodejs.org](https://nodejs.org)

### Linux
```bash
# Install Tauri dependencies
sudo apt-get install libwebkit2gtk-4.1-dev libappindicator3-dev
```

### macOS
- Install Xcode Command Line Tools: `xcode-select --install`
