"""
A simple testbench GUI for comparing Wordle solver heuristics.

This module provides a Tkinter-based interface that allows the user to run
simulations of the available solving strategies over a specified number of
random Wordle games. It reports metrics such as the average number of guesses,
the total elapsed runtime, and the success rate for each selected strategy.

To launch the GUI, run this module directly with Python::

    python ui/performance_gui.py

The GUI is designed for demonstration and educational purposes. It loads
the expanded word list if available, falling back to the default dictionary
otherwise. The simulations run locally and may take several seconds when the
number of games is large.
"""

from __future__ import annotations

import random
import time
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import sys

# Ensure project modules are importable when running as a script
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from data.loader import clean_words, load_words_default
from solver.solver import solve_word, solve_word_frequency


def load_word_list() -> list[str]:
    """Load the expanded word list if present, otherwise fall back to default."""
    expanded = ROOT / "data" / "expanded_words.txt"
    if expanded.exists():
        with expanded.open("r", encoding="utf-8") as f:
            return [w.strip() for w in f if w.strip()]
    # Fallback
    return load_words_default()


class PerformanceTestbenchGUI(tk.Tk):
    """
    A GUI for running performance comparisons between solver heuristics.

    Users can select which strategies to benchmark, specify the number of
    games to simulate, and see a summary of performance metrics.
    """

    def __init__(self) -> None:
        super().__init__()
        self.title("Wordle Solver Performance Testbench")
        self.geometry("550x450")
        self.resizable(False, False)

        # Load words once
        self.words: list[str] = load_word_list()

        # UI elements
        self._create_widgets()

    def _create_widgets(self) -> None:
        # Heading
        heading = tk.Label(self, text="Performance Comparison", font=("Arial", 16, "bold"))
        heading.pack(pady=(10, 5))

        # Number of games entry
        entry_frame = tk.Frame(self)
        entry_frame.pack(pady=(5, 10))
        tk.Label(entry_frame, text="Number of games:").pack(side=tk.LEFT)
        self.games_var = tk.StringVar(value="50")
        games_entry = tk.Entry(entry_frame, textvariable=self.games_var, width=6)
        games_entry.pack(side=tk.LEFT, padx=(5, 0))

        # Solver selection
        self.strategy_vars: dict[str, tk.BooleanVar] = {
            "entropy": tk.BooleanVar(value=True),
            "frequency": tk.BooleanVar(value=True),
        }
        strategies_frame = tk.Frame(self)
        strategies_frame.pack(pady=(0, 10))
        tk.Label(strategies_frame, text="Select strategies:").pack(anchor="w")
        tk.Checkbutton(
            strategies_frame,
            text="Entropy heuristic",
            variable=self.strategy_vars["entropy"],
        ).pack(anchor="w")
        tk.Checkbutton(
            strategies_frame,
            text="Frequency heuristic",
            variable=self.strategy_vars["frequency"],
        ).pack(anchor="w")

        # Run button
        run_btn = tk.Button(self, text="Run Testbench", command=self.run_testbench)
        run_btn.pack(pady=(0, 10))

        # Results display
        self.results_text = tk.Text(
            self,
            width=65,
            height=14,
            state=tk.DISABLED,
            font=("Courier", 11),
            wrap="none",
        )
        self.results_text.pack(padx=10, pady=(0, 10))

    def run_testbench(self) -> None:
        """Run simulations for selected strategies and display the results."""
        # Validate number of games
        try:
            n_games = int(self.games_var.get())
            if n_games <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a positive integer for the number of games.")
            return

        selected_strategies = [name for name, var in self.strategy_vars.items() if var.get()]
        if not selected_strategies:
            messagebox.showwarning("No strategies selected", "Please select at least one strategy to test.")
            return

        # Run simulations
        results: list[tuple[str, float, float, float]] = []  # (name, avg_guesses, success_rate, total_time)
        for strategy in selected_strategies:
            successes = 0
            total_guesses = 0
            start_time = time.perf_counter()
            for _ in range(n_games):
                secret = random.choice(self.words)
                try:
                    if strategy == "entropy":
                        guesses = solve_word(secret, self.words)
                    elif strategy == "frequency":
                        guesses = solve_word_frequency(secret, self.words)
                    else:
                        continue
                    total_guesses += len(guesses)
                    successes += 1 if guesses[-1][0] == secret else 0
                except Exception:
                    # In case of unexpected failure
                    pass
            elapsed = time.perf_counter() - start_time
            avg_guesses = (total_guesses / successes) if successes else 0.0
            success_rate = (successes / n_games) * 100.0
            results.append((strategy, avg_guesses, success_rate, elapsed))

        # Display results
        self.results_text.configure(state=tk.NORMAL)
        self.results_text.delete("1.0", tk.END)
        header = f"{'Strategy':<15}{'Avg guesses':>12}{'Success %':>12}{'Time (s)':>12}\n"
        self.results_text.insert(tk.END, header)
        self.results_text.insert(tk.END, "-" * (len(header) - 1) + "\n")
        for name, avg, success, total_time in results:
            self.results_text.insert(
                tk.END,
                f"{name:<15}{avg:>12.2f}{success:>12.1f}{total_time:>12.2f}\n",
            )
        self.results_text.configure(state=tk.DISABLED)


def main() -> None:
    app = PerformanceTestbenchGUI()
    app.mainloop()


if __name__ == "__main__":
    main()