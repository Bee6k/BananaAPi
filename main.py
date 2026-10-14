"""
===============================================================================
BANANA GAME - ADVANCED CS EDUCATIONAL APPLICATION
Main Entry Point File: main.py
Description: Desktop application entry point initializing CustomTkinter GUI window,
             screen view routing, and event controller loop.

CS THEME COVERAGE:
1. Version Control & Evolutionary Design: Modular Python package structure replacing
   legacy monolithic Java Swing (LoginGUI.java / GameGUI.java).
2. Event-Driven Programming: CustomTkinter mainloop GUI architecture with non-blocking threads.
3. Interoperability: HTTP Client querying Marc Conrad's Banana REST API.
4. Virtual Identity: Role-Based Access Control (PLAYER vs ADMIN views).

VIDEO PRESENTATION TALKING POINTS:
1. "Welcome to the Banana Game - Advanced CS Educational Application."
2. "This application serves as a comprehensive 10-minute presentation project covering
   our four core Computer Science themes."
3. "Here in main.py, we initialize the main CustomTkinter window and manage clean screen routing
   between the LoginView, GameView, and AdminView using the Observer pattern."
===============================================================================
"""

import sys
import os

# Ensure project root directory is in sys.path for clean package imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from auth.authenticator import authenticator
from auth.user_roles import Role, can_access_admin_dashboard
from models.user import User
from gui.login_view import LoginView
from gui.game_view import GameView
from gui.admin_view import AdminView


class BananaGameApp(ctk.CTk):
    """
    Main Desktop Application Window controlling screen navigation routes and global GUI theme settings.
    """

    def __init__(self) -> None:
        """Initialize the main CustomTkinter application window."""
        super().__init__()

        # Window Branding & Configuration
        self.title("Banana Game - Advanced CS Educational Application")
        self.geometry("1024x720")
        self.minsize(900, 650)

        # Set Appearance Theme (Dark mode by default, customizable)
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Container Frame for View Swapping
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.current_view: ctk.CTkFrame = None

        # Start with Login Screen
        self.show_login_view()

    def clear_current_view(self) -> None:
        """Destroy the active view frame before rendering a new screen route."""
        if self.current_view is not None:
            self.current_view.destroy()
            self.current_view = None

    def show_login_view(self) -> None:
        """Render the Authentication & Virtual Identity Login Screen."""
        self.clear_current_view()
        self.current_view = LoginView(
            parent=self.container,
            on_login_success=self.on_login_success
        )
        self.current_view.pack(fill="both", expand=True)

    def on_login_success(self, user: User) -> None:
        """
        Route user to appropriate screen based on Role-Based Access Control (RBAC).

        Args:
            user (User): Authenticated user instance.
        """
        if user.is_admin():
            self.show_admin_view()
        else:
            self.show_game_view()

    def show_game_view(self) -> None:
        """Render the Interactive Math Puzzle Game Player Screen."""
        self.clear_current_view()
        self.current_view = GameView(
            parent=self.container,
            on_logout=self.show_login_view,
            on_open_admin=self.show_admin_view
        )

    def show_admin_view(self) -> None:
        """
        Render the Admin Management Dashboard Screen (Enforces Role.ADMIN RBAC).
        """
        user = authenticator.current_user
        if not user or not can_access_admin_dashboard(user.role):
            # Security Enforcement: Reject non-admins
            self.show_game_view()
            return

        self.clear_current_view()
        self.current_view = AdminView(
            parent=self.container,
            on_logout=self.show_login_view,
            on_back_to_game=self.show_game_view
        )


def main() -> None:
    """Application Launch Entry Point."""
    app = BananaGameApp()
    app.mainloop()


if __name__ == "__main__":
    main()
