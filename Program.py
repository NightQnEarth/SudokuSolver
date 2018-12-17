from Package.Sudoku import SudokuSolver
import Package.ExtractInputData as ExtractInputData
import sys
from Package.Exceptions import ExtractInputDataExceptions, IncorrectSudokuError
from Package.GUI import gui_create
from Package.Peek import peek


def print_puzzle(puzzle):
    for row in puzzle:
        print(row)


def print_error(error):
    print()
    print(error)
    sys.exit(error.return_exit_code())


def main():
    try:
        input_data_tuple_or_puzzle = ExtractInputData.input_puzzle()
    except ExtractInputDataExceptions as error:
        print_error(error)

    if isinstance(input_data_tuple_or_puzzle, list):
        puzzle = input_data_tuple_or_puzzle
        print_puzzle(puzzle)
    else:
        puzzle = input_data_tuple_or_puzzle[0]
        additional_params = input_data_tuple_or_puzzle[1]
        list_of_first_rule_point = input_data_tuple_or_puzzle[2]
        solve = input_data_tuple_or_puzzle[3]

        if solve and additional_params.gui_off:
            print_puzzle(puzzle)
            print()
            print_puzzle(solve)
        else:
            if additional_params.generate:
                print_puzzle(puzzle)
                print()

            try:
                solutions = SudokuSolver.solve(puzzle, additional_params,
                                               list_of_first_rule_point)
            except IncorrectSudokuError as error:
                print_error(error)

            if additional_params.gui_off:
                try:
                    check_empty = peek(solutions)
                    if check_empty is None:
                        print('Решений нет.')
                    else:
                        solutions = check_empty[1]
                        for solution in solutions:
                            print_puzzle(solution)
                            print()
                except IncorrectSudokuError as error:
                    print_error(error)
            else:
                try:
                    gui_create(solutions)
                except IncorrectSudokuError as error:
                    print_error(error)


if __name__ == '__main__':
    main()
