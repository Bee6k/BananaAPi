"""
===============================================================================
BANANA GAME - ADVANCED CS EDUCATIONAL APPLICATION
Package: gui
File: login_view.py
Description: Authentication and Virtual Identity login View built with CustomTkinter.

CS THEME COVERAGE:
- Theme 2: Event-Driven Programming (UI Events & Control Binding)
- Theme 4: Virtual Identity (Authentication Gate)

VIDEO PRESENTATION TALKING POINTS:
1. "The LoginView serves as the Virtual Identity entry point for Theme 4."
2. "Notice the clean Event-Driven Architecture (Theme 2): buttons are explicitly bound
   to event handlers like 'on_login_click' and key bindings like '<Return>'."
3. "We include Quick-Login shortcuts for compulsory project credentials:
     - Player Account (Ada / hello23)
     - Admin Account (admin / admin123)"
===============================================================================
"""

import customtkinter as ctk
from typing import Callable, Optional
from auth.authenticator import authenticator
from auth.user_roles import Role
from models.user import User


class LoginView(ctk.CTkFrame):
    """
    CustomTkinter Frame providing user authentication and identity verification interface.
    """

    def __init__(
        self,
        parent: ctk.CTk,
        on_login_success: Callable[[User], None]
    ) -> None:
        """
        Initialize the LoginView.

        Args:
            parent (ctk.CTk): Main application container window.
            on_login_success (Callable[[User], None]): Callback triggered upon valid login.
        """
        super().__init__(parent, fg_color="transparent")
        self.parent: ctk.CTk = parent
        self.on_login_success_callback: Callable[[User], None] = on_login_success

        self._build_ui()

    def _build_ui(self) -> None:
        """Construct visual card layout, input fields, and event bindings."""
        # Main Grid Centering
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Card Container Frame
        self.card = ctk.CTkFrame(
            self,
            fg_color=("#F0F3F4", "#16213E"),
            corner_radius=20,
            border_width=2,
            border_color="#F1C40F"
        )
        self.card.grid(row=1, column=1, padx=40, pady=40, sticky="nsew")

        # Header Title
        self.title_label = ctk.CTkLabel(
            self.card,
            text="🍌 BANANA GAME",
            font=ctk.CTkFont(family="Helvetica", size=32, weight="bold"),
            text_color="#F1C40F"
        )
        self.title_label.pack(padx=30, pady=(30, 5))

        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.card,
            text="Advanced CS Educational Application",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            text_color=("#7F8C8D", "#BDC3C7")
        )
        self.subtitle_label.pack(padx=30, pady=(0, 20))

        # CS Theme Badges
        self.badge_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.badge_frame.pack(pady=(0, 20))

        badges = ["Git Evolution", "Event GUI", "REST API", "Virtual Identity (RBAC)"]
        for b in badges:
            lbl = ctk.CTkLabel(
                self.badge_frame,
                text=f"• {b} ",
                font=ctk.CTkFont(size=11),
                text_color="#3498DB"
            )
            lbl.pack(side="left", padx=4)

        # Username Field
        self.username_entry = ctk.CTkEntry(
            self.card,
            placeholder_text="Username",
            width=300,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(size=14)
        )
        self.username_entry.pack(pady=10)
        self.username_entry.bind("<Return>", lambda event: self.on_login_click())

        # Password Field
        self.password_entry = ctk.CTkEntry(
            self.card,
            placeholder_text="Password",
            show="•",
            width=300,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(size=14)
        )
        self.password_entry.pack(pady=10)
        self.password_entry.bind("<Return>", lambda event: self.on_login_click())

        # Status / Error Banner Label
        self.status_label = ctk.CTkLabel(
            self.card,
            text="",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#E74C3C"
        )
        self.status_label.pack(pady=5)

        # Login Submit Button
        self.login_btn = ctk.CTkButton(
            self.card,
            text="🔐 LOGIN TO SYSTEM",
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#F1C40F",
            hover_color="#D4AC0D",
            text_color="#1A1A2E",
            width=300,
            height=45,
            corner_radius=10,
            command=self.on_login_click
        )
        self.login_btn.pack(pady=(10, 20))

        # Divider
        divider = ctk.CTkFrame(self.card, height=2, fg_color=("#BDC3C7", "#2C3E50"))
        divider.pack(fill="x", padx=30, pady=10)

        # Demo Quick Login Section Title
        demo_title = ctk.CTkLabel(
            self.card,
            text="⚡ Quick Demo Credentials (RBAC Roles):",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("#34495E", "#ECF0F1")
        )
        demo_title.pack(pady=(5, 10))

        # Quick Login Buttons Container
        self.quick_btn_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.quick_btn_frame.pack(pady=(0, 25))

        # Ada Player Button
        self.quick_player_btn = ctk.CTkButton(
            self.quick_btn_frame,
            text="👤 Ada (PLAYER)",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#2ECC71",
            hover_color="#27AE60",
            width=140,
            height=35,
            corner_radius=8,
            command=lambda: self._quick_login("Ada", "hello23")
        )
        self.quick_player_btn.pack(side="left", padx=5)

        # Admin Button
        self.quick_admin_btn = ctk.CTkButton(
            self.quick_btn_frame,
            text="🔑 admin (ADMIN)",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#E94560",
            hover_color="#C0392B",
            width=140,
            height=35,
            corner_radius=8,
            command=lambda: self._quick_login("admin", "admin123")
        )
        self.quick_admin_btn.pack(side="left", padx=5)

    def on_login_click(self) -> None:
        """Event Handler triggered when user clicks Login or presses Enter key."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.status_label.configure(
                text="⚠️ Please enter both Username and Password.",
                text_color="#E74C3C"
            )
            return

        user = authenticator.authenticate(username, password)
        if user:
            self.status_label.configure(
                text=f"✅ Welcome {user.username}! Redirecting...",
                text_color="#2ECC71"
            )
            self.after(400, lambda: self.on_login_success_callback(user))
        else:
            self.status_label.configure(
                text="❌ Invalid Username or Password. Try 'Ada' / 'hello23'.",
                text_color="#E74C3C"
            )

    def _quick_login(self, uname: str, pword: str) -> None:
        """Helper to pre-fill and automatically authenticate demo accounts."""
        self.username_entry.delete(0, "end")
        self.username_entry.insert(0, uname)
        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, pword)
        self.on_login_click()
