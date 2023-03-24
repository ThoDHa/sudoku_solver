"""main.py Initial driver for the sudoku Puzzle
"""
import os
from sudoku import sudoku

def clear():
    """ Clears the console
    """
    os.system('clear')

def create_puzzle():
    """ Create the board and return back the object
    """
    puzzle = sudoku.Puzzle(9)
    puzzle.fill(1,1,2, True)
    puzzle.fill(1,3,3, True)
    puzzle.fill(1,4,6, True)
    puzzle.fill(1,5,5, True)
    puzzle.fill(1,7,7, True)

    puzzle.fill(2,3,8, True)
    puzzle.fill(2,5,2, True)
    puzzle.fill(2,6,7, True)
    puzzle.fill(2,8,3, True)

    puzzle.fill(3,2,5, True)
    puzzle.fill(3,3,7, True)
    puzzle.fill(3,9,4, True)

    puzzle.fill(4,1,8, True)
    puzzle.fill(4,9,2, True)

    puzzle.fill(5,1,3, True)
    puzzle.fill(5,2,9, True)
    puzzle.fill(5,4,8, True)
    puzzle.fill(5,7,4, True)

    puzzle.fill(6,1,4, True)
    puzzle.fill(6,3,6, True)
    puzzle.fill(6,5,1, True)

    puzzle.fill(7,5,9, True)
    puzzle.fill(7,8,1, True)

    puzzle.fill(8,7,8, True)
    puzzle.fill(8,9,5, True)

    puzzle.fill(9,2,3, True)
    puzzle.fill(9,3,2, True)
    puzzle.fill(9,4,7, True)
    puzzle.fill(9,5,8, True)
    puzzle.fill(9,7,6, True)
    return puzzle

def brute_force():
    """ Create and brute force the puzzle
    """
    puzzle = create_puzzle()
    puzzle.pretty_print()
    puzzle.brute_force_solve()
    puzzle.pretty_print()
def console_game():
    """ Basic console implmentation of the game
    """
    puzzle = create_puzzle()
    while puzzle.solved():

        puzzle.pretty_print()
        row = input("Input Row: ")
        column = input("Input Column: ")
        value = input("Input Value: ")
        puzzle.fill(int(row), int(column), int(value))
        valid = puzzle.validate()
        clear()
        if not valid:
            print("Last Entry Was not a valid Entry")
            puzzle.fill(int(row), int(column), puzzle.INVALID)
        else:
            print("")
    input("Congrats you beat the game!")
    puzzle.pretty_print()

def generate_game():
    """ main function
    """
    puzzle = sudoku.Puzzle(9)
    puzzle.generate_board()

def main():
    """ main function
    """
    generate_game()
    #brute_force()
main()
