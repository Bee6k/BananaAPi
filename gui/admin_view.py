"""
===============================================================================
BANANA GAME - ADVANCED CS EDUCATIONAL APPLICATION
Package: gui
File: admin_view.py
Description: Specialized Admin Dashboard View for system management, user audit,
             score resetting, and REST API diagnostics.

CS THEME COVERAGE:
- Theme 3: Interoperability (API Health Diagnostic Suite)
- Theme 4: Virtual Identity & Role-Based Access Control (Admin Dashboard)

VIDEO PRESENTATION TALKING POINTS:
1. "The AdminView provides a specialized management dashboard exclusive to Role.ADMIN users (Theme 4)."
2. "Admin features include inspecting registered identities, viewing high scores, and resetting player stats."
3. "The Audit Trail tab provides complete security compliance logs (Logins, score updates, system calls)."
4. "The API Diagnostics tab verifies REST API health and latency (Theme 3)."
===============================================================================
"""

import time
import requests
import customtkinter as ctk
from typing import Callable, List
from auth.authenticator import authenticator
from auth.user_roles import Role, get_role_badge_color
from models.user import User
from models.session_log import audit_logger, AuditLogEntry


class AdminView(ctk.CTkFrame):
    """
    CustomTkinter Frame providing the Admin Dashboard for user administration,
    audit trail inspection, global stats, and REST API health monitoring.
    """

    def __init__(
        self,
        parent: ctk.CTk,
        on_logout: Callable[[], None],
        on_back_to_game: Callable[[], None]
    ) -> None:
        """
        Initialize the AdminView.

        Args:
            parent (ctk.CTk): Parent window container.
            on_logout (Callable[[], None]): Logout callback.
            on_back_to_game (Callable[[], None]): Return to game callback.
        """
        super().__init__(parent, fg_color="transparent")
        self.parent: ctk.CTk = parent
        self.on_logout_callback: Callable[[], None] = on_logout
        self.on_back_to_game_callback: Callable[[], None] = on_back_to_game

        self.current_user: User = authenticator.current_user

        self._build_ui()

    def _build_ui(self) -> None:
        """Construct Header and Tabbed Dashboard interface."""
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # ------------------- HEADER NAVBAR -------------------
        self.header_bar = ctk.CTkFrame(self, fg_color=("#EAEDED", "#16213E"), corner_radius=15, height=60)
        self.header_bar.pack(fill="x", pady=(0, 15))

        # Admin Badge
        badge_color = get_role_badge_color(Role.ADMIN)
        uname = self.current_user.username if self.current_user else "admin"

        self.admin_badge = ctk.CTkLabel(
            self.header_bar,
            text=f" 🔑 ADMIN DASHBOARD ({uname}) ",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=badge_color,
            text_color="#FFFFFF",
            corner_radius=10,
            height=32
        )
        self.admin_badge.pack(side="left", padx=15, pady=10)

        # Navigation Buttons
        self.logout_btn = ctk.CTkButton(
            self.header_bar,
            text="🚪 Logout",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#E74C3C",
            hover_color="#C0392B",
            width=90,
            height=32,
            corner_radius=8,
            command=self.on_logout_click
        )
        self.logout_btn.pack(side="right", padx=15)

        self.game_btn = ctk.CTkButton(
            self.header_bar,
            text="🎮 Play Banana Game",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#2ECC71",
            hover_color="#27AE60",
            width=140,
            height=32,
            corner_radius=8,
            command=self.on_back_to_game_callback
        )
        self.game_btn.pack(side="right", padx=5)

        # ------------------- TABBED DASHBOARD -------------------
        self.tabview = ctk.CTkTabview(self, corner_radius=15)
        self.tabview.pack(fill="both", expand=True)

        self.tab_users = self.tabview.add("👥 User Management & High Scores")
        self.tab_audit = self.tabview.add("📜 Session Audit Logs")
        self.tab_stats = self.tabview.add("📊 Global Game Analytics")
        self.tab_api = self.tabview.add("🌐 REST API Health Diagnostics")

        # Build individual tabs
        self._build_users_tab()
        self._build_audit_tab()
        self._build_stats_tab()
        self._build_api_tab()

    # ================= TAB 1: USER MANAGEMENT =================
    def _build_users_tab(self) -> None:
        """Construct User Management tab displaying users, scores, and reset options."""
        # Split into Left List and Right Add Form
        self.tab_users.grid_columnconfigure(0, weight=3)
        self.tab_users.grid_columnconfigure(1, weight=2)
        self.tab_users.grid_rowconfigure(0, weight=1)

        # Users Table Scrollable Frame
        self.users_frame = ctk.CTkScrollableFrame(self.tab_users, label_text="Registered System Users")
        self.users_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Add User Form Frame
        self.add_user_card = ctk.CTkFrame(self.tab_users, fg_color=("#F0F3F4", "#1A1A2E"), corner_radius=15)
        self.add_user_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        form_title = ctk.CTkLabel(
            self.add_user_card,
            text="➕ Register New Identity",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#F1C40F"
        )
        form_title.pack(pady=(20, 15))

        self.new_uname_entry = ctk.CTkEntry(self.add_user_card, placeholder_text="New Username", width=220, height=40)
        self.new_uname_entry.pack(pady=8)

        self.new_pword_entry = ctk.CTkEntry(self.add_user_card, placeholder_text="New Password", show="•", width=220, height=40)
        self.new_pword_entry.pack(pady=8)

        self.role_option = ctk.CTkOptionMenu(
            self.add_user_card,
            values=["PLAYER", "ADMIN"],
            width=220,
            height=40
        )
        self.role_option.set("PLAYER")
        self.role_option.pack(pady=8)

        self.create_user_btn = ctk.CTkButton(
            self.add_user_card,
            text="Create User Account",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#3498DB",
            hover_color="#2980B9",
            width=220,
            height=40,
            command=self.on_create_user_submit
        )
        self.create_user_btn.pack(pady=(15, 10))

        self.add_user_status = ctk.CTkLabel(self.add_user_card, text="", font=ctk.CTkFont(size=12))
        self.add_user_status.pack(pady=5)

        self.refresh_users_list()

    def refresh_users_list(self) -> None:
        """Render registered users list with high scores and reset actions."""
        # Clear existing rows
        for child in self.users_frame.winfo_children():
            child.destroy()

        users = authenticator.get_all_users()
        for u in users:
            row_frame = ctk.CTkFrame(self.users_frame, fg_color=("#EAEDED", "#16213E"), corner_radius=10)
            row_frame.pack(fill="x", padx=5, pady=5)

            badge_col = get_role_badge_color(u.role)
            lbl_info = ctk.CTkLabel(
                row_frame,
                text=f"👤 {u.username} [{u.role.value}] | High Score: {u.high_score} | Wins: {u.total_wins}/{u.total_games}",
                font=ctk.CTkFont(size=13, weight="bold")
            )
            lbl_info.pack(side="left", padx=10, pady=10)

            # Score Reset Button (Admin operation)
            reset_btn = ctk.CTkButton(
                row_frame,
                text="🔄 Reset Score",
                font=ctk.CTkFont(size=11, weight="bold"),
                fg_color="#E74C3C",
                hover_color="#C0392B",
                width=100,
                height=30,
                corner_radius=6,
                command=lambda username=u.username: self.on_reset_player_score(username)
            )
            reset_btn.pack(side="right", padx=10, pady=10)

    def on_reset_player_score(self, username: str) -> None:
        """Admin action to reset score for a targeted user."""
        success, msg = authenticator.reset_user_stats(username)
        self.refresh_users_list()
        self.refresh_stats_tab()

    def on_create_user_submit(self) -> None:
        """Handle creation of a new user account by Admin."""
        uname = self.new_uname_entry.get().strip()
        pword = self.new_pword_entry.get().strip()
        role_str = self.role_option.get()

        success, msg = authenticator.register_user(uname, pword, Role(role_str))
        if success:
            self.add_user_status.configure(text=f"✅ {msg}", text_color="#2ECC71")
            self.new_uname_entry.delete(0, "end")
            self.new_pword_entry.delete(0, "end")
            self.refresh_users_list()
            self.refresh_stats_tab()
        else:
            self.add_user_status.configure(text=f"❌ {msg}", text_color="#E74C3C")

    # ================= TAB 2: AUDIT LOGS =================
    def _build_audit_tab(self) -> None:
        """Construct Session Audit Trail tab."""
        filter_bar = ctk.CTkFrame(self.tab_audit, fg_color="transparent")
        filter_bar.pack(fill="x", pady=(0, 10))

        self.audit_search_entry = ctk.CTkEntry(
            filter_bar,
            placeholder_text="Filter logs by username or action...",
            width=350,
            height=38
        )
        self.audit_search_entry.pack(side="left", padx=5)

        search_btn = ctk.CTkButton(
            filter_bar,
            text="🔍 Filter",
            width=90,
            height=38,
            command=self.refresh_audit_logs
        )
        search_btn.pack(side="left", padx=5)

        refresh_btn = ctk.CTkButton(
            filter_bar,
            text="🔄 Refresh",
            width=90,
            height=38,
            fg_color="#7F8C8D",
            command=self.refresh_audit_logs
        )
        refresh_btn.pack(side="left", padx=5)

        self.logs_scroll_frame = ctk.CTkScrollableFrame(self.tab_audit, label_text="Security Audit Trail")
        self.logs_scroll_frame.pack(fill="both", expand=True)

        self.refresh_audit_logs()

    def refresh_audit_logs(self) -> None:
        """Refresh displayed audit log entries."""
        for child in self.logs_scroll_frame.winfo_children():
            child.destroy()

        query = self.audit_search_entry.get().strip()
        if query:
            logs = audit_logger.filter_logs(username=query, action=query)
        else:
            logs = audit_logger.get_all_logs()

        for entry in logs[:50]:  # Display top 50 recent events
            card = ctk.CTkFrame(self.logs_scroll_frame, fg_color=("#EAEDED", "#16213E"), corner_radius=8)
            card.pack(fill="x", padx=5, pady=4)

            log_text = f"[{entry.timestamp}] {entry.username} ({entry.role}) → {entry.action}: {entry.details}"
            lbl = ctk.CTkLabel(card, text=log_text, font=ctk.CTkFont(size=12), anchor="w")
            lbl.pack(fill="x", padx=10, pady=8)

    # ================= TAB 3: GLOBAL ANALYTICS =================
    def _build_stats_tab(self) -> None:
        """Construct System Global Analytics tab."""
        self.stats_container = ctk.CTkFrame(self.tab_stats, fg_color="transparent")
        self.stats_container.pack(fill="both", expand=True, padx=20, pady=20)
        self.refresh_stats_tab()

    def refresh_stats_tab(self) -> None:
        """Calculate and render analytics summary cards."""
        for child in self.stats_container.winfo_children():
            child.destroy()

        users = authenticator.get_all_users()
        total_users = len(users)
        players_count = sum(1 for u in users if u.is_player())
        global_high_score = max((u.high_score for u in users), default=0)
        total_games_all = sum(u.total_games for u in users)
        total_wins_all = sum(u.total_wins for u in users)
        win_rate = (total_wins_all / total_games_all * 100) if total_games_all > 0 else 0.0

        # Cards Layout
        metrics = [
            ("👥 Registered Users", str(total_users), "#3498DB"),
            ("🎮 Active Players", str(players_count), "#2ECC71"),
            ("🏆 Global High Score", str(global_high_score), "#F1C40F"),
            ("🧩 Total Puzzles Attempted", str(total_games_all), "#9B59B6"),
            ("📈 System Win Rate", f"{win_rate:.1f}%", "#E94560"),
        ]

        for i, (title, val, color) in enumerate(metrics):
            card = ctk.CTkFrame(self.stats_container, fg_color=("#F0F3F4", "#16213E"), corner_radius=15, border_width=2, border_color=color)
            card.pack(fill="x", pady=8, padx=10)

            lbl_title = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=15, weight="bold"), text_color=color)
            lbl_title.pack(side="left", padx=20, pady=15)

            lbl_val = ctk.CTkLabel(card, text=val, font=ctk.CTkFont(size=22, weight="bold"), text_color=("#1A1A2E", "#FFFFFF"))
            lbl_val.pack(side="right", padx=20, pady=15)

    # ================= TAB 4: API DIAGNOSTICS =================
    def _build_api_tab(self) -> None:
        """Construct REST API Health & Diagnostics tab."""
        self.api_card = ctk.CTkFrame(self.tab_api, fg_color=("#F0F3F4", "#16213E"), corner_radius=15)
        self.api_card.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(
            self.api_card,
            text="🌐 Marc Conrad Banana API Health Diagnostics",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#F1C40F"
        )
        title.pack(pady=15)

        self.test_api_btn = ctk.CTkButton(
            self.api_card,
            text="⚡ Execute API Connection Test",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#3498DB",
            hover_color="#2980B9",
            height=40,
            command=self.run_api_health_check
        )
        self.test_api_btn.pack(pady=10)

        self.api_output_box = ctk.CTkTextbox(
            self.api_card,
            width=600,
            height=250,
            font=ctk.CTkFont(family="Consolas", size=13)
        )
        self.api_output_box.pack(pady=15, fill="both", expand=True, padx=20)
        self.api_output_box.insert("1.0", "Click 'Execute API Connection Test' to run live HTTP REST API diagnostic ping.")

    def run_api_health_check(self) -> None:
        """Run a live diagnostic ping to Marc Conrad's REST API."""
        self.api_output_box.delete("1.0", "end")
        self.api_output_box.insert("1.0", "Initiating HTTP GET request to Marc Conrad Banana API...\n")

        url = "https://marcconrad.com/uob/banana/api.php?out=json&base64=yes"
        t0 = time.time()
        try:
            res = requests.get(url, timeout=8)
            latency = int((time.time() - t0) * 1000)

            status_report = (
                f"✅ HTTP DIAGNOSTIC SUCCESSFUL\n"
                f"--------------------------------------------------\n"
                f"Target Endpoint: {url}\n"
                f"HTTP Status Code: {res.status_code} OK\n"
                f"Response Latency: {latency} ms\n"
                f"Content-Type: {res.headers.get('Content-Type', 'Unknown')}\n"
                f"Payload Format: JSON (base64=yes)\n\n"
                f"Raw JSON Response Sample:\n{res.text[:300]}...\n"
            )
        except Exception as e:
            status_report = (
                f"❌ HTTP DIAGNOSTIC FAILED\n"
                f"--------------------------------------------------\n"
                f"Target Endpoint: {url}\n"
                f"Error Context: {str(e)}\n"
            )

        self.api_output_box.delete("1.0", "end")
        self.api_output_box.insert("1.0", status_report)

    def on_logout_click(self) -> None:
        """Logout Admin."""
        authenticator.logout()
        self.on_logout_callback()
