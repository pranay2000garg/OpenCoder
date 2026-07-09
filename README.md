# OpenCoder

OpenCoder is a local AI coding assistant inspired by Claude Code and Cursor, designed to work with local LLMs through Ollama.

It provides an interactive terminal interface that allows an AI model to inspect projects, create and edit files, search code, and execute shell commands with user approval.

---

## Features

- Interactive terminal interface
- Local-first architecture
- Ollama integration
- Tool calling support
- File creation and editing
- Recursive code search
- Shell command execution
- Conversation history
- Model switching
- Auto approval mode (YOLO)

---

## Requirements

- Python 3.11+
- Ollama
- A supported coding model

Example:

```bash
ollama pull qwen2.5-coder:7b
```

---

## Installation

Clone the repository.

```bash
git clone <repository-url>
cd OpenCoder
```

Create a virtual environment.

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

## Running

```bash
python -m ocode.main
```

Specify a different model.

```bash
python -m ocode.main --model deepseek-coder:latest
```

Specify a different Ollama server.

```bash
python -m ocode.main --host http://localhost:11434
```

Disable tools.

```bash
python -m ocode.main --chat
```

Enable automatic approvals.

```bash
python -m ocode.main --yolo
```

---

## Available Commands

| Command | Description |
|---------|-------------|
| `/help` | Show available commands |
| `/model <name>` | Switch model |
| `/reset` | Reset conversation |
| `/clear` | Clear the screen |
| `/tools` | Enable or disable tool usage |
| `/yolo` | Toggle automatic approvals |
| `/exit` | Exit OpenCoder |

---

## Project Structure

```
ocode/
├── cli/
├── contracts/
├── core/
├── models/
├── tools/
├── utils/
└── main.py
```

---

## Current Tools

- read_file
- list_dir
- write_file
- edit_file
- run_bash
- search_code

---

## Roadmap

- Streaming responses
- Git integration
- Project indexing
- Better terminal UI
- Multi-provider support
- Plugin system

---

## License

MIT License