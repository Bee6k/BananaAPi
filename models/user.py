"""
===============================================================================
BANANA GAME - ADVANCED CS EDUCATIONAL APPLICATION
Package: models
File: user.py
Description: Domain data model representing a User in the system.

CS THEME COVERAGE:
- Theme 1: Version Control & Evolutionary Design (OOP Data Encapsulation)
- Theme 4: Virtual Identity & Role-Based Access Control (RBAC User Entity)

VIDEO PRESENTATION TALKING POINTS:
1. "The User class represents our domain entity for Virtual Identity in Theme 4."
2. "Notice how we encapsulate user state (username, role, high score) and separate
   it cleanly from authentication logic (Authenticator) and UI representation (GUI)."
3. "This follows the Single Responsibility Principle (SRP) and MVC design pattern,
   which is a key evolutionary upgrade over legacy monolithic Java Swing files."
===============================================================================
"""

from typing import Dict, Any
from auth.user_roles import Role


class User:
    """
    Data model representing an authenticated user within the system.

    Attributes:
        username (str): The unique username of the user.
        password_hash (str): The hashed password or password string.
        role (Role): The RBAC role assigned to the user (PLAYER or ADMIN).
        high_score (int): The highest score achieved by the player.
        total_games (int): Total number of puzzle attempts.
        total_wins (int): Total number of correctly solved puzzles.
    """

    def __init__(
        self,
        username: str,
        password_hash: str,
        role: Role,
        high_score: int = 0,
        total_games: int = 0,
        total_wins: int = 0
    ) -> None:
        """
        Initialize a User instance.

        Args:
            username (str): Unique username.
            password_hash (str): Password credentials.
            role (Role): User role (Role.PLAYER or Role.ADMIN).
            high_score (int, optional): Initial high score. Defaults to 0.
            total_games (int, optional): Initial total games. Defaults to 0.
            total_wins (int, optional): Initial total wins. Defaults to 0.
        """
        self.username: str = username
        self.password_hash: str = password_hash
        self.role: Role = role if isinstance(role, Role) else Role(role)
        self.high_score: int = high_score
        self.total_games: int = total_games
        self.total_wins: int = total_wins

    def is_admin(self) -> bool:
        """Check if the user holds an ADMIN role."""
        return self.role == Role.ADMIN

    def is_player(self) -> bool:
        """Check if the user holds a PLAYER role."""
        return self.role == Role.PLAYER

    def update_score(self, current_score: int) -> bool:
        """
        Update player high score if current_score exceeds existing high score.

        Args:
            current_score (int): The player's score from the recent session.

        Returns:
            bool: True if a new high score was set, False otherwise.
        """
        if current_score > self.high_score:
            self.high_score = current_score
            return True
        return False

    def record_game_result(self, is_win: bool, score: int) -> None:
        """Record a completed game puzzle attempt."""
        self.total_games += 1
        if is_win:
            self.total_wins += 1
            self.update_score(score)

    def reset_stats(self) -> None:
        """Reset player statistics (Admin capability)."""
        self.high_score = 0
        self.total_games = 0
        self.total_wins = 0

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize User model to a dictionary format for persistence.

        Returns:
            Dict[str, Any]: JSON-serializable dictionary.
        """
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "role": self.role.value,
            "high_score": self.high_score,
            "total_games": self.total_games,
            "total_wins": self.total_wins
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        """
        Factory method to reconstruct a User instance from a dictionary.

        Args:
            data (Dict[str, Any]): Dictionary containing user attributes.

        Returns:
            User: Deserialized User instance.
        """
        return cls(
            username=data["username"],
            password_hash=data["password_hash"],
            role=Role(data["role"]),
            high_score=data.get("high_score", 0),
            total_games=data.get("total_games", 0),
            total_wins=data.get("total_wins", 0)
        )

    def __repr__(self) -> str:
        return f"<User username='{self.username}', role='{self.role.value}', high_score={self.high_score}>"
