This is a bonus project for ECE4524: Artificial Intelligence and Engineering Applications, Spring 2026 with Dr. Abhijit Sarkar.

The goal of this project is to create an AI program that solves Wordle games efficiently.

The solver keeps a list of all possible secret words and picks guesses one by one. 
Each guess is chosen to give the most information about the secret word using entropy. 
After each guess, the AI checks which letters are correct, in the wrong spot, or not in the word. 
It then removes any words from the list that don’t match the feedback. The AI repeats this until it finds the secret word. 
By doing this, it can solve Wordle quickly without learning or training.

To run the program, enter py main.py or python main.py in the terminal