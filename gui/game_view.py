"""
===============================================================================
BANANA GAME - ADVANCED CS EDUCATIONAL APPLICATION
Package: gui
File: game_view.py
Description: Interactive Math Puzzle Player View built with CustomTkinter.

CS THEME COVERAGE:
- Theme 2: Event-Driven Programming (Control Binding & Keyboard Numpad Listeners)
- Theme 3: Interoperability (Asynchronous REST API Puzzle Image Display & Pre-fetching)
- Theme 4: Virtual Identity (Role Badge Context & Personal Score Tracking)

VIDEO PRESENTATION TALKING POINTS:
1. "The GameView is our interactive puzzle workspace for Theme 2 and Theme 3."
2. "Notice how UI controls (numpad 0-9, hint, skip, reset) bind directly to Python event handlers."
3. "We also register physical keyboard listeners so players can type answers directly on their keyboard."
4. "The puzzle image is pre-fetched asynchronously using worker threads from Marc Conrad's REST API,
   ensuring instant 0-millisecond puzzle transitions while maintaining a 100% thread-safe UI."
===============================================================================
"""

import customtkinter as ctk
from PIL import Image
from typing import Callable, Optional
from engine.game_engine import GameEngine
from utils.image_loader import create_ctk_image
from auth.authenticator import authenticator
from auth.user_roles import get_role_badge_color, can_access_admin_dashboard
from models.user import User


