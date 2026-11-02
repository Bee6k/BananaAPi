# Future Development Roadmap (Post-Week 8 Milestones) 🚀

This document outlines planned enhancements for subsequent development phases following the **Week 8 Working Prototype** presentation.

---

## 📌 Planned Enhancements

### 1. Database Migration & Persistence
- [ ] Migrate local JSON persistence (`users.json`, `session_logs.json`) to **SQLite** / **PostgreSQL** relational database.
- [ ] Implement an ORM layer using **SQLAlchemy** for structured database models and transactions.

### 2. Advanced Security & Session Management
- [ ] Upgrade SHA-256 password hashing to salted **bcrypt** or **argon2**.
- [ ] Implement expiring session tokens (JSON Web Tokens - JWT) for enhanced session security.

### 3. Audio & Sensory Feedback
- [ ] Add sound effects for correct answer chimes, wrong answer buzzers, and timer countdown ticks.
- [ ] Provide toggleable sound settings in the user interface.

### 4. Global Multiplayer & Cloud Leaderboards
- [ ] Implement real-time WebSocket connection for live 1v1 puzzle battles.
- [ ] Cloud-synchronized global high scores with daily, weekly, and all-time rankings.
