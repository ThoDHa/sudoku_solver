"""main.py Initial driver for the sudoku Puzzle
"""
import os
import datetime
from os.path import isdir
from sudoku import sudoku
from sudoku import driver

def clear():
    """ Clears the console
    """
    os.system('clear')

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
    game = driver.Game()

    while True:
        game.print_game()
        print("")
        print("There are 3 modes to the games regular mode(1), enter notes(2), and view notes (3)")
        print("to validate the board as is, enter (4)")
        mode = input("Which mode do you want to enter? ")
        clear()
        if mode == "1":
            while True:
                print("Regular mode, to exit mode enter in a not int number for the value")
                print("")
                game.print_game()
                row = input("Input Row: ")
                column = input("Input Column: ")
                value = input("Input Value: ")
                if not value.lstrip("-").isdigit():
                    break
                game.add(int(row), int(column), int(value))
                clear()
        elif mode == "2":
            hints = []
            while True:
                print("Entering Notes Mode, to exit int in a str for the value")
                print("")
                if hints:
                    print(hints)
                game.print_game()
                add = input("Adding Notes (y/n): ")
                row = input("Input Row: ")
                column = input("Input Column: ")
                value = input("Input Value: ")
                if not value.lstrip("-").isdigit():
                    break
                if add == "y":
                    hints =  game.notes_add(int(row), int(column), int(value))
                else:
                    hints =  game.notes_remove(int(row), int(column), int(value))
                clear()

        elif mode == "3":
            while True:
                clear()
                print("View Notes Mode, to exit int in a str for the value")
                print("")
                game.print_game()
                row = input("Input Row: ")
                column = input("Input Column: ")
                if not row.lstrip("-").isdigit() or not column.lstrip("-").isdigit():
                    break
                print(game.notes_get(int(row), int(column)))
        elif mode == "4":
            if game.validate():
                print("The game is currently valid")

def timing_test():
    """ main function
    """
    times = []
    solutions = []
    for _ in range(1, 100):
        first = datetime.datetime.now()
        puzzle = sudoku.Puzzle(9)
        puzzle.generate_board(puzzle.Difficulty.EXTREME)
        now = datetime.datetime.now()
        generate = ((now-first).microseconds) /1000
        solutions.append(str(puzzle))

        first = datetime.datetime.now()
        puzzle.brute_force_solve()
        now = datetime.datetime.now()
        solve = ((now-first).microseconds) /1000
        times.append({"generate": f"{generate}ms", "solved": f"{solve}ms"})
        return times

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

def main():
    """ main function
    """
    #timing_test()
    console_game()
    #puzzle = generate_game()
    #brute_force()

main()