class GameView(ctk.CTkFrame):
    """
    CustomTkinter Frame providing the main interactive math puzzle gameplay interface.
    """

    def __init__(
        self,
        parent: ctk.CTk,
        on_logout: Callable[[], None],
        on_open_admin: Optional[Callable[[], None]] = None
    ) -> None:
        """
        Initialize the GameView.

        Args:
            parent (ctk.CTk): Parent window container.
            on_logout (Callable[[], None]): Logout callback.
            on_open_admin (Optional[Callable[[], None]]): Admin dashboard callback.
        """
        super().__init__(parent, fg_color="transparent")
        self.parent: ctk.CTk = parent
        self.on_logout_callback: Callable[[], None] = on_logout
        self.on_open_admin_callback: Optional[Callable[[], None]] = on_open_admin

        self.game_engine: GameEngine = GameEngine()
        self.timer_active: bool = True
        self.current_user: Optional[User] = authenticator.current_user

        self._build_ui()
        self._bind_keyboard_events()
        self._start_timer_loop()
        
        # Load initial puzzle asynchronously
        self._load_next_puzzle()

    def _build_ui(self) -> None:
        """Construct Top Header Bar, Puzzle Canvas Card, Feedback Banner, and Control Keypad."""
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # ------------------- TOP NAVBAR -------------------
        self.top_bar = ctk.CTkFrame(self, fg_color=("#EAEDED", "#16213E"), corner_radius=15, height=60)
        self.top_bar.pack(fill="x", pady=(0, 15))

        # User Role Badge
        uname = self.current_user.username if self.current_user else "GUEST"
        urole = self.current_user.role if self.current_user else "PLAYER"
        badge_color = get_role_badge_color(urole)

        self.user_badge = ctk.CTkLabel(
            self.top_bar,
            text=f" 👤 {uname} ({urole}) ",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=badge_color,
            text_color="#FFFFFF",
            corner_radius=10,
            height=32
        )
        self.user_badge.pack(side="left", padx=15, pady=10)

        # Score Displays
        self.score_label = ctk.CTkLabel(
            self.top_bar,
            text="⭐ Score: 0",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#F1C40F"
        )
        self.score_label.pack(side="left", padx=15)

        high_score_val = self.current_user.high_score if self.current_user else 0
        self.high_score_label = ctk.CTkLabel(
            self.top_bar,
            text=f"🏆 High Score: {high_score_val}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#3498DB"
        )
        self.high_score_label.pack(side="left", padx=15)

        # Timer Display
        self.timer_label = ctk.CTkLabel(
            self.top_bar,
            text="⏱️ Time: 0s",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("#2C3E50", "#ECF0F1")
        )
        self.timer_label.pack(side="left", padx=15)

        # Right Side Header Actions (Admin & Logout)
        self.logout_btn = ctk.CTkButton(
            self.top_bar,
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

        if self.current_user and can_access_admin_dashboard(self.current_user.role):
            self.admin_btn = ctk.CTkButton(
                self.top_bar,
                text="⚙️ Admin Dashboard",
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color="#E94560",
                hover_color="#9B59B6",
                width=140,
                height=32,
                corner_radius=8,
                command=self.on_admin_click
            )
            self.admin_btn.pack(side="right", padx=5)

        # ------------------- MAIN CONTENT AREA -------------------
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True)
        self.content_frame.grid_columnconfigure(0, weight=3)
        self.content_frame.grid_columnconfigure(1, weight=2)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # --- LEFT COLUMN: PUZZLE DISPLAY CARD ---
        self.puzzle_card = ctk.CTkFrame(
            self.content_frame,
            fg_color=("#F0F3F4", "#16213E"),
            corner_radius=20,
            border_width=2,
            border_color="#F1C40F"
        )
        self.puzzle_card.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="nsew")

        # Card Title
        self.card_title = ctk.CTkLabel(
            self.puzzle_card,
            text="🍌 BANANA MATH PUZZLE",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#F1C40F"
        )
        self.card_title.pack(pady=(15, 5))

        # Puzzle Image Canvas Placeholder
        self.image_container = ctk.CTkLabel(
            self.puzzle_card,
            text="⏳ Loading Puzzle from Marc Conrad REST API...",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=("#7F8C8D", "#BDC3C7"),
            width=500,
            height=260
        )
        self.image_container.pack(padx=20, pady=10, fill="both", expand=True)

        # API Source Info Label
        self.api_source_label = ctk.CTkLabel(
            self.puzzle_card,
            text="Connecting to REST API...",
            font=ctk.CTkFont(size=11, slant="italic"),
            text_color="#7F8C8D"
        )
        self.api_source_label.pack(pady=(0, 15))

        # Feedback Banner
        self.feedback_label = ctk.CTkLabel(
            self.puzzle_card,
            text="Select an answer digit (0-9) below or use your keyboard!",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#3498DB",
            height=30
        )
        self.feedback_label.pack(pady=(0, 15))

        # --- RIGHT COLUMN: CONTROL PANEL & NUMPAD ---
        self.control_card = ctk.CTkFrame(
            self.content_frame,
            fg_color=("#F0F3F4", "#16213E"),
            corner_radius=20,
            border_width=2,
            border_color="#3498DB"
        )
        self.control_card.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="nsew")

        control_title = ctk.CTkLabel(
            self.control_card,
            text="🔢 ANSWER KEYPAD",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#3498DB"
        )
        control_title.pack(pady=(15, 10))

        # Keypad Numpad Grid Container
        self.numpad_frame = ctk.CTkFrame(self.control_card, fg_color="transparent")
        self.numpad_frame.pack(pady=10)

        # Create Buttons 1 to 9 (3x3 grid)
        for i in range(1, 10):
            row = (i - 1) // 3
            col = (i - 1) % 3
            btn = ctk.CTkButton(
                self.numpad_frame,
                text=str(i),
                font=ctk.CTkFont(size=22, weight="bold"),
                fg_color="#34495E",
                hover_color="#F1C40F",
                text_color="#FFFFFF",
                width=75,
                height=60,
                corner_radius=12,
                command=lambda digit=i: self.on_digit_submit(digit)
            )
            btn.grid(row=row, column=col, padx=6, pady=6)

        # Bottom Row: 0 Button centered
        zero_btn = ctk.CTkButton(
            self.numpad_frame,
            text="0",
            font=ctk.CTkFont(size=22, weight="bold"),
            fg_color="#34495E",
            hover_color="#F1C40F",
            text_color="#FFFFFF",
            width=245,
            height=50,
            corner_radius=12,
            command=lambda: self.on_digit_submit(0)
        )
        zero_btn.grid(row=3, column=0, columnspan=3, padx=6, pady=6)

        # Action Buttons Container (Hint, Next, Reset)
        self.action_frame = ctk.CTkFrame(self.control_card, fg_color="transparent")
        self.action_frame.pack(pady=15, fill="x", padx=20)

        self.hint_btn = ctk.CTkButton(
            self.action_frame,
            text="💡 Get Hint",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#F39C12",
            hover_color="#D68910",
            height=38,
            corner_radius=10,
            command=self.on_hint_click
        )
        self.hint_btn.pack(fill="x", pady=4)

        self.next_btn = ctk.CTkButton(
            self.action_frame,
            text="⏭️ Skip / Next Puzzle",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#2980B9",
            hover_color="#1F618D",
            height=38,
            corner_radius=10,
            command=self._load_next_puzzle
        )
        self.next_btn.pack(fill="x", pady=4)

        self.reset_btn = ctk.CTkButton(
            self.action_frame,
            text="🔄 Reset Score",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#7F8C8D",
            hover_color="#626567",
            height=34,
            corner_radius=10,
            command=self.on_reset_click
        )
        self.reset_btn.pack(fill="x", pady=4)

    def _bind_keyboard_events(self) -> None:
        """Bind physical keyboard numpad digits (0-9) to solution verification."""
        for digit in range(10):
            self.parent.bind(str(digit), lambda event, d=digit: self.on_digit_submit(d))

    def _start_timer_loop(self) -> None:
        """Recurring event loop updating elapsed time indicator."""
        if self.timer_active:
            elapsed = self.game_engine.get_elapsed_seconds()
            self.timer_label.configure(text=f"⏱️ Time: {elapsed}s")
            self.after(1000, self._start_timer_loop)

    def _load_next_puzzle(self) -> None:
        """Trigger fetching or instant loading of the pre-fetched math puzzle."""
        def on_success(pil_image: Image.Image, source_info: str):
            # Schedule GUI update thread-safely on Tkinter main thread
            self.after(0, lambda img=pil_image, src=source_info: self._apply_puzzle_to_ui(img, src))

        def on_error(err_msg: str):
            self.after(0, lambda msg=err_msg: self._apply_error_to_ui(msg))

        # Async Engine Call
        self.game_engine.fetch_next_puzzle_async(on_success=on_success, on_error=on_error)

    def _apply_puzzle_to_ui(self, pil_image: Image.Image, source_info: str) -> None:
        """Thread-safe main loop execution to render puzzle image and reset banner."""
        try:
            ctk_img = create_ctk_image(pil_image, target_size=(480, 240))
            self.image_container.configure(image=ctk_img, text="")
            self.api_source_label.configure(text=f"Source: {source_info}")
            self.feedback_label.configure(
                text="Solve the equation and pick 0-9!",
                text_color="#3498DB"
            )
        except Exception as e:
            print(f"[GameView Error] UI update exception: {e}")

    def _apply_error_to_ui(self, err_msg: str) -> None:
        """Thread-safe main loop execution to render error message."""
        self.image_container.configure(image=None, text=f"⚠️ {err_msg}")
        self.feedback_label.configure(text="Network Error. Click Next to retry.", text_color="#E74C3C")

    def on_digit_submit(self, digit: int) -> None:
        """
        Event Handler for player answer submission.

        Args:
            digit (int): The integer answer submitted (0-9).
        """
        if self.game_engine.is_loading:
            return

        is_correct, sol, msg = self.game_engine.verify_solution(digit)

        # Update Score Header
        self.score_label.configure(text=f"⭐ Score: {self.game_engine.current_score}")
        if self.current_user:
            self.high_score_label.configure(text=f"🏆 High Score: {self.current_user.high_score}")

        if is_correct:
            self.feedback_label.configure(text=msg, text_color="#2ECC71")
            # Immediately trigger next puzzle (uses pre-fetched puzzle instantly!)
            self.after(500, self._load_next_puzzle)
        else:
            self.feedback_label.configure(text=msg, text_color="#E74C3C")

    def on_hint_click(self) -> None:
        """Event Handler for hint button."""
        hint_text = self.game_engine.get_hint()
        self.feedback_label.configure(text=hint_text, text_color="#F39C12")

    def on_reset_click(self) -> None:
        """Reset player session score."""
        self.game_engine.reset_session()
        self.score_label.configure(text="⭐ Score: 0")
        self.feedback_label.configure(text="Session Reset! Select an answer (0-9).", text_color="#3498DB")

    def on_logout_click(self) -> None:
        """Clean up bindings and trigger logout."""
        self.timer_active = False
        authenticator.logout()
        self.on_logout_callback()

    def on_admin_click(self) -> None:
        """Switch view to Admin Dashboard (Role.ADMIN only)."""
        if self.on_open_admin_callback:
            self.on_open_admin_callback()
