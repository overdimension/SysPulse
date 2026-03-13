# SysPulse

**SysPulse** is a modular system monitoring tool for Windows written in Python.  
It collects system metrics such as CPU usage, memory consumption, disk activity, and running processes, and stores them for further analysis.

The project is designed as a **component-based system**, demonstrating principles of software engineering such as modular architecture, extensibility, and clean separation of responsibilities.

This project is developed as part of a university course **"Software Engineering Components"**.

---

# Features

- System metrics collection
- CPU usage monitoring
- Memory usage monitoring
- Disk statistics
- Running processes analysis
- Modular collector architecture
- Configurable data storage
- CLI interface
- Extensible plugin system *(planned)*
- Optional REST API *(planned)*

---

# Architecture

The project follows a **component-based architecture** where each subsystem is responsible for a specific part of functionality.

### Core Components

- **Core** – main monitoring agent and scheduler  
- **Collectors** – modules responsible for gathering system metrics  
- **Storage** – data persistence layer  
- **CLI** – command line interface  
- **Plugins** – extension system for additional collectors  

## Project structure
```text
sys-pulse/
│
├── core/
│ ├── agent.py
│ ├── scheduler.py
│ └── config.py
│
├── collectors/
│ ├── base.py
│ ├── cpu.py
│ ├── memory.py
│ ├── disk.py
│ └── processes.py
│
├── storage/
│ ├── base.py
│ └── memory_storage.py
│
├── cli/
│ └── main.py
│
├── plugins/
│
├── tests/
│
├── requirements.txt
└── README.md
```
This structure allows components to evolve independently and makes the system easy to extend.

---

# Technology Stack

Main technologies used in the project:

- **Python 3**
- **psutil** — system information library
- **Click / Argparse** — command line interface
- **SQLite** — metrics storage *(planned)*
- **Pytest** — testing framework
- **FastAPI** — REST API *(optional feature)*

---

# Installation

Clone the repository:

```bash
git clone https://github.com/overdimension/SysPulse.git
cd SysPulse
