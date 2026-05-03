"""
UI for demonstrating the Wordle solver.

This simple Tkinter-based GUI lets a user choose a secret word, select a
solving strategy (entropy or frequency), and then view the solver's guesses
and feedback. It is designed for demonstration purposes only; there is no
validation of the input beyond basic length and alphabetic checks.
"""

import tkinter as tk
from tkinter import ttk, messagebox

import sys
import os
from pathlib import Path

# Add project root to sys.path so we can import project modules when running
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from data.loader import clean_words
from solver.solver import solve_word, solve_word_frequency


def load_expanded_words() -> list[str]:
    """Load the expanded word list used for solving."""
    data_path = ROOT / "data" / "expanded_words.txt"
    if not data_path.exists():
        # fall back to default lists if expanded list is missing
        from data.loader import load_words_default
        return load_words_default()
    with data_path.open("r", encoding="utf-8") as f:
        words = [w.strip() for w in f.readlines() if w.strip()]
    return words


class WordleSolverGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wordle Solver Demo")
        self.geometry("480x400")
        self.resizable(False, False)
        # Load word list once
        self.words = load_expanded_words()

        # UI elements
        self.create_widgets()

    def create_widgets(self):
        # Instruction label
        instr = tk.Label(self, text="Enter a 5‑letter secret word:")
        instr.pack(pady=(10, 5))

        # Entry field for secret word
        self.word_entry = tk.Entry(self, width=10, font=("Arial", 14))
        self.word_entry.pack(pady=(0, 10))

        # Solver choice
        solver_frame = tk.Frame(self)
        solver_frame.pack(pady=(0, 10))
        self.solver_var = tk.StringVar(value="entropy")
        tk.Radiobutton(solver_frame, text="Entropy heuristic", variable=self.solver_var,
                       value="entropy").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(solver_frame, text="Frequency heuristic", variable=self.solver_var,
                       value="frequency").pack(side=tk.LEFT, padx=5)

        # Solve button
        solve_btn = tk.Button(self, text="Solve", command=self.solve)
        solve_btn.pack(pady=(0, 10))

        # Frame for results
        self.results_text = tk.Text(self, width=40, height=12, state=tk.DISABLED, font=("Courier", 12))
        self.results_text.pack(padx=10, pady=(0, 10))

    def solve(self):
        secret = self.word_entry.get().strip().lower()
        # Basic validation
        if len(secret) != 5 or not secret.isalpha():
            messagebox.showerror("Invalid input", "Please enter exactly 5 letters (A‑Z)")
            return
        if secret not in self.words:
            messagebox.showwarning("Word not found", "The secret word is not in the word list.\n"
                                  "The solver will still attempt to solve it, but may fail.")
        # Solve
        if self.solver_var.get() == "frequency":
            guesses = solve_word_frequency(secret, self.words)
        else:
            guesses = solve_word(secret, self.words)
        # Display results
        self.results_text.configure(state=tk.NORMAL)
        self.results_text.delete("1.0", tk.END)
        for i, (guess, feedback) in enumerate(guesses, 1):
            colored = ''.join(self._format_letter(g, fb) for g, fb in zip(guess, feedback))
            self.results_text.insert(tk.END, f"{i}. {colored}\n")
        self.results_text.insert(tk.END, f"\nSolved in {len(guesses)} guesses.\n")
        self.results_text.configure(state=tk.DISABLED)

    @staticmethod
    def _format_letter(letter: str, fb: str) -> str:
        """Return a string with Tk tags to style the letter according to feedback."""
        # Colors similar to Wordle: green for correct, yellow for present, gray for absent
        color_map = {"G": "#6AAA64", "Y": "#C9B458", "B": "#787C7E"}
        return letter.upper()


def main():
    app = WordleSolverGUI()
    app.mainloop()


if __name__ == "__main__":
    main()