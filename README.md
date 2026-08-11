# 🤖 JARVIS - Personal AI Desktop Assistant

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

JARVIS is a modern, intelligent desktop assistant for Windows that uses natural language processing to understand your commands and execute tasks automatically. Named after the AI from Iron Man, JARVIS is designed to be your personal digital butler.

## ✨ Features

- **🎯 Intent Detection**: Understands user commands and detects intent
- **📋 Task Planning**: Breaks down complex tasks into manageable steps
- **⚙️ Automatic Execution**: Executes planned tasks automatically
- **💾 Memory Management**: Remembers your preferences and information
- **🌐 Web Integration**: Open websites and search the web
- **🚀 App Launcher**: Launch and manage applications
- **💬 Conversation Context**: Maintains conversation history
- **🎨 Modern GUI**: Beautiful dark-themed tkinter interface

## 📋 Supported Commands

### Application Control
```
open chrome
close firefox
launch visual studio code
quit notepad
```

### Web Navigation
```
open google.com
go to github.com
browse amazon.com
```

### Web Search
```
search python tutorial
find machine learning courses
google weather today
```

### Memory Management
```
remember my name is John
recall my email
what's my favorite color
forget my password
```

### Multiple Tasks
```
open chrome and search for python
launch discord then open spotify
```

## 🚀 Getting Started

### Requirements
- Windows 7 or later
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ikbenraar128-coder/jarvis-assistant.git
cd jarvis-assistant
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run JARVIS**
```bash
python main.py
```

## 📁 Project Structure

```
jarvis-assistant/
├── core/
│   ├── ai_brain.py           # Intent detection and NLP
│   ├── task_planner.py       # Task planning and orchestration
│   ├── executor.py           # Task execution engine
│   └── memory_manager.py     # Memory and history management
├── tools/
│   ├── app_launcher.py       # Application launching
│   └── browser_control.py    # Browser automation
├── gui/
│   └── interface.py          # Modern tkinter GUI
├── tests/
│   └── __init__.py           # Unit tests
├── main.py                   # Entry point
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

## 🏗️ Architecture

### Components

1. **AI Brain** (`core/ai_brain.py`)
   - Detects user intent from natural language input
   - Supports 12+ intent types
   - Uses regex patterns for intent matching

2. **Task Planner** (`core/task_planner.py`)
   - Creates execution plans from detected intents
   - Breaks down complex tasks into steps
   - Manages task priorities and dependencies

3. **Task Executor** (`core/executor.py`)
   - Executes planned tasks step by step
   - Handles error recovery
   - Provides execution feedback

4. **Memory Manager** (`core/memory_manager.py`)
   - Stores user preferences and information
   - Maintains conversation history
   - Supports JSON-based persistence

5. **Tools**
   - **App Launcher**: Find and launch Windows applications
   - **Browser Control**: Open websites and search the web

6. **GUI** (`gui/interface.py`)
   - Modern dark-themed tkinter interface
   - Real-time command processing
   - Status updates and feedback

## 💻 Usage

### Basic Usage

1. Launch JARVIS: `python main.py`
2. Type your command in the input field
3. Press `Ctrl+Enter` or click the send button
4. JARVIS will process and execute your command

### Example Commands

```
# Open applications
open chrome
open vscode
launch discord

# Close applications
close firefox
quit explorer

# Search and browse
search python tutorials
open google.com
google weather

# Memory management
remember my favorite color is blue
recall my email
what's my name
forget my password
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/ -v
```

Run specific test:
```bash
python -m pytest tests/__init__.py::TestAIBrain::test_intent_open_app -v
```

## 📦 Dependencies

- `psutil` - System and process utilities
- `pytest` - Testing framework

See `requirements.txt` for full list.

## 🔧 Configuration

### Memory Storage

JARVIS stores data in the `memory/` directory:
- `memory.json` - User preferences and information
- `conversation_history.json` - Chat history
- `preferences.json` - Application preferences

### Customization

You can customize:
- Intent patterns in `core/ai_brain.py`
- Application shortcuts in `tools/app_launcher.py`
- GUI theme colors in `gui/interface.py`

## 🐛 Known Limitations

- Windows-only (requires Windows 7+)
- Voice input not yet implemented
- Limited to predefined applications
- No AI model integration yet (uses rule-based matching)

## 🗺️ Roadmap

- [ ] Voice input/output support
- [ ] Integration with real AI models (GPT, etc.)
- [ ] Cross-platform support (macOS, Linux)
- [ ] Scheduled tasks and reminders
- [ ] Advanced context awareness
- [ ] Plugin system for extensibility
- [ ] System tray integration
- [ ] Cloud sync for settings

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Write tests for new features
5. Run tests: `python -m pytest tests/`
6. Commit: `git commit -am 'Add my feature'`
7. Push: `git push origin feature/my-feature`
8. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**ikbenraar128-coder**
- GitHub: [@ikbenraar128-coder](https://github.com/ikbenraar128-coder)
- Email: ikbenraar128@gmail.com

## 🙏 Acknowledgments

- Inspired by the JARVIS AI from Iron Man
- Built with Python and tkinter
- Community contributions and feedback

## 📞 Support

For issues, questions, or suggestions:
- Open an [Issue](https://github.com/ikbenraar128-coder/jarvis-assistant/issues)
- Start a [Discussion](https://github.com/ikbenraar128-coder/jarvis-assistant/discussions)
- Contact via email: ikbenraar128@gmail.com

## 🔐 Security

JARVIS stores user data locally in JSON files. No data is sent to external servers. Be cautious when storing sensitive information.

---

**Made with ❤️ by ikbenraar128-coder**
