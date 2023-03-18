"""main.py Initial driver for the sudoku Puzzle
"""
import os

from sudoku import sudoku

def clear():
    """ Clears the console
    """
    os.system('clear')
def main():
    """ main function
    """
    board = sudoku.Puzzle(9)
    board.fill(1,1,2, True)
    board.fill(1,3,3, True)
    board.fill(1,4,6, True)
    board.fill(1,5,5, True)
    board.fill(1,7,7, True)

    board.fill(2,3,8, True)
    board.fill(2,5,2, True)
    board.fill(2,6,7, True)
    board.fill(2,8,3, True)

    board.fill(3,2,5, True)
    board.fill(3,3,7, True)
    board.fill(3,9,4, True)

    board.fill(4,1,8, True)
    board.fill(4,9,2, True)

    board.fill(5,1,3, True)
    board.fill(5,2,9, True)
    board.fill(5,4,8, True)
    board.fill(5,7,4, True)

    board.fill(6,1,4, True)
    board.fill(6,3,6, True)
    board.fill(6,5,1, True)

    board.fill(7,5,9, True)
    board.fill(7,8,1, True)

    board.fill(8,7,8, True)
    board.fill(8,9,5, True)

    board.fill(9,2,3, True)
    board.fill(9,3,2, True)
    board.fill(9,4,7, True)
    board.fill(9,5,8, True)
    board.fill(9,7,6, True)

    board.validate()
    board.add_hint(1,2,1)
    board.add_hint(1,2,2)
    board.add_hint(1,2,3)
    board.add_hint(1,2,4)
#print(board.get_hints(1,2))
#board.remove_hint(1,2,1)
#print(board.get_hints(1,2))
    valid = True
    while board.solved():
        if valid:
            print("Last Entry Was not a valid Entry")
        else:
            print("")

        board.pretty_print()
        row = input("Input Row: ")
        column = input("Input Column: ")
        value = input("Input Value: ")
        board.fill(int(row), int(column), int(value))
        valid = board.validate()
        if valid:
            board.fill(int(row), int(column), board.INVALID)
        clear()
main()
