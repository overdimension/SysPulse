# SysPulse

**SysPulse** is a modular system monitoring tool for Windows written in Python.  
It collects system metrics such as CPU usage, memory consumption, disk activity, and running processes, and stores them for further analysis.

The project is designed as a **component-based system**, demonstrating principles of software engineering such as modular architecture, extensibility, and clean separation of responsibilities.

This project is developed as part of a university course **"Software Engineering Components"**.

---

## 🚀 Features

### 📊 Comprehensive Monitoring
Collects data on:
- CPU usage  
- memory (RAM) usage  
- disk space  
- active processes

### 🛡 Fault Tolerance
Each collector is isolated with `try-except`.  
Failure in one component does not affect the entire system.

### ⚖️ Data Normalization
CPU usage is automatically normalized to a **0–100% range** based on the number of logical cores.

### 🧾 Dual Logging System
- **Console** — clean, human-readable dashboard  
- **File** — detailed technical logs (`logs/agent.log`)  

### ⚡ Efficient Data Processing
Uses **Python generators** for streaming process data, minimizing memory usage.

### 🔄 Graceful Shutdown
Proper handling of `Ctrl+C`:
- saves state  
- cleans up resources

---

## 🛠 Architecture

The system follows a component-based architecture:

- **Core** — manages the monitoring loop and error handling  
- **Collectors** — independent sensor modules  
- **Storage** — data persistence layer (supports Dependency Injection)  
- **CLI** — command-line interface

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
│ ├── config.py
│ ├── decorators.py
│ ├── events.py
│ ├── http_client.py
│ └── scheduler.py
│
├── collectors/
│ ├── base.py
│ ├── cpu.py
│ ├── disk.py
│ ├── memory.py
│ └── processes.py
│
├── storage/
│ ├── base.py
│ ├── cloud_storage.py
│ ├── csv_storage.py
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
- **Argparse** — command line interface
- **Logging** — multi-level event logging
- **SQLite** — metrics storage *(planned)*
- **Pytest** — testing framework *(planed)*
- **FastAPI** — REST API *(optional feature)*

---

## 💡 Future Ideas
- **REST API for integrations**
- **Web dashboard**

---

# Installation

Clone the repository:

```bash
git clone https://github.com/overdimension/SysPulse.git
cd SysPulse
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Usage:

```bash
#Default mode (5-second interval)
python -m cli.main

#Custom interval
python -m cli.main --interval 1

#Log analysis mode
python -m cli.main --analyze

#Web-page
python -m cli.main --ui 
(use in another terminal window after starting the main agent loop "python -m cli.main")

#Last Metrics
python -m utils.cloud_viewer view

#Statistics
python -m utils.cloud_viewer stats

#Specific collector's metrics
python -m utils.cloud_viewer collector cpu

#Export to JSON
python -m utils.cloud_viewer export example.json
```
