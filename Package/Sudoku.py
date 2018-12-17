import copy
import math
from Package.Classes import Point
from Package.Exceptions import IncorrectSudokuError


class SudokuSolver:
    @staticmethod
    def solve(puzzle, additional_params, list_of_first_rule_point):
        if not additional_params.generate:
            not_correct_location = SudokuSolver.check_correctly_puzzle(puzzle)

            if type(not_correct_location) is Point:
                raise IncorrectSudokuError(not_correct_location.row,
                                           not_correct_location.column)

        found_solvers = []

        solution = copy.deepcopy(puzzle)

        all_solutions_flag = False
        if additional_params.decisions_number == -1:
            all_solutions_flag = True

        while (len(found_solvers) < additional_params.decisions_number or
                all_solutions_flag)\
                and SudokuSolver.solve_helper(solution, found_solvers):
            found_solvers.append(solution)
            if additional_params.first_rule and additional_params.second_rule:
                if (SudokuSolver.check_first_rule(
                        solution,
                        list_of_first_rule_point,
                        additional_params.first_rule)
                    and
                        SudokuSolver.check_second_rule(
                            solution,
                            additional_params.second_rule)):
                    yield solution
            elif additional_params.first_rule:
                if SudokuSolver.check_first_rule(
                        solution,
                        list_of_first_rule_point,
                        additional_params.first_rule):
                    yield solution
            elif additional_params.second_rule:
                if SudokuSolver.check_second_rule(
                        solution,
                        additional_params.second_rule):
                    yield solution
            else:
                yield solution
            solution = copy.deepcopy(puzzle)

    @staticmethod
    def solve_helper(solution, found_solvers):
        size = len(solution)
        while True:
            cell_with_min_count_possible_value = None
            for row_index in range(size):
                for column_index in range(size):
                    # Если в клетке уже есть значение, переходим к следующей
                    if solution[row_index][column_index] != 0:
                        continue

                    possible_values = SudokuSolver.find_possible_values(
                        row_index, column_index, solution)
                    possible_value_count = len(possible_values)
                    # Если нет возможных вариантов, тогда судоку не имеет
                    # решения.
                    if possible_value_count == 0:
                        return False
                    # Если вариант один, тогда сразу заполняем клетку
                    if possible_value_count == 1:
                        solution[row_index][column_index] = \
                            possible_values.pop()
                    # Постоянно обновляем клетку, с минимальным числом
                    # вариантов
                    if not cell_with_min_count_possible_value or \
                       possible_value_count < len(
                                cell_with_min_count_possible_value[1]):
                        cell_with_min_count_possible_value = \
                            ((row_index, column_index), possible_values)
            # Если нет такой клетки, и нас не выкинуло раньше с False,
            # тогда судоку решено
            if not cell_with_min_count_possible_value and solution not in \
                    found_solvers:
                return True
            elif (not cell_with_min_count_possible_value and solution in
                  found_solvers)\
                    or len(cell_with_min_count_possible_value[1]) > 1:
                break
            # Если в клетке с минимальным числом вариантов число вариантов
                # больше 1, тогда этот алгоритм нам пока не поможет.
            # Выходим из цикла
            # Или, если найденное решение уже содержится в found_solvers,
            # тогда нам нужно выйти из этой ветки рекурсии
        # Далее brute force, просто перебираем варианты.
        if solution not in found_solvers:
            r, c = cell_with_min_count_possible_value[0]
            for v in cell_with_min_count_possible_value[1]:
                solution_copy = copy.deepcopy(solution)
                solution_copy[r][c] = v
                if SudokuSolver.solve_helper(solution_copy, found_solvers):
                    for r in range(size):
                        for c in range(size):
                            solution[r][c] = solution_copy[r][c]
                    return True
            return False

    @staticmethod
    def find_possible_values(row_index, column_index, puzzle):
        size = len(puzzle)
        values = {v for v in range(1, size + 1)}
        values -= SudokuSolver.get_row_values(row_index, puzzle)
        values -= SudokuSolver.get_column_values(column_index, puzzle)
        values -= SudokuSolver.get_block_values(row_index, column_index,
                                                puzzle)
        return values

    @staticmethod
    def get_row_values(row_index, puzzle):
        return set(puzzle[row_index][:])

    @staticmethod
    def get_column_values(column_index, puzzle):
        size = len(puzzle)
        return {puzzle[r][column_index] for r in range(size)}

    @staticmethod
    def get_block_values(row_index, column_index, puzzle):
        size = len(puzzle)
        sqrt_size = int(math.sqrt(size))
        block_row_start = sqrt_size * (row_index // sqrt_size)
        block_column_start = sqrt_size * (column_index // sqrt_size)
        return {puzzle[block_row_start + r][block_column_start + c]
                for r in range(sqrt_size)
                for c in range(sqrt_size)
                }

    @staticmethod
    def check_correct_cell(row_index, column_index, puzzle):
        suspicious_value = puzzle[row_index][column_index]
        temporary_puzzle = copy.deepcopy(puzzle)
        temporary_puzzle[row_index][column_index] = 0
        ban_values = \
            (SudokuSolver.get_row_values(row_index, temporary_puzzle) |
             SudokuSolver.get_column_values(column_index, temporary_puzzle)
             | SudokuSolver.get_block_values(row_index, column_index,
                                             temporary_puzzle))

        return suspicious_value not in ban_values

    @staticmethod
    def check_correctly_puzzle(puzzle):
        size = len(puzzle)
        for r in range(size):
            for c in range(size):
                if puzzle[r][c] == 0:
                    continue

                if puzzle[r][c] > size or not \
                        SudokuSolver.check_correct_cell(r, c, puzzle):
                    return Point(r, c)
        return True

    @staticmethod
    def check_first_rule(puzzle, list_of_first_rule_point,
                         first_rule_constant):
        size = len(puzzle)
        for point in list_of_first_rule_point:
            neighbor_points = {Point(point.row + i, point.column + j)
                               for i in range(-1, 2)for j in range(-1, 2)
                               if 0 <= point.row + i < size and 0 <=
                               point.column + j < size and abs(i + j) == 1}

            for neighbor_point in neighbor_points:
                if abs(puzzle[point.row][point.column] - puzzle[
                       neighbor_point.row][neighbor_point.column]) > \
                        first_rule_constant:
                    return False
        return True

    @staticmethod
    def find_max_count_reiteration_in_list(list_):
        max_count = 0
        for element_ in list_:
            suspicious_element = element_
            count = 0
            for _element in list_:
                if _element == suspicious_element:
                    count += 1
            if count > max_count:
                max_count = count
        return max_count

    @staticmethod
    def check_second_rule(puzzle, second_rule_constant):
        size = len(puzzle)
        general_diagonal = [puzzle[i][i] for i in range(size)]
        collateral_diagonal = [puzzle[i][size-i-1] for i in range(size)]

        return not (
            SudokuSolver.find_max_count_reiteration_in_list(
                general_diagonal) > second_rule_constant or
            SudokuSolver.find_max_count_reiteration_in_list(
                collateral_diagonal) > second_rule_constant)
