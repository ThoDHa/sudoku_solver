import json
import math

class Puzzle:

    INVALID = "-1"

    def __init__(self, size):
        self.board = []
        self.size = size + 1
        self.square_root = math.sqrt(size)

        for row in range(1, self.size):
            for column in range(1, self.size):
                self.board.append({"row": row, "column" : column, "value": self.INVALID, "hints": [], "initial": "False"})

    def fill(self, row, column, value, initial="False"):
        assert 0 < row <= 9, "invalid row value"
        assert 0 < column <= 9, "invalid column value"
        assert 0 < int(value) <= 9 or int(value) == -1, "invalid value"
        return self._set_cell(row, column, value, initial)

    def not_solved(self):
        for row in range(1, self.size):
            for column in range(1, self.size):
                value = self._get_cell(row, column)['value']
                if value is self.INVALID:
                    return True
        return False

    def validate(self):
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
        for cell in self.board:
            if cell['value'] == self.INVALID:
                return cell['row'], cell['column']
        return None


    def brute_force_solve(self):
        find = self.find_empty()
        if not find:
            return True
        else:
            row, column = find

        value = self._get_cell(row, column)['value']

        for i in range(1, self.size):
            self.fill(row, column, i)
#            time.sleep(30/1000)
            if self.validate() is True:
                if self.brute_force_solve():
                    return True
            self.fill(row, column, self.INVALID)
        return False

    def __str__(self):
        return json.dumps(self.board, ensure_ascii=False, indent=4)

    def _set_cell(self, x, y, value, initial = "False"):
        for cell in self.board:
            if cell["row"] == x and cell["column"] == y:
                if cell['initial'] != "True":
                    cell['value'] = f'{value}'
                    cell['initial'] = initial
                    return True
                else:
                    return False

    def _get_cell(self, x, y):
        for cell in self.board:
            if cell["row"] == x and cell["column"] == y:
                return cell

    def _validate_row(self, row):
        answers = []
        for column in range(1, self.size):
            value = self._get_cell(row, column)['value']
            if value is not self.INVALID:
                if value in answers:
                    return False
                else:
                    answers.append(value)
        return True

    def _validate_column(self, column):
        answers = []
        for row in range(1, self.size):
            value = self._get_cell(row, column)['value']
            if value is not self.INVALID:
                if value in answers:
                    return False
                else:
                    answers.append(value)
        return True

    def _validate_block(self, block):
        answers = []
        for cell in self.board:
            if self._get_block(cell['row'], cell['column']) is block:
                value = cell['value']
                if value is not self.INVALID:
                    if value in answers:
                        return False
                    answers.append(value)
        return True

    def console_print(self):
        str = "   "
        for row in range(1, self.size):
            str += f'{row}' + " "

        str += "\n  "
        for i in range(1, self.size*2):
            str += "-"

        str += "\n"
        for row in range(1, self.size):
            str += row.__str__() + " |"
            for column in range(1, self.size):
                value = self._get_cell(row, column)['value']
                if value == self.INVALID:
                    str += "-"
                else:
                    str += value

                if column%self.square_root == 0:
                    str += "|"
                else:
                    str += " "
                if column == (self.size -1):
                    str += " " + f'{row}'
            if row%self.square_root == 0:
                str += "\n"
                str += "  "
                for i in range(1, self.size*2):
                    str += "-"
                str += "\n"
            else:
                str += "\n"

        str += "   "
        for row in range(1, self.size):
            str += f'{row}' + " "
        str += "\n"

        print(str)                

    def _get_block(self, x, y):
        row = (x-1)//self.square_root
        column = (y-1)//self.square_root
        block = (row * self.square_root) + column +1
        return block
