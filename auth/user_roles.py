"""
===============================================================================
BANANA GAME - ADVANCED CS EDUCATIONAL APPLICATION
Package: auth
File: user_roles.py
Description: Enums and Role-Based Access Control (RBAC) permission logic.

CS THEME COVERAGE:
- Theme 4: Virtual Identity & Role-Based Access Control (RBAC)

VIDEO PRESENTATION TALKING POINTS:
1. "Role-Based Access Control (RBAC) restricts access to authorized users."
2. "Here we define the explicit Role enumeration (PLAYER vs ADMIN) and permission
   predicates that control UI route rendering and administrative operations."
3. "For example, only users with Role.ADMIN can access the Admin Management Dashboard
   or trigger global score resets."
===============================================================================
"""

from enum import Enum


class Role(str, Enum):
    """
    Enumeration defining supported system roles for Role-Based Access Control.
    """
    PLAYER = "PLAYER"
    ADMIN = "ADMIN"

    def __str__(self) -> str:
        return self.value


def can_access_admin_dashboard(role: Role) -> bool:
    """
    Determine if a given role has permissions to open the Admin Dashboard.

    Args:
        role (Role): The user's role.

    Returns:
        bool: True if ADMIN, False otherwise.
    """
    return role == Role.ADMIN


def can_play_game(role: Role) -> bool:
    """
    Determine if a given role can play the interactive puzzle game.

    Args:
        role (Role): The user's role.

    Returns:
        bool: True for both PLAYER and ADMIN (admins can test play).
    """
    return role in (Role.PLAYER, Role.ADMIN)


def get_role_badge_color(role: Role) -> str:
    """
    Get the hex color code for UI role status badges.

    Args:
        role (Role): The user's role.

    Returns:
        str: Hex color code (#E94560 for ADMIN, #2ECC71 for PLAYER).
    """
    if role == Role.ADMIN:
        return "#E94560"  # Vibrant Red/Crimson for Admin
    return "#2ECC71"      # Emerald Green for Player
