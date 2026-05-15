# Attendance & Intelligence System

A sophisticated Django-based Attendance Management System integrated with advanced codebase intelligence tools: **Graphify** and **Project Mapper (Local RAG)**.

---

## 🚀 Core Components

### 1. Attendance Management System (Main App)
A robust Django application designed for enterprise attendance tracking with geographic and network constraints.

- **Employee Lifecycle**: Custom `Employee` model extending Django's Auth, managing profile details and office assignments.
- **Smart Check-In/Out**:
    - **Geofencing**: Attendance only allowed within a specified radius of office coordinates.
    - **IP Restriction**: Restrict check-ins to authorized office networks.
- **Leave Management**: Full workflow for leave requests, approvals, and rejections with automated email notifications.
- **Reporting Engine**: Generates monthly attendance summaries and detailed employee performance reports.
- **Security Hardening**: Integrated with `django-axes` for brute-force protection and account lockout policies.

### 2. Graphify (Codebase Knowledge Graph)
An architectural analysis tool that indexes the entire codebase into a navigable knowledge graph.

- **Dependency Mapping**: Automatically identifies relationships between models, views, and functions.
- **Architectural Auditing**: Helps identify tight coupling, circular dependencies, and "fragile" areas of the project.
- **Visualization**: Generates structured outputs (found in `graphify-out`) used by the intelligence layer to understand project flow.

### 3. Project Mapper (Local RAG Engine)
A state-of-the-art Local Retrieval-Augmented Generation (RAG) system for codebase interaction.

- **LLM Integration**: Powered by local LLMs (e.g., Llama 3 via Ollama) for private, secure code analysis.
- **Hybrid Retrieval**: Combines semantic search with graph-based dependency tracing for high-accuracy answers.
- **Automated Edits**: Support for natural language code modifications (e.g., "replace - def - to - class").
- **Impact Analysis**: Predicts what might break if a specific model or function is modified.
- **Caching**: Efficient query handling using a local hashing-based cache system.

---

## 🛠 Tech Stack

- **Backend**: Django 6.0+, Python
- **Database**: SQLite (Development)
- **Intelligence**: Ollama (Llama 3), Custom Graph-Search Algorithms
- **Security**: Django-Axes, CSRF/XSS Protection
- **Email**: SMTP integration for automated workflows

---

## ⚙️ Setup & Installation

### 1. Project Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

### 2. Intelligence Layer (Project Mapper)
Ensure **Ollama** is running locally with the `llama3` model.
```bash
# Index the project
python project_mapper/auto_indexer.py

# Run the RAG assistant
python project_mapper/local_llm_interface.py
```

---

## 📊 Directory Structure

- `accounts/`: User and Employee model management.
- `attendance/`: Core check-in/out logic and geofencing.
- `leave_management/`: Leave request workflows.
- `reports/`: Data aggregation and report generation.
- `project_mapper/`: Local RAG engine and indexing scripts.
- `graphify-out/`: Knowledge graph artifacts.
- `holidays/`: Public holiday management.
