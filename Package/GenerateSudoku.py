import math
import random
import copy
from Package.Classes import AdditionalParams, Point


class SudokuGenerate:
    @staticmethod
    def generate_sudoku(size, percent_fill, quick_answer_flag=False):
        count_not_zero_cell = round(size ** 2 * (percent_fill / 100))

        if count_not_zero_cell == 0 and not quick_answer_flag:
            return [[0 for j in range(size)] for i in range(size)]

        sqrt_size = int(math.sqrt(size))
        pattern = [[((i * sqrt_size + i // sqrt_size + j) % size + 1) for j in
                    range(size)] for i in range(size)]

        pattern = SudokuGenerate.shuffle(pattern)

        result = copy.deepcopy(pattern)

        not_zero_points = \
            [Point(i, j)
             for i in range(len(result))
             for j in range(len(result[i]))
             if result[i][j] != 0]

        while len(not_zero_points) != count_not_zero_cell:

            random_point = random.choice(not_zero_points)
            not_zero_points.remove(random_point)

            result[random_point.row][random_point.column] = 0

        if quick_answer_flag:
            return pattern, result

        return result

    @staticmethod
    def transposing(puzzle):
        copy_puzzle = copy.deepcopy(puzzle)
        return list(map(list, zip(*copy_puzzle)))

    @staticmethod
    def swap_rows_in_area(puzzle):
        copy_puzzle = copy.deepcopy(puzzle)
        if len(copy_puzzle) == 1:
            return copy_puzzle

        sqrt_size = int(math.sqrt(len(copy_puzzle)))

        random_area = random.randrange(0, sqrt_size)

        first_random_line = random.randrange(0, sqrt_size)
        second_random_line = random.randrange(0, sqrt_size)
        while first_random_line == second_random_line:
            second_random_line = random.randrange(0, sqrt_size)

        first_line_for_swap = random_area * sqrt_size + first_random_line
        second_line_for_swap = random_area * sqrt_size + second_random_line

        copy_puzzle[first_line_for_swap], copy_puzzle[second_line_for_swap] = \
            copy_puzzle[second_line_for_swap], copy_puzzle[first_line_for_swap]

        return copy_puzzle

    @staticmethod
    def swap_columns_in_area(puzzle):
        copy_puzzle = copy.deepcopy(puzzle)
        if len(copy_puzzle) == 1:
            return copy_puzzle

        copy_puzzle = SudokuGenerate.transposing(copy_puzzle)
        copy_puzzle = SudokuGenerate.swap_rows_in_area(copy_puzzle)
        return SudokuGenerate.transposing(copy_puzzle)

    @staticmethod
    def swap_horizontal_area(puzzle):
        copy_puzzle = copy.deepcopy(puzzle)
        if len(copy_puzzle) == 1:
            return copy_puzzle

        sqrt_size = int(math.sqrt(len(copy_puzzle)))

        first_random_area = random.randrange(0, sqrt_size)
        second_random_area = random.randrange(0, sqrt_size)
        while first_random_area == second_random_area:
            second_random_area = random.randrange(0, sqrt_size)

        for i in range(sqrt_size):
            first_line_for_swap, second_line_for_swap =\
                first_random_area * sqrt_size + i,\
                second_random_area * sqrt_size + i
            copy_puzzle[first_line_for_swap], \
                copy_puzzle[second_line_for_swap] = \
                copy_puzzle[second_line_for_swap],\
                copy_puzzle[first_line_for_swap]

        return copy_puzzle

    @staticmethod
    def swap_vertical_area(puzzle):
        copy_puzzle = copy.deepcopy(puzzle)
        if len(copy_puzzle) == 1:
            return copy_puzzle

        copy_puzzle = SudokuGenerate.transposing(copy_puzzle)
        copy_puzzle = SudokuGenerate.swap_horizontal_area(copy_puzzle)
        return SudokuGenerate.transposing(copy_puzzle)

    @staticmethod
    def shuffle(puzzle):
        shuffle_funcs = [
            SudokuGenerate.transposing,
            SudokuGenerate.swap_rows_in_area,
            SudokuGenerate.swap_columns_in_area,
            SudokuGenerate.swap_horizontal_area,
            SudokuGenerate.swap_vertical_area
        ]
        shuffle_count = random.randint(15, 200)
        for i in range(shuffle_count):
            random_index = random.randint(0, len(shuffle_funcs) - 1)
            puzzle = shuffle_funcs[random_index](puzzle)
        return puzzle
