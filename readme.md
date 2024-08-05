# Description

The Sudoku Solver application is a tool designed to solve Sudoku puzzles using machine learning to recognize digits in images. It allows users to either manually input puzzles or automatically recognize and solve Sudoku based on images selected by the user.

The application is built using the Kivy framework, employs a machine learning model implemented with scikit-learn, and uses OpenCV for image processing to detect digits.

For solving Sudoku puzzles, the Sudoku Solver application utilizes a backtracking algorithm. This algorithm systematically tries different possibilities and backtracks when it determines that the current path does not lead to a solution. In the context of Sudoku, the algorithm attempts to place digits from 1 to 9 in empty cells while ensuring that the placement adheres to the rules of the game (no digit can be repeated in any row, column, or 3x3 grid).


# Installation

Clone the repository:

    git clone ...
    cd kivy-sudoku-solver

Install dependencies:

    pip install -r requirements.txt

How to Use

Launch the Application:
Run the application using 

    python3 main.py
    

