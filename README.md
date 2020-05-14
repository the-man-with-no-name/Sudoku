# Sudoku
This repository provides an implementation of Sudoku using ```pygame``` and ```numpy```.
The inner workings of the game are located in ```sudoku.py```.
The folder ```font``` contains the font used by the game and ```data``` includes a text file containing a Leaderboard of the top 5 scores.
The last file is ```run.py``` which runs the game.

To run the game, ```cd``` to the proper directory and type

```python run.py```

This implementation of sudoku has some key features:
1. Main Menu where user selects difficulty and leaderboard is displayed.
1. When user selects difficulty, we use the symmetric group to create a new board isomorphic to a few hardcoded boards (this allows us to have ```16,930,529,280``` different boards up to isomorphism for each hardcoded board).
1. Hints are given as to whether a move is valid or not given the current board.
1. The game is scored to encourage the user to only make moves they are certain are correct. 
1. A sudoku solver using backtracking is also provided in the ```sudoku.py``` file.
