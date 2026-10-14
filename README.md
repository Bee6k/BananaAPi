# Banana Game - Advanced CS Educational Application 🍌

An advanced, production-grade Python desktop application designed to demonstrate four core Computer Science themes.

---

## 📌 Executive Summary & Core CS Themes

This project covers:

1. **Version Control & Evolutionary Design**: Transition from legacy monolithic Java Swing code (`LoginGUI.java` / `GameGUI.java`) into a clean, modular, object-oriented Python architecture following the Model-View-Controller (MVC) pattern.
2. **Event-Driven Programming (GUI Architecture)**: CustomTkinter event-loop architecture with asynchronous worker threads (`threading.Thread`) ensuring non-blocking network calls and real-time control event bindings.
3. **Interoperability (HTTP Protocol & Remote REST API)**: HTTP client interfacing with **Marc Conrad's Banana REST API** (`https://marcconrad.com/uob/banana/api.php`), processing JSON/CSV Base64 binary payloads with offline fallback resilience.
4. **Virtual Identity & Role-Based Access Control (RBAC)**: Comprehensive security system supporting `PLAYER` (e.g., `Ada`) and `ADMIN` (e.g., `admin`) roles, session tracking, score management, and real-time audit trails.

---

## 🏗️ Software Package Structure

```text
banana_game/
│
├── main.py                     # Main application entry point & view router
├── requirements.txt            # Project dependencies (customtkinter, Pillow, requests)
├── README.md                   # System documentation
│
├── auth/                       # Virtual Identity & Security Package
│   ├── __init__.py
│   ├── authenticator.py        # Authentication logic, user persistence & session state
│   └── user_roles.py           # Role definitions (PLAYER vs ADMIN) & RBAC permission predicates
│
├── engine/                     # Game Logic & Interoperability Package
│   ├── __init__.py
│   ├── banana_api.py           # HTTP client interfacing with Marc Conrad's Banana REST API
│   └── game_engine.py          # Puzzle state management, scoring, async thread dispatching
│
├── models/                     # Domain Data Models Package
│   ├── __init__.py
│   ├── user.py                 # User domain entity model (Username, Role, High Score)
│   └── session_log.py          # Security audit trail & action logger
│
├── gui/                        # Event-Driven Interface Package
│   ├── __init__.py
│   ├── login_view.py           # Authentication GUI window with quick demo credentials
│   ├── game_view.py            # Interactive puzzle player window & answer keypad
│   └── admin_view.py           # Admin management dashboard (Audit logs, user management, API health)
│
└── utils/                      # Helper Utilities Package
    ├── __init__.py
    └── image_loader.py         # Base64 string decoding & CustomTkinter image conversion
```

---

## 🔑 Compulsory Virtual Identity Credentials (RBAC)

| Role | Username | Password | Access Capabilities |
|---|---|---|---|
| **PLAYER** | `Ada` | `hello23` | Interactive math puzzle game, score/streak tracking, timer, personal high score, answer keypad. |
| **ADMIN** | `admin` | `admin123` | Admin Dashboard access, user account creation, player score resets, audit trail inspection, API health diagnostics. |

---

## 🚀 Execution & Setup Instructions

### 1. Prerequisites
- Python **3.10+** (Tested on Python 3.12)
- Pip package manager

### 2. Installation
Install project dependencies using `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Launching the Application
Run the entry point script from the project root directory:
```bash
python main.py
```
