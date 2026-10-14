# Banana Game - Advanced CS Educational Application 🍌

An advanced, production-grade Python desktop application designed to demonstrate four core Computer Science themes for a 10-minute educational video presentation.

---

## 📌 Executive Summary & Core CS Themes

This project serves as the practical implementation for a 10-minute video presentation covering:

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
├── README.md                   # System documentation & presentation script
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

---

## 🎬 10-Minute Video Presentation Talking Points & Script

Use this structured breakdown when recording your 10-minute presentation video:

### ⏱️ Minute 0:00 - 02:00: Project Introduction & Theme 1 (Evolutionary Design)
- **Concept:** Explain how the legacy Java Swing app (`LoginGUI.java` / `GameGUI.java`) was refactored into a modular Python application.
- **Key Point:** Highlight separation of concerns into distinct packages (`auth`, `engine`, `models`, `gui`, `utils`).
- **Code Reference:** Point to `models/user.py` and `main.py` demonstrating OOP encapsulation.

### ⏱️ Minute 02:00 - 04:00: Theme 2 (Event-Driven GUI Architecture)
- **Concept:** Explain CustomTkinter event loops, callback bindings, and asynchronous multithreading.
- **Key Point:** Demonstrate how keypad buttons (0-9) and physical keyboard inputs bind to event handlers in `gui/game_view.py`. Show that fetching new puzzle images uses background threads (`engine/game_engine.py`) so the UI never freezes.

### ⏱️ Minute 04:00 - 07:00: Theme 3 (Interoperability & REST API)
- **Concept:** Discuss HTTP protocol integration with Marc Conrad's Banana API (`https://marcconrad.com/uob/banana/api.php`).
- **Key Point:** Open `engine/banana_api.py`. Show how JSON/CSV responses containing Base64 binary strings are decoded with PIL and rendered seamlessly. Demonstrate the offline fallback equation generator.

### ⏱️ Minute 07:00 - 09:00: Theme 4 (Virtual Identity & RBAC Admin Dashboard)
- **Concept:** Explain Virtual Identity verification and Role-Based Access Control.
- **Key Point:** Log in as `Ada` (PLAYER) to show game functionality, then log in as `admin` (ADMIN) to reveal the Admin Dashboard (`gui/admin_view.py`). Show score resets, registration of new accounts, real-time audit logs (`models/session_log.py`), and API health ping diagnostics.

### ⏱️ Minute 09:00 - 10:00: Live Demo & Conclusion
- **Concept:** Solve a live equation puzzle, score points, check high score update, and summarize learning outcomes.
