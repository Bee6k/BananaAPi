"""
===============================================================================
BANANA GAME - ADVANCED CS EDUCATIONAL APPLICATION
Package: engine
File: game_engine.py
Description: Game state controller, asynchronous networking thread dispatcher,
             pre-fetching queue manager, scoring rules, and solution verification engine.

CS THEME COVERAGE:
- Theme 2: Event-Driven Programming & Asynchronous Multithreading
- Theme 3: Interoperability (REST API Engine Integration & Pre-fetching Buffer)

VIDEO PRESENTATION TALKING POINTS:
1. "To maintain responsive Event-Driven GUI architecture (Theme 2), networking calls
   must never run on the main Tkinter UI looper thread."
2. "GameEngine encapsulates asynchronous multithreading using Python's 'threading.Thread'
   module and implements a pre-fetching queue."
3. "The pre-fetching queue fetches upcoming puzzles in the background so that when
   a player solves an equation, the next equation displays INSTANTLY without waiting!"
4. "It tracks player streaks, scores, solution verification (0-9 integer logic), and hint generation."
===============================================================================
"""

import threading
import time
from typing import Callable, Optional, Tuple, List
from PIL import Image
from engine.banana_api import BananaAPIClient
from auth.authenticator import authenticator
from models.session_log import audit_logger


