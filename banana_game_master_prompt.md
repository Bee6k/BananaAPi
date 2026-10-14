# Master Prompt: Python 'Banana Game' Educational Software Project

Use the following detailed prompt when instructing an AI agent or developer to build the complete Python **Banana Game** assignment application.

---

```markdown
You are an expert Senior Python Software Architect. Your task is to design, structure, and implement a complete, production-grade desktop application in Python called **"Banana Game - Advanced CS Educational Application"**. 

This application serves as the core practical project for a 10-minute video presentation covering four fundamental Computer Science themes:
1. **Version Control & Evolutionary Design**
2. **Event-Driven Programming (GUI Architecture)**
3. **Interoperability (HTTP Protocol & Remote REST API)**
4. **Virtual Identity & Role-Based Access Control (RBAC)**

---

### Key Requirements & Technical Specification

#### 1. Software Architecture & Package Structure
Organize the project into clean, modular Python packages following industry best practices:

```text
banana_game/
│
├── main.py                     # Entry point for the application
├── requirements.txt            # Project dependencies (requests, Pillow, customtkinter / tkinter)
├── README.md                   # System documentation & execution instructions
│
├── auth/                       # Virtual Identity & Security Package
│   ├── __init__.py
│   ├── authenticator.py        # Authentication logic & session tracking
│   └── user_roles.py           # Role definitions (ADMIN vs PLAYER)
│
├── engine/                     # Game Logic & Interoperability Package
│   ├── __init__.py
│   ├── banana_api.py           # HTTP client interfacing with Marc Conrad's Banana API
│   └── game_engine.py          # Puzzle state management, scoring, and solution verification
│
├── models/                     # Domain Data Models Package
│   ├── __init__.py
│   ├── user.py                 # User data model (Username, Role, High Score)
│   └── session_log.py          # Session and audit trail logger
│
├── gui/                        # Event-Driven Interface Package
│   ├── __init__.py
│   ├── login_view.py           # Authentication GUI window
│   ├── game_view.py            # Interactive puzzle player window
│   └── admin_view.py           # Admin management dashboard window
│
└── utils/                      # Helper Utilities Package
    ├── __init__.py
    └── image_loader.py         # Base64 string to PIL/Tkinter image converter
```

---

#### 2. Four CS Core Themes Implementation Details

##### Theme 1: Version Control & Evolutionary Design
- Model the codebase as an upgraded, modular Python evolution of the legacy Java Tomato Game (`LoginGUI.java` / `GameGUI.java`).
- Document key refactoring decisions (e.g., transition from Java Swing to Python Event-Driven Tkinter/CustomTkinter, separation of concerns into distinct packages).

##### Theme 2: Event-Driven Programming
- Implement an explicit Event Loop using `Tkinter` / `CustomTkinter` or `PyQt`.
- Bind UI controls (Login button, Number buttons 0-9, Reset button, Logout) to explicit event handlers.
- Handle asynchronous network loading gracefully so the GUI thread never freezes during HTTP API calls.

##### Theme 3: Interoperability (HTTP API Integration)
- Interface with the official **Marc Conrad Banana API**:
  - Endpoint: `https://marcconrad.com/uob/banana/api.php?out=csv&base64=yes` (or `out=json`).
  - Request format: Standard HTTP GET request.
  - Payload processing: Parse CSV/JSON output, extract the Base64 image payload or image URL, decode binary data using `base64` and `PIL.Image`, and parse the integer `solution`.
  - Robust exception handling: Gracefully manage HTTP 500 errors, network timeouts, and invalid API responses.

##### Theme 4: Virtual Identity (Authentication & RBAC)
- Support multiple pre-configured user credentials:
  - **Player Account:** `Username: Ada` | `Password: hello23` (Role: `PLAYER`)
  - **Admin Account:** `Username: admin` | `Password: admin123` (Role: `ADMIN`)
- **Role-Based Behavior:**
  - **PLAYER Role:** Accesses the interactive math puzzle game interface, views their individual score, tracks timer, and submits answers.
  - **ADMIN Role:** Accesses a specialized **Admin Dashboard** allowing system logging review, user activity inspection, player score resets, and global game statistics.

---

#### 3. Visual Aesthetics & UI Design
- Use a modern dark/light mode palette (sleek card containers, styled buttons, high-contrast typography, smooth spacing).
- Responsive layout that auto-centers image equations, displays user status badges, and renders clear score indicators.

---

#### 4. Code Comments & Presentation Readiness
- **Extensive Code Comments:** Provide clear, line-by-line docstrings and inline comments across all files explaining:
  - How event binding works (`@event_handler`).
  - How HTTP requests interoperate with external services.
  - How virtual identity context switches user views.
  - How OOP design patterns (Factory, Singleton, MVC/Observer) are used.
- Include explicit **"VIDEO PRESENTATION TALKING POINTS"** in docstrings to assist the student in explaining their code during the 10-minute presentation.
```
