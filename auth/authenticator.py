"""
===============================================================================
BANANA GAME - ADVANCED CS EDUCATIONAL APPLICATION
Package: auth
File: authenticator.py
Description: Authentication manager, session tracking, and user persistence.

CS THEME COVERAGE:
- Theme 4: Virtual Identity & Role-Based Access Control (RBAC Authenticator)

VIDEO PRESENTATION TALKING POINTS:
1. "The Authenticator module manages active user sessions and identity verification."
2. "We pre-configure mandatory virtual identities:
     - Player Account: Username 'Ada' | Password 'hello23' (Role: PLAYER)
     - Admin Account:  Username 'admin' | Password 'admin123' (Role: ADMIN)"
3. "It provides role-based authentication, updates high scores, and logs all login
   attempts to the AuditLogger to maintain system integrity."
===============================================================================
"""

import json
import os
import hashlib
from typing import Dict, Optional, List
from models.user import User
from auth.user_roles import Role
from models.session_log import audit_logger


class Authenticator:
    """
    Manager class handling authentication, credential validation, user persistence,
    and active session state.
    """

    def __init__(self, users_filepath: str = "users.json") -> None:
        """
        Initialize the Authenticator with user storage.

        Args:
            users_filepath (str): File path for user data persistence.
        """
        self.users_filepath: str = users_filepath
        self.users: Dict[str, User] = {}
        self.current_user: Optional[User] = None
        self._initialize_users()

    def _hash_password(self, password: str) -> str:
        """Helper to create a SHA-256 hash of password for security."""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def _initialize_users(self) -> None:
        """Load existing users from JSON file or seed default accounts."""
        if os.path.exists(self.users_filepath):
            try:
                with open(self.users_filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.users = {
                        uname: User.from_dict(udata)
                        for uname, udata in data.items()
                    }
            except Exception as e:
                print(f"[Authenticator Warning] Failed to load users.json: {e}. Seeding default accounts.")
                self._seed_default_users()
        else:
            self._seed_default_users()

    def _seed_default_users(self) -> None:
        """Seed compulsory default accounts: Ada (Player) and admin (Admin)."""
        self.users = {
            "Ada": User(
                username="Ada",
                password_hash=self._hash_password("hello23"),
                role=Role.PLAYER,
                high_score=10,
                total_games=5,
                total_wins=4
            ),
            "admin": User(
                username="admin",
                password_hash=self._hash_password("admin123"),
                role=Role.ADMIN,
                high_score=0,
                total_games=0,
                total_wins=0
            )
        }
        self.save_users()

    def save_users(self) -> None:
        """Persist user records to JSON file."""
        try:
            with open(self.users_filepath, "w", encoding="utf-8") as f:
                data = {uname: user.to_dict() for uname, user in self.users.items()}
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[Authenticator Error] Failed to save users: {e}")

    def authenticate(self, username: str, password_raw: str) -> Optional[User]:
        """
        Validate username and password, establish session if correct.

        Args:
            username (str): Entered username.
            password_raw (str): Entered plain-text password.

        Returns:
            Optional[User]: Authenticated User object if successful, None otherwise.
        """
        user = self.users.get(username)
        if not user:
            audit_logger.log_event(
                username=username,
                role=Role.PLAYER,
                action="LOGIN_FAILED",
                details="Username not found"
            )
            return None

        hashed_input = self._hash_password(password_raw)
        # Support both hashed comparison and plain text fallback if needed
        if user.password_hash == hashed_input or user.password_hash == password_raw:
            self.current_user = user
            audit_logger.log_event(
                username=user.username,
                role=user.role,
                action="LOGIN_SUCCESS",
                details=f"Logged in as {user.role.value}"
            )
            return user
        else:
            audit_logger.log_event(
                username=username,
                role=user.role,
                action="LOGIN_FAILED",
                details="Invalid password"
            )
            return None

    def logout(self) -> None:
        """Log out the current user session."""
        if self.current_user:
            audit_logger.log_event(
                username=self.current_user.username,
                role=self.current_user.role,
                action="LOGOUT",
                details="User session terminated"
            )
            self.current_user = None

    def register_user(self, username: str, password_raw: str, role: Role = Role.PLAYER) -> tuple[bool, str]:
        """
        Register a new user account (Admin functionality or public signup).

        Args:
            username (str): New username.
            password_raw (str): New password.
            role (Role): Assigned role.

        Returns:
            tuple[bool, str]: (Success boolean, Status message).
        """
        if not username or not password_raw:
            return False, "Username and password cannot be empty."
        if username in self.users:
            return False, "Username already exists."

        new_user = User(
            username=username,
            password_hash=self._hash_password(password_raw),
            role=role
        )
        self.users[username] = new_user
        self.save_users()
        
        audit_logger.log_event(
            username=self.current_user.username if self.current_user else "SYSTEM",
            role=self.current_user.role if self.current_user else Role.ADMIN,
            action="USER_REGISTERED",
            details=f"Created user '{username}' with role '{role.value}'"
        )
        return True, f"User '{username}' registered successfully."

    def reset_user_stats(self, username: str) -> tuple[bool, str]:
        """
        Reset high score and statistics for a player (Admin RBAC capability).

        Args:
            username (str): Target user to reset.

        Returns:
            tuple[bool, str]: (Success boolean, Status message).
        """
        user = self.users.get(username)
        if not user:
            return False, f"User '{username}' not found."

        user.reset_stats()
        self.save_users()
        
        audit_logger.log_event(
            username=self.current_user.username if self.current_user else "ADMIN",
            role=self.current_user.role if self.current_user else Role.ADMIN,
            action="SCORE_RESET",
            details=f"Admin reset scores for player '{username}'"
        )
        return True, f"Scores for '{username}' have been reset to 0."

    def get_all_users(self) -> List[User]:
        """Get a list of all registered users."""
        return list(self.users.values())

    def update_user_high_score(self, username: str, score: int) -> None:
        """Update and persist high score for a user."""
        user = self.users.get(username)
        if user:
            updated = user.update_score(score)
            if updated:
                self.save_users()


# Global authenticator instance
authenticator = Authenticator()