class GameEngine:
    """
    Core Game Engine managing puzzle state, score calculations, async API fetching,
    pre-fetched queue buffering, and solution verification logic.
    """

    def __init__(self) -> None:
        """Initialize the Game Engine state and pre-fetch queue."""
        self.api_client: BananaAPIClient = BananaAPIClient(use_base64=True, output_format="json")
        self.current_puzzle_image: Optional[Image.Image] = None
        self.current_solution: Optional[int] = None
        self.current_source_info: str = ""

        # Pre-fetching Queue for instant zero-latency puzzle transitions
        self._puzzle_queue: List[Tuple[Image.Image, int, str]] = []
        self._queue_lock = threading.Lock()
        
        # Scoring & Session Metrics
        self.current_score: int = 0
        self.streak: int = 0
        self.total_attempts: int = 0
        self.correct_answers: int = 0
        self.start_time: float = time.time()
        self.is_loading: bool = False
        self.hints_used: int = 0

        # Start preloading puzzles in background immediately
        self.preload_puzzle_in_background()

    def reset_session(self) -> None:
        """Reset current game session score and streak."""
        self.current_score = 0
        self.streak = 0
        self.total_attempts = 0
        self.correct_answers = 0
        self.hints_used = 0
        self.start_time = time.time()

    def get_elapsed_seconds(self) -> int:
        """Calculate total elapsed time in seconds for the session."""
        return int(time.time() - self.start_time)

    def preload_puzzle_in_background(self) -> None:
        """
        Background worker thread to pre-fetch upcoming puzzles into memory queue.
        Ensures player experiences instant puzzle loading upon answering.
        """
        with self._queue_lock:
            if len(self._puzzle_queue) >= 2 or self.is_loading:
                return

        def preload_worker():
            try:
                image, solution, source_info = self.api_client.fetch_puzzle()
                with self._queue_lock:
                    self._puzzle_queue.append((image, solution, source_info))
                
                # Check if we should pre-fetch one more
                with self._queue_lock:
                    if len(self._puzzle_queue) < 2:
                        threading.Thread(target=preload_worker, daemon=True).start()
            except Exception as e:
                print(f"[GameEngine Preload Warning] Preload background fetch exception: {e}")

        thread = threading.Thread(target=preload_worker, daemon=True)
        thread.start()

    def fetch_next_puzzle_async(
        self,
        on_success: Callable[[Image.Image, str], None],
        on_error: Callable[[str], None]
    ) -> None:
        """
        Fetch the next puzzle asynchronously. If a pre-fetched puzzle exists in the queue,
        it returns INSTANTLY (0ms latency). Otherwise, dispatches worker thread.

        Args:
            on_success (Callable[[Image.Image, str], None]): Callback on success (image, source_info).
            on_error (Callable[[str], None]): Callback on failure error message.
        """
        # 1. Check if pre-fetched puzzle is readily available in queue
        cached_puzzle = None
        with self._queue_lock:
            if len(self._puzzle_queue) > 0:
                cached_puzzle = self._puzzle_queue.pop(0)

        if cached_puzzle:
            image, solution, source_info = cached_puzzle
            self.current_puzzle_image = image
            self.current_solution = solution
            self.current_source_info = source_info

            # Log event
            user = authenticator.current_user
            if user:
                audit_logger.log_event(
                    username=user.username,
                    role=user.role,
                    action="PUZZLE_LOADED",
                    details=f"Loaded puzzle from pre-fetch queue. Source: {source_info}"
                )

            # Replenish pre-fetch buffer in background
            self.preload_puzzle_in_background()

            # Execute callback immediately
            on_success(image, source_info)
            return

        # 2. If queue is empty, fetch asynchronously via worker thread
        if self.is_loading:
            return  # Prevent concurrent fetch loops

        self.is_loading = True

        def worker():
            try:
                image, solution, source_info = self.api_client.fetch_puzzle()
                self.current_puzzle_image = image
                self.current_solution = solution
                self.current_source_info = source_info

                # Log event
                user = authenticator.current_user
                if user:
                    audit_logger.log_event(
                        username=user.username,
                        role=user.role,
                        action="PUZZLE_LOADED",
                        details=f"Fetched new puzzle. Source: {source_info}"
                    )

                # Replenish buffer
                self.preload_puzzle_in_background()

                on_success(image, source_info)

            except Exception as e:
                error_msg = f"Failed to fetch puzzle: {str(e)}"
                on_error(error_msg)
            finally:
                self.is_loading = False

        # Dispatch background thread
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()

    def verify_solution(self, player_answer: int) -> Tuple[bool, int, str]:
        """
        Verify player's integer answer (0-9) against the current solution.

        Args:
            player_answer (int): Answer digit submitted by player.

        Returns:
            Tuple[bool, int, str]:
                - Boolean indicating whether answer is correct.
                - Correct integer solution.
                - Informative message.
        """
        if self.current_solution is None:
            return False, -1, "No active puzzle loaded."

        self.total_attempts += 1
        is_correct = (player_answer == self.current_solution)

        user = authenticator.current_user
        username = user.username if user else "GUEST"
        role = user.role if user else "PLAYER"

        if is_correct:
            self.correct_answers += 1
            self.streak += 1
            # Base score 10 points + streak bonus
            points_gained = 10 + (self.streak * 2)
            self.current_score += points_gained

            # Update User High Score if logged in
            if user:
                authenticator.update_user_high_score(user.username, self.current_score)
                user.record_game_result(is_win=True, score=self.current_score)

            audit_logger.log_event(
                username=username,
                role=role,
                action="PUZZLE_CORRECT",
                details=f"Submitted {player_answer}. Correct! Score: {self.current_score}, Streak: {self.streak}"
            )
            msg = f"🎉 Correct! +{points_gained} pts (Streak x{self.streak})"
        else:
            self.streak = 0
            if user:
                user.record_game_result(is_win=False, score=self.current_score)

            audit_logger.log_event(
                username=username,
                role=role,
                action="PUZZLE_INCORRECT",
                details=f"Submitted {player_answer}. Expected {self.current_solution}."
            )
            msg = f"❌ Incorrect! The correct solution was {self.current_solution}."

        return is_correct, self.current_solution, msg

    def get_hint(self) -> str:
        """
        Generate a pedagogical hint for the player regarding the current solution.

        Returns:
            str: Hint description.
        """
        if self.current_solution is None:
            return "Load a puzzle first to get a hint!"

        self.hints_used += 1
        sol = self.current_solution
        parity = "EVEN" if sol % 2 == 0 else "ODD"
        
        if sol <= 3:
            range_hint = "0, 1, 2, or 3"
        elif sol <= 6:
            range_hint = "4, 5, or 6"
        else:
            range_hint = "7, 8, or 9"

        user = authenticator.current_user
        if user:
            audit_logger.log_event(
                username=user.username,
                role=user.role,
                action="HINT_REQUESTED",
                details=f"Hint requested for solution {sol}"
            )

        return f"💡 HINT: The number is {parity} and falls in the range ({range_hint})."
