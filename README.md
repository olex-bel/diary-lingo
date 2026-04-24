# Diary Lingo

This project is a Python application designed to analyze and translate Slovak text using large language models (LLMs). It features a graphical user interface (GUI) built with Tkinter, allowing users to easily interact with the application. The core functionality includes text analysis and translation, leveraging LLMs to provide insights and translations for Slovak text. The idea is to create a tool that can assist users in learning Slovak, improving their writing, or simply understanding Slovak text better. The application is structured with a clear separation of concerns, utilizing a modular design to keep the code organized and maintainable. The user learn language by writting personal diary in Slovak and then analyzing and translating it with the help of LLMs.

# 🚀 Getting Started

This project uses **[uv](https://docs.astral.sh/uv/)** for fast Python package and project management.

### Prerequisites

Ensure you have `uv` installed. If you don't have it yet, run:

```bash
# macOS/Linux
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh

# Windows (PowerShell)
powershell -c "ir [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"
```

### Installation
```bash
git clone https://github.com/olex-bel/BiasBuster
cd BiasBuster

# Sync dependencies (uv will automatically create a .venv)
uv sync
```

### Configuration
The application uses toml files for configuration. You can modify the settings in `config.toml` to customize the behavior of the application.

```toml
[app]
window_geometry = "600x400"
font_family = "Arial"
font_size_main = 12
font_size_ui = 8

[llm]
provider = "ollama"
model = "ethanwebb/OpenEuroLLM-Slovak-FIX"
temperature = 0.7

[translator]
provider = "ollama"
model = "ethanwebb/OpenEuroLLM-Slovak-FIX"
temperature = 0.7
```