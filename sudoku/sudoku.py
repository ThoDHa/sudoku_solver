"""sudoku.py
This is the base file for the Sudoku puzzle.
"""
import sys
import json
import math
from enum import Enum
import random

class Puzzle:
    """
    This is the base class class for the sudoku puzzle
    """

    INVALID = -1
    ROW = "row"
    COLUMN = "column"
    VALUE = "value"
    HINTS = "hints"
    INITIAL = "Initial"

    class Difficulty(Enum):
        """ The levels of difficulty that can be had,
        """
        EASY = 1
        MEDIUM = 2
        HARD = 3
        EXTREME = 4

    def __init__(self, size : int):
        """This is to initalize the class,
        
        Keyword Arugments:
            size (int): The size of the board to build, needs to be square rootable
        """
        self.board = []
        self.size = size + 1
        self.square_root = math.sqrt(size)

        for row in range(1, self.size):
            for column in range(1, self.size):
                self.board.append(
                        {self.ROW: row,
                         self.COLUMN : column,
                         self.VALUE: self.INVALID,
                         self.HINTS: [],
                         self.INITIAL: False
                         }
                        )

    def fill(self, row: int, column: int, value: int, initial: bool = False):
        """This will fill in the cell sepcified with the value, Returns True if successfully set, 
        otherwise returns false 
        Keyword Arugments:
            row (int): The row of the cell to set.
            column (int): The column of the cell to set.
            value (int): The value to set for the cell.
            initial (bool) default: False: When set to true, this means this cell is a starter cell.
                                    Starter cells cannot be deleted
        """

        assert 0 < row <= self.size, "invalid row value"
        assert 0 < column <= self.size, "invalid column value"
        assert 0 < value <= self.size or value == -1, "invalid value"
        return self._set_cell(row, column, value, initial)

    def add_hint(self, row: int, column: int, value: int) -> bool:
        """ Add hints to the cell.
        Keyword Arugments:
            row (int): The row of the cell to set.

            column (int): The column of the cell to set.

            value (int): The value to set for the cell. Starter cells cannot be deleted

        Return:
            True if adding the hint is successful, False otherwise.
        """

        assert 0 < row <= self.size, "invalid row value"
        assert 0 < column <= self.size, "invalid column value"
        assert 0 < value <= self.size or value == -1, "invalid value"
        cell = self._get_cell(row, column)

        if cell[self.VALUE] == self.INVALID and cell[self.INITIAL] is False:
            if value not in cell[self.HINTS]:
                cell[self.HINTS].append(value)
            return True
        return False

    def remove_hint(self, row: int, column: int, value: int) -> bool:
        """ Remove hint from a cell.
        
        Keyword Arugments:
            row (int): The row of the cell to remove.

            column (int): The column of the cell to remove.

            value (int): The value to remove for the cell.

        Return:
            True if the remove is successul, False otherwise.
        """

        assert 0 < row <= self.size, "invalid row value"
        assert 0 < column <= self.size, "invalid column value"
        assert 0 < value <= self.size or value == -1, "invalid value"
        cell = self._get_cell(row, column)

        if cell[self.VALUE] == self.INVALID and cell[self.INITIAL] is False:
            if value in cell[self.HINTS]:
                cell[self.HINTS].remove(value)
            return True
        return False

    def get_hints(self, row: int, column: int):
        """ Get hints for cell.
        
        Keyword Arugments:
            row (int): The row of the cell to get the hint for.

            column (int): The column of the cell to get the hint for.

        Return:
            An list of possible values for the cell.
        """

        assert 0 < row <= self.size, "invalid row value"
        assert 0 < column <= self.size, "invalid column value"
        cell = self._get_cell(row, column)

        if cell[self.VALUE] == self.INVALID and cell[self.INITIAL] is False:
            return cell[self.HINTS]
        return []

    def solved(self) -> bool:
        """ Check to see if the puzzle is solved.

        Return:
            True if the board is solved, False otherwise.
        """
        if self.find_empty() is None:
            return False
        return True

    def validate(self) -> bool:
        """ Validate the current puzzle.

        Return:
            True if the current board is valid, False otherwise.
        """
        for row in range(1, self.size):
            if self._validate_row(row) is False:
                return False

        for column in range(1, self.size):
            if self._validate_column(column) is False:
                return False

        for block in range(1, self.size):
            if self._validate_block(block) is False:
                return False
        return True

    def find_empty(self):
        """ Find the first empty cell in the puzzle.

        Return:
            The cell if a empty cell is found, None if there are no empty cells.
        """
        for cell in self.board:
            if cell['value'] == self.INVALID:
                return cell[self.ROW], cell[self.COLUMN]
        return None


    def brute_force_solve(self) -> bool:
        """ Brute force solve the Puzzle

        Return:
            True once a solution is found, otherwise return false.
        """
        find = self.find_empty()
        if not find:
            return True
        row, column = find

        for i in range(1, self.size):
            self.fill(row, column, i)
            if self.validate() is True:
                if self.brute_force_solve():
                    return True
            self.fill(row, column, self.INVALID)
        return False

    def __str__(self):
        """ Tells stuff how to convert this class to a string 
        """
        return json.dumps(self.board, ensure_ascii=False, indent=4)

    def pretty_print(self):
        """ Pretty prints the board in a CLI GUI. 
        """

        output = "   "
        for row in range(1, self.size):
            output += f'{row}' + " "

        output += "\n  "
        output += "-"*self.size*2
        output += "\n"

        for row in range(1, self.size):
            output += f'{row}' + " |"
            for column in range(1, self.size):
                value = self._get_cell(row, column)[self.VALUE]
                if value == self.INVALID:
                    output += "-"
                else:
                    output += f'{value}'

                if column%self.square_root == 0:
                    output += "|"
                else:
                    output += " "
                if column == (self.size -1):
                    output += " " + f'{row}'
            if row%self.square_root == 0:
                output += "\n"
                output += "  "

                output += "-"*self.size*2
            output += "\n"

        output += "   "
        for row in range(1, self.size):
            output += f'{row}' + " "
        output += "\n"

        print(output)

    def generate_board(self, difficulty: Difficulty = Difficulty.EASY):
        """ Generates a board with the given difficulty value. 
        """

        while True:
            print("Generating a new board")
            self._generate_board()
            print("Generation of board done, brute force solving the rest.")
            self.brute_force_solve()
            if not self.find_empty():
                break
        if difficulty:
            pass

    def _generate_board(self):
        seed_value = random.randrange(sys.maxsize)
        random.seed(seed_value)
        max_cells = (self.size-1) * (self.size-1)
        end = max_cells*.80
        for _ in range(0, math.ceil(end)):
            while True:
                value =  random.randint(1,self.size-1)
                row =  random.randint(1,self.size-1)
                column =  random.randint(1,self.size-1)
                self.fill(row, column, value)
                if self.validate():
                    self.pretty_print()
                    break
                self.fill(row, column, self.INVALID)

    def _set_cell(self, row: int, column: int, value: int, initial: bool = False):
        """This will fill in the cell sepcified with the value.
        
        Keyword Arugments:
            row (int): The row of the cell to set.

            column (int): The column of the cell to set.
            
            value (int): The value to set for the cell.

            initial (bool) default: False: When set to true, this means this cell is a starter cell.
            Starter cells cannot be deleted.

        Return:
            True if the set is successfull, false otherwise.
        """
        assert 0 < row <= self.size, "invalid row value"
        assert 0 < column <= self.size, "invalid column value"

        for cell in self.board:
            if cell[self.ROW] == row and cell[self.COLUMN] == column:
                if cell[self.INITIAL] is not True:
                    cell[self.VALUE] = value
                    cell[self.INITIAL] = initial
                    return True
                return False

        return False

    def _get_cell(self, row: int, column: int):
        """ Internal function to get the cell given the row and column.
            If you can find the Cell then return the cell, otherwise return None
        
        Keyword Arugments:
            row (int): The row of the cell to set.

            column (int): The column of the cell to set.

        Return:
            Return the cell from the row and column
        """
        assert 0 < row <= self.size, "invalid row value"
        assert 0 < column <= self.size, "invalid column value"

        for cell in self.board:
            if cell[self.ROW] == row and cell[self.COLUMN] == column:
                return cell

        # Should never get here...
        assert False, "Why do we get here?"

    def _validate_row(self, row: int) -> bool:
        """ Internal function to validate the given row in the puzzle.

        Keyword Arugments:
            row (int): The row of the cell verify.

        Returns:
            True if the row is valid, False otherwise.
        """
        answers = []
        for column in range(1, self.size):
            value = self._get_cell(row, column)[self.VALUE]
            if value is not self.INVALID:
                if value in answers:
                    return False
                answers.append(value)
        return True

    def _validate_column(self, column: int) ->bool:
        """ Internal function to validate the given column in the puzzle.

        Keyword Arugments:
            column (int): The column of the cell verify.

        Return:
            True if the column is valid, False otherwise.
        """

        answers = []
        for row in range(1, self.size):
            value = self._get_cell(row, column)[self.VALUE]
            if value is not self.INVALID:
                if value in answers:
                    return False
                answers.append(value)
        return True

    def _validate_block(self, block: int) ->bool:
        """ Internal function to validate the given block in the puzzle.

        Keyword Arugments:
            block (int): The block of the cell verify.

        Returns:
            True if the block is valid, false otherwise.
        """
        answers = []
        for cell in self.board:
            if self._get_block(cell[self.ROW], cell[self.COLUMN]) is block:
                value = cell[self.VALUE]
                if value is not self.INVALID:
                    if value in answers:
                        return False
                    answers.append(value)
        return True

    def _get_block(self, row: int, column: int):
        """ Returns the block the row and column should be in.
        
        Keyword Arugments:
            row (int): The row of the cell to set.
            
            column (int): The column of the cell to set.

        Returns:
            The block the cell belongs in.
        """
        rows = (row-1)//self.square_root
        columns = (column-1)//self.square_root
        block = (rows * self.square_root) + columns +1
