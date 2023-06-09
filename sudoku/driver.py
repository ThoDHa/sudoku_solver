"""driver.py
This is the basic driver for the sudoku puzzle
"""
from .sudoku import Puzzle

class Move:
    """ THe list of moves, so we can keep track of the moves tried.
    """
    def __init__(self, row: int, column: int, value: int, add: bool = True, notes: bool = False):
        """ Initialize the move

        Keyword Arguments
            row (int) -- The row to change the value of.
            column (int) -- The column to change the value of.
            value (int) -- The value to change the value of.
            notes (bool) -- Is it a note.
            value (bool) -- Are we adding or removing it (default False).
        """
        self.row = row
        self.column = column
        self.value = value
        self.add = add
        self.notes = notes

class Game:
    """ The basic driver for the game of sudoku puzzle.
    """

    def __init__(self):
        """ Initialize the game.
        """
        self.puzzle = Puzzle(9)
        self.puzzle.generate_board(Puzzle.Difficulty.EXTREME)
        self.moves = []

    def print_game(self):
        """ Print the game 
        """
        self.puzzle.pretty_print()
    def validate(self)->bool:
        """ Validate the current state of the game

        Return:
            True if the game is valid, false if invalid.
        """
        return self.puzzle.validate()

    def add(self, row: int, column: int, value: int, verify: bool = False):
        """ Add a value to a cell.

        Keyword Agurments:
            row (int) -- the column of the cell to get the hints for.

            column (int) -- the row of the cell to get the hints for.

            value (int) -- the value of the the cell to add.

            verify (bool) -- to validate the value of the cell (default false).

        Returns:
            True always if verify is false, otherwise return the value from the verify.
        """
        self.puzzle.fill(row, column, value)
        self.moves.append(Move(row, column, self.puzzle.INVALID))
        if verify:
            return self.puzzle.validate()
        return True

    def remove(self, row: int, column: int):
        """ Add a value to a cell. 
        Keyword Agurments:
            row (int) -- the column of the cell to get the hints for.

            column (int) -- the row of the cell to get the hints for.
        """
        self.puzzle.fill(row, column, self.puzzle.INVALID)
        self.moves.append(Move(row, column, self.puzzle.INVALID, add=False))

    def notes_add(self, row: int, column: int, value: int):
        """ Add the hints to a cell. 
        Keyword Agurments:
            row (int) -- the column of the cell to add the hints for.

            column (int) -- the row of the cell to add the hints for.
            
            value (int) -- the row of the cell to add the hints for.
        """
        return self.puzzle.add_hint(row, column, value)

    def notes_remove(self, row: int, column: int, value: int):
        """ Remove the hints from a cell. 
        Keyword Agurments:
            row (int) -- the column of the cell to remove the hints for.

            column (int) -- the row of the cell to remove the hints for.
            
            value (int) -- the row of the cell to remove the hints for.
        """
        return self.puzzle.remove_hint(row, column, value)

    def notes_get(self, row: int, column: int):
        """ Get the hints to a cell. 
        Keyword Agurments:
            row (int) -- the column of the cell to get the hints for.

            column (int) -- the row of the cell to get the hints for.
            
        """
        return self.puzzle.get_hints(row, column)
