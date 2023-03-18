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
                        {"row": row,
                         "column" : column, 
                         "value": self.INVALID, 
                         "hints": [], 
                         "initial": False
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

    def not_solved(self):
        """ Returns True if the puzzle has been solved, False Otherwise
        """
        if self.find_empty() is None:
            return True
        return False

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
                return cell['row'], cell['column']
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
#            time.sleep(30/1000)
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
            if cell["row"] == row and cell["column"] == column:
                if cell['initial'] is not True:
                    cell['value'] = value
                    cell['initial'] = initial
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
            if cell["row"] == row and cell["column"] == column:
                return cell

        # Should never get here...
        return self.board[1][1]
    def _validate_row(self, row: int):
        """ Internal function to validate the given row in the puzzle. Returns False if invalid
            othwerise return True

        Keyword Arugments:
            row (int): The row of the cell verify.
        """
        answers = []
        for column in range(1, self.size):
            value = self._get_cell(row, column)['value']
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
            value = self._get_cell(row, column)['value']
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
            if self._get_block(cell['row'], cell['column']) is block:
                value = cell['value']
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
                value = self._get_cell(row, column)['value']
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
