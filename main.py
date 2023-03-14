import json
import os
INVALID = "-1"
clear = lambda: os.system('clear')
class Board:

    def __init__(self):
        self.board = []

        for x in range(1, 10):
            for y in range(1, 10):
                self.board.append({"x": x, "y": y, "value": INVALID, "hints": [], "initial": "False"})
    def fill(self, x, y, value, initial="False"):
        assert 0 < x <= 9, "invalid row value"
        assert 0 < y <= 9, "invalid column value"
        assert 0 < int(value) <= 9 or int(value) == -1, "invalid value"
        return self._set_cell(x, y, value, initial)

    def not_solved(self):
        for x in range(1, 10):
            for y in range(1, 10):
                value = self._get_cell(x, y)['value']
                if value is INVALID:
                    return True
        return False

    def validate(self):
        for x in range(1, 10):
            if self._validate_row(x) is False:
                return False 
        for y in range(1, 10):
            if self._validate_column(y) is False:
                return False 
    
        for block in range(1, 10):
            if self._validate_block(block) is False:
                return False
        return True

    def find_empty(self):
        for x in range(1, 10):
            for y in range(1, 10):
                value = self._get_cell(x, y)['value']
                if value is INVALID:
                    return (x, y)
        return None


    def brute_force_solve(self):
        find = self.find_empty()
        if not find:
            return True
        else:
            x, y = find
        value = self._get_cell(x, y)['value']
        for i in range(1, 10):
            self.fill(x, y, i)
            clear()
            self.console_print()
            if self.validate() is True:
                if self.brute_force_solve():
                    return True
            self.fill(x, y, INVALID)
        return False
    def __str__(self):
        return json.dumps(self.board, ensure_ascii=False, indent=4)

    def _set_cell(self, x, y, value, initial = "False"):
        for cell in self.board:
            if cell['x'] == x and cell['y'] == y:
                if cell['initial'] != "True":
                    cell['value'] = f'{value}'
                    cell['initial'] = initial
                    return True
                else:
                    return False

    def _get_cell(self, x, y):
        for cell in self.board:
            if cell['x'] == x and cell['y'] == y:
                return cell

    def _validate_row(self, x):
        answers = []
        for y in range(1, 10):
            value = self._get_cell(x, y)['value']
            if value is not INVALID:
                if value in answers:
                    return False
                else:
                    answers.append(value)
        return True

    def _validate_column(self, y):
        answers = []
        for x in range(1, 10):
            value = self._get_cell(x, y)['value']
            if value is not INVALID:
                if value in answers:
                    return False
                else:
                    answers.append(value)
        return True

    def _validate_block(self, block):
        answers = []
        for x in range(1, 10):
            for y in range(1, 10):
                if self._get_block(x, y) is block:
                    value = self._get_cell(x, y)['value']
                    if value is not INVALID:
                        if value in answers:
                            return False
                        else:
                            answers.append(value)
        return True

    def console_print(self):
        str = "   1 2 3 4 5 6 7 8 9\n"
        str += "   -----------------\n"
        for x in range(1, 10):
            str += x.__str__() + " |"
            for y in range(1, 10):
                value = self._get_cell(x, y)['value']
                if value == INVALID:
                    str += "-"
                else:
                    str += value

                if y%3 == 0:
                    str += "|"
                else:
                    str += " "
                if y == 9:
                    str += " " + x.__str__()
            if x%3 == 0:
                str += "\n   -----------------\n"
            else:
                str += "\n"

        str += "   1 2 3 4 5 6 7 8 9\n"
        print(str)                

    def _get_block(self, x, y):
        row = (x-1)//3
        column = (y-1)//3
        block = (row * 3) + column +1
        return block
def main():
    board = Board()
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
    valid = True 
    while board.not_solved():
        if not valid:
            print("Last Entry Was not a valid Entry")
        else:
            print("")

        board.console_print()
        x = input("Input Row: ")
        y = input("Input Column: ")
        value = input("Input Value: ")
        board.fill(int(x), int(y), f'{value}')
        valid = board.validate() 
        if not valid:
            board.fill(int(x), int(y), INVALID)
        clear()
main()
