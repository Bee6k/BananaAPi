"""
===============================================================================
BANANA GAME - ADVANCED CS EDUCATIONAL APPLICATION
Package: models
File: session_log.py
Description: Session audit logger for recording system actions and user security events.

CS THEME COVERAGE:
- Theme 4: Virtual Identity & Role-Based Access Control (Security Audit Trail)

VIDEO PRESENTATION TALKING POINTS:
1. "Security compliance requires an unalterable audit log of user activity."
2. "The AuditLogger records security and gameplay events (logins, solution submissions,
   score resets) with exact ISO timestamps, username, role, and action context."
3. "Admins can inspect, filter, and review this trail in real-time from the Admin View."
===============================================================================
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from auth.user_roles import Role


class AuditLogEntry:
    """
    Model representing a single audit log entry.
    """

    def __init__(
        self,
        username: str,
        role: str,
        action: str,
        details: str = "",
        timestamp: Optional[str] = None
    ) -> None:
        self.timestamp: str = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.username: str = username
        self.role: str = role
        self.action: str = action
        self.details: str = details

    def to_dict(self) -> Dict[str, Any]:
        """Convert entry to dictionary for JSON persistence."""
        return {
            "timestamp": self.timestamp,
            "username": self.username,
            "role": self.role,
            "action": self.action,
            "details": self.details
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AuditLogEntry":
        """Factory method to recreate AuditLogEntry from dictionary."""
        return cls(
            username=data.get("username", "Unknown"),
            role=data.get("role", "PLAYER"),
            action=data.get("action", "UNKNOWN"),
            details=data.get("details", ""),
            timestamp=data.get("timestamp")
        )

    def __repr__(self) -> str:
        return f"[{self.timestamp}] {self.username} ({self.role}): {self.action} - {self.details}"


class AuditLogger:
    """
    Manager class for recording and persisting system audit logs.
    """

    def __init__(self, log_filepath: str = "session_logs.json") -> None:
        """
        Initialize the AuditLogger with a target persistence file.

        Args:
            log_filepath (str): Filepath to save audit logs.
        """
        self.log_filepath: str = log_filepath
        self.logs: List[AuditLogEntry] = []
        self.load_logs()

    def load_logs(self) -> None:
        """Load persistent logs from JSON file if available."""
        if os.path.exists(self.log_filepath):
            try:
                with open(self.log_filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.logs = [AuditLogEntry.from_dict(entry) for entry in data]
            except Exception:
                self.logs = []
        else:
            self.logs = []

    def save_logs(self) -> None:
        """Save in-memory logs to JSON file."""
        try:
            with open(self.log_filepath, "w", encoding="utf-8") as f:
                json.dump([entry.to_dict() for entry in self.logs], f, indent=2)
        except Exception as e:
            print(f"[AuditLogger Error] Failed to save logs: {e}")

    def log_event(self, username: str, role: Role, action: str, details: str = "") -> None:
        """
        Record a new security or system action event.

        Args:
            username (str): Username triggering the action.
            role (Role): Role of the user.
            action (str): Category/type of action (e.g., 'LOGIN_SUCCESS', 'PUZZLE_SOLVED').
            details (str): Contextual detail string.
        """
        role_str = role.value if isinstance(role, Role) else str(role)
        entry = AuditLogEntry(username=username, role=role_str, action=action, details=details)
        self.logs.insert(0, entry)  # Prepend newest logs first
        self.save_logs()

    def get_all_logs(self) -> List[AuditLogEntry]:
        """Get all audit log entries."""
        return self.logs

    def filter_logs(self, username: Optional[str] = None, action: Optional[str] = None) -> List[AuditLogEntry]:
        """
        Filter log entries by username or action keyword.

        Args:
            username (Optional[str]): Filter by matching username.
            action (Optional[str]): Filter by matching action string.

        Returns:
            List[AuditLogEntry]: Filtered log entries.
        """
        filtered = self.logs
        if username:
            filtered = [e for e in filtered if username.lower() in e.username.lower()]
        if action:
            filtered = [e for e in filtered if action.lower() in e.action.lower()]
        return filtered

    def clear_logs(self) -> None:
        """Clear all audit logs (Admin option)."""
        self.logs.clear()
        self.save_logs()


# Global audit logger instance
audit_logger = AuditLogger()
