"""sudoku.py
This is the base file for the Sudoku puzzle.
"""

import json
import math

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

    def add_hint(self, row: int, column: int, value: int):
        """ Add hints to the cell. Returns True if the hint was successfully set, otherwise
            returns False
        Keyword Arugments:
            row (int): The row of the cell to set.
            column (int): The column of the cell to set.
            value (int): The value to set for the cell.
                         Starter cells cannot be deleted
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

    def remove_hint(self, row: int, column: int, value: int):
        """ Remove hint from a cell. Returns True if the hint was successfully removed, otherwise
            returns False
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
        cell = self._get_cell(row, column)

        if cell[self.VALUE] == self.INVALID and cell[self.INITIAL] is False:
            if value in cell[self.HINTS]:
                cell[self.HINTS].remove(value)
            return True
        return False

    def get_hints(self, row: int, column: int):
        """ Get hints for cell. Returns the hints if found, otherwise returns empty list
        Keyword Arugments:
            row (int): The row of the cell to set.
            column (int): The column of the cell to set.
            value (int): The value to set for the cell.
            initial (bool) default: False: When set to true, this means this cell is a starter cell.
                                    Starter cells cannot be deleted
        """

        assert 0 < row <= self.size, "invalid row value"
        assert 0 < column <= self.size, "invalid column value"
        cell = self._get_cell(row, column)

        if cell[self.VALUE] == self.INVALID and cell[self.INITIAL] is False:
            return cell[self.HINTS]
        return []

    def solved(self):
        """ Returns True if the puzzle has been solved, False Otherwise
        """
        if self.find_empty() is None:
            return False
        return True

    def validate(self):
        """ Returns False if the puzzle is invalid, otherwise returns True 
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
        """ Returns False if the puzzle is invalid, otherwise returns True 
        """
        for cell in self.board:
            if cell['value'] == self.INVALID:
                return cell[self.ROW], cell[self.COLUMN]
        return None


    def brute_force_solve(self):
        """ Brute force solve the puzzle
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

    def _set_cell(self, row: int, column: int, value: int, initial: bool = False):
        """This will fill in the cell sepcified with the value, Returns True if
        successful, False otherwise.
        
        Keyword Arugments:
            row (int): The row of the cell to set.
            column (int): The column of the cell to set.
            value (int): The value to set for the cell.
            initial (bool) default: False: When set to true, this means this cell is a starter cell.
                                    Starter cells cannot be deleted
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
        """
        assert 0 < row <= self.size, "invalid row value"
        assert 0 < column <= self.size, "invalid column value"

        for cell in self.board:
            if cell[self.ROW] == row and cell[self.COLUMN] == column:
                return cell

        # Should never get here...
        assert False, "Why do we get here?"

    def _validate_row(self, row: int):
        """ Internal function to validate the given row in the puzzle. Returns False if invalid
            othwerise return True

        Keyword Arugments:
            row (int): The row of the cell verify.
        """
        answers = []
        for column in range(1, self.size):
            value = self._get_cell(row, column)[self.VALUE]
            if value is not self.INVALID:
                if value in answers:
                    return False
                answers.append(value)
        return True

    def _validate_column(self, column: int):
        """ Internal function to validate the given column in the puzzle. Returns False if invalid
            othwerise return True

        Keyword Arugments:
            column (int): The column of the cell verify.
        """

        answers = []
        for row in range(1, self.size):
            value = self._get_cell(row, column)[self.VALUE]
            if value is not self.INVALID:
                if value in answers:
                    return False
                answers.append(value)
        return True

    def _validate_block(self, block: int):
        """ Internal function to validate the given block in the puzzle. Returns False if invalid
            othwerise return True

        Keyword Arugments:
            block (int): The block of the cell verify.
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

    def _get_block(self, row: int, column: int):
        """ Returns the block the row and column should be in.
        Keyword Arugments:
            row (int): The row of the cell to set.
            column (int): The column of the cell to set.
        """
        rows = (row-1)//self.square_root
        columns = (column-1)//self.square_root
        block = (rows * self.square_root) + columns +1
        return block
