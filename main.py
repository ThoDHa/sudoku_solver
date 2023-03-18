
import json
import os
import math

from sudoku import Sudoku


clear = lambda: os.system('clear')


def main():
    board = Sudoku.Puzzle(9)
    board.fill(1,1,"2", "True")
    board.fill(1,3,"3", "True")
    board.fill(1,4,"6", "True")
    board.fill(1,5,"5", "True")
    board.fill(1,7,"7", "True")

    board.fill(2,3,"8", "True")
    board.fill(2,5,"2", "True")
    board.fill(2,6,"7", "True")
    board.fill(2,8,"3", "True")

    board.fill(3,2,"5", "True")
    board.fill(3,3,"7", "True")
    board.fill(3,9,"4", "True")

    board.fill(4,1,"8", "True")
    board.fill(4,9,"2", "True")

    board.fill(5,1,"3", "True")
    board.fill(5,2,"9", "True")
    board.fill(5,4,"8", "True")
    board.fill(5,7,"4", "True")

    board.fill(6,1,"4", "True")
    board.fill(6,3,"6", "True")
    board.fill(6,5,"1", "True")

    board.fill(7,5,"9", "True")
    board.fill(7,8,"1", "True")

    board.fill(8,7,"8", "True")
    board.fill(8,9,"5", "True")

    board.fill(9,2,"3", "True")
    board.fill(9,3,"2", "True")
    board.fill(9,4,"7", "True")
    board.fill(9,5,"8", "True")
    board.fill(9,7,"6", "True")

    board.validate()
    board.brute_force_solve()
    board.console_print()
    #valid = True 
    #while board.not_solved():
    #    if not valid:
    #        print("Last Entry Was not a valid Entry")
    #    else:
    #        print("")

    #    board.console_print()
    #    x = input("Input Row: ")
    #    y = input("Input Column: ")
    #    value = input("Input Value: ")
    #    board.fill(int(x), int(y), f'{value}')
    #    valid = board.validate() 
    #    if not valid:
    #        board.fill(int(x), int(y), INVALID)
    #    clear()
main()
