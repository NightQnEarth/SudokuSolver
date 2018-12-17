import unittest
import tempfile
from Package.Exceptions import IncorrectSudokuSizeError, IncorrectSudokuError
from Package.Classes import AdditionalParams, Point
from Package.Sudoku import SudokuSolver
import Package.ExtractInputData as ExtractInputData


class Tests(unittest.TestCase):
    @staticmethod
    def check_correct_answer(generator):
        answer = []
        for solution in generator:
            answer.append(solution)
        for i in range(len(answer)):
            temp_list = answer[i]
            answer[i] = None
            if not SudokuSolver.check_correctly_puzzle(temp_list) \
                    or temp_list in answer:
                return False
        return True

    @staticmethod
    def create_situation(puzzle, number=1, first_rule=None,
                         second_rule=None, points=None):
        if not points:
            points = []
        additional_params = AdditionalParams(number, first_rule, second_rule)
        return Tests.check_correct_answer(SudokuSolver.solve(
            puzzle, additional_params, points))

    def test_duplication_in_row(self):
        input_puzzle = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 1]
        ]
        number = 1
        first_rule = None
        second_rule = None
        additional_params = AdditionalParams(number, first_rule, second_rule)
        list_of_first_rule_point = []

        with self.assertRaises(IncorrectSudokuError):
            list(SudokuSolver.solve(input_puzzle, additional_params,
                                    list_of_first_rule_point))

    def test_duplication_in_column(self):
        input_puzzle = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0]
        ]
        number = 1
        first_rule = None
        second_rule = None
        additional_params = AdditionalParams(number, first_rule, second_rule)
        list_of_first_rule_point = []

        with self.assertRaises(IncorrectSudokuError):
            list(SudokuSolver.solve(input_puzzle, additional_params,
                                    list_of_first_rule_point))

    def test_duplication_in_sector(self):
        input_puzzle = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        number = 1
        first_rule = None
        second_rule = None
        additional_params = AdditionalParams(number, first_rule, second_rule)
        list_of_first_rule_point = []

        with self.assertRaises(IncorrectSudokuError):
            list(SudokuSolver.solve(input_puzzle, additional_params,
                                    list_of_first_rule_point))

    def test_zero_sudoku(self):
        input_puzzle = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.assertTrue(Tests.create_situation(input_puzzle))

    def test_easy_sudoku(self):
        input_puzzle = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        self.assertTrue(Tests.create_situation(input_puzzle))

    def test_hardly_sudoku(self):
        input_puzzle = [
            [8, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 6, 0, 0, 0, 0, 0],
            [0, 7, 0, 0, 9, 0, 2, 0, 0],
            [0, 5, 0, 0, 0, 7, 0, 0, 0],
            [0, 0, 0, 0, 4, 5, 7, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 3, 0],
            [0, 0, 1, 0, 0, 0, 0, 6, 8],
            [0, 0, 8, 5, 0, 0, 0, 1, 0],
            [0, 9, 0, 0, 0, 0, 4, 0, 0]
        ]
        self.assertTrue(Tests.create_situation(input_puzzle))

    def test_resolved_sudoku(self):
        input_puzzle = [
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [4, 5, 6, 7, 8, 9, 1, 2, 3],
            [7, 8, 9, 1, 2, 3, 4, 5, 6],
            [2, 3, 1, 6, 7, 4, 8, 9, 5],
            [8, 7, 5, 9, 1, 2, 3, 6, 4],
            [6, 9, 4, 5, 3, 8, 2, 1, 7],
            [3, 1, 7, 2, 6, 5, 9, 4, 8],
            [5, 4, 2, 8, 9, 7, 6, 3, 1],
            [9, 6, 8, 3, 4, 1, 5, 7, 2]
        ]
        self.assertTrue(Tests.create_situation(input_puzzle))

    def test_zero_sudoku_and_big_decisions_count(self):
        input_puzzle = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.assertTrue(Tests.create_situation(input_puzzle))

    def test_zero_sudoku_1x1(self):
        input_puzzle = [[0]]
        self.assertTrue(Tests.create_situation(input_puzzle))

    def test_sudoku_1x1(self):
        input_puzzle = [[1]]
        self.assertTrue(Tests.create_situation(input_puzzle))

    def test_sudoku_4x4(self):
        input_puzzle = [
            [0, 1, 0, 0],
            [0, 0, 0, 2],
            [3, 0, 0, 0],
            [0, 0, 3, 0]
        ]
        self.assertTrue(Tests.create_situation(input_puzzle))

    def test_sudoku_16x16(self):
        input_puzzle = [
            [11, 14, 2, 0, 0, 8, 4, 12, 0, 5, 13, 15, 6, 1, 3, 16],
            [13, 0, 5, 0, 0, 0, 0, 7, 0, 6, 0, 0, 0, 0, 0, 11],
            [8, 0, 6, 16, 11, 0, 0, 0, 0, 0, 0, 3, 0, 4, 7, 12],
            [7, 0, 0, 0, 0, 6, 0, 3, 0, 0, 10, 11, 0, 2, 0, 0],
            [5, 0, 13, 12, 0, 0, 0, 0, 0, 3, 6, 0, 0, 15, 0, 0],
            [14, 0, 0, 6, 8, 5, 0, 2, 0, 0, 11, 0, 3, 0, 0, 7],
            [10, 9, 0, 0, 12, 0, 3, 11, 1, 13, 0, 0, 0, 0, 0, 8],
            [0, 0, 0, 0, 0, 0, 10, 6, 16, 8, 14, 0, 1, 0, 9, 2],
            [9, 2, 0, 14, 0, 11, 12, 13, 10, 1, 0, 0, 0, 0, 0, 0],
            [12, 0, 0, 0, 0, 0, 14, 16, 3, 11, 0, 6, 0, 0, 13, 4],
            [6, 0, 0, 15, 0, 3, 0, 0, 13, 0, 12, 14, 16, 0, 0, 5],
            [0, 0, 16, 0, 0, 1, 6, 0, 0, 0, 0, 0, 12, 11, 0, 9],
            [0, 0, 9, 0, 3, 2, 0, 0, 15, 0, 7, 0, 0, 0, 0, 13],
            [15, 13, 14, 0, 10, 0, 0, 0, 0, 0, 0, 8, 5, 7, 0, 1],
            [1, 0, 0, 0, 0, 0, 15, 0, 11, 0, 0, 0, 0, 14, 0, 3],
            [2, 3, 10, 7, 6, 4, 13, 0, 9, 14, 5, 0, 0, 16, 11, 15]
        ]
        self.assertTrue(Tests.create_situation(input_puzzle))

    def test_sudoku_25x25(self):
        input_puzzle = [
            [11, 1, 5, 18, 25, 0, 0, 0, 0, 0, 16, 4, 20, 2, 21, 0, 0, 0, 0, 0,
             15, 14, 17, 24, 12],
            [15, 0, 0, 0, 0, 4, 24, 0, 20, 9, 14, 22, 12, 7, 3, 25, 6, 0,
                18, 21, 0, 0, 0, 0, 5],
            [6, 0, 21, 20, 24, 22, 12, 0, 10, 0, 0, 0, 13, 0, 0, 0, 15,
                0, 14, 2, 19, 16, 3, 0, 7],
            [14, 0, 22, 0, 0, 3, 2, 18, 11, 17, 0, 0, 0, 0, 0, 23, 12, 1,
                24, 13, 0, 0, 4, 0, 25],
            [2, 0, 12, 0, 0, 21, 1, 0, 7, 0, 10, 6, 25, 24, 23, 0, 17, 0,
                5, 16, 0, 0, 18, 0, 13],
            [0, 5, 1, 22, 11, 0, 0, 0, 0, 0, 12, 16, 14, 21, 4, 0, 0, 0,
                0, 0, 18, 15, 19, 10, 0],
            [0, 6, 19, 10, 4, 0, 23, 9, 0, 11, 0, 0, 0, 0, 0, 12, 0, 21,
                20, 0, 16, 2, 25, 14, 0],
            [0, 0, 0, 21, 0, 0, 7, 2, 5, 19, 6, 15, 17, 1, 20, 10, 22,
                25, 13, 0, 0, 9, 0, 0, 0],
            [0, 17, 14, 2, 20, 0, 0, 10, 0, 22, 0, 9, 0, 19, 0, 15, 0, 6,
                0, 0, 5, 12, 23, 13, 0],
            [0, 24, 0, 13, 0, 0, 6, 17, 8, 4, 0, 23, 2, 3, 0, 14, 5, 18,
                16, 0, 0, 22, 0, 7, 0],
            [17, 15, 0, 0, 2, 19, 0, 25, 0, 0, 22, 11, 0, 14, 13, 0, 0,
                3, 0, 20, 9, 0, 0, 16, 4],
            [5, 20, 0, 0, 1, 17, 0, 22, 14, 2, 19, 0, 0, 0, 16, 4, 9, 15,
                0, 25, 8, 0, 0, 18, 11],
            [19, 4, 16, 0, 21, 18, 0, 1, 0, 7, 0, 0, 0, 0, 0, 5, 0, 24,
                0, 10, 23, 0, 2, 22, 20],
            [13, 11, 0, 0, 10, 15, 0, 4, 6, 24, 2, 0, 0, 0, 7, 19, 16, 8,
                0, 1, 17, 0, 0, 21, 14],
            [22, 18, 0, 0, 3, 13, 0, 21, 0, 0, 5, 20, 0, 25, 6, 0, 0, 7,
                0, 14, 10, 0, 0, 15, 19],
            [0, 22, 0, 8, 0, 0, 17, 14, 13, 18, 0, 25, 15, 16, 0, 3, 1,
                5, 21, 0, 0, 19, 0, 12, 0],
            [0, 23, 17, 1, 5, 0, 0, 11, 0, 21, 0, 19, 0, 4, 0, 16, 0, 12,
                0, 0, 7, 20, 13, 6, 0],
            [0, 0, 0, 11, 0, 0, 9, 20, 1, 16, 8, 14, 5, 18, 12, 7, 19,
                23, 2, 0, 0, 4, 0, 0, 0],
            [0, 16, 4, 19, 14, 0, 15, 7, 0, 12, 0, 0, 0, 0, 0, 11, 0, 13,
                17, 0, 25, 24, 8, 1, 0],
            [0, 7, 2, 15, 12, 0, 0, 0, 0, 0, 17, 21, 22, 13, 1, 0, 0, 0,
                0, 0, 14, 11, 16, 5, 0],
            [20, 0, 6, 0, 0, 9, 21, 0, 17, 0, 4, 1, 11, 23, 19, 0, 25, 0,
                10, 5, 0, 0, 14, 0, 16],
            [4, 0, 13, 0, 0, 2, 16, 6, 22, 5, 0, 0, 0, 0, 0, 21, 20, 9,
                3, 12, 0, 0, 7, 0, 8],
            [1, 0, 18, 3, 15, 11, 14, 0, 25, 0, 0, 0, 9, 0, 0, 0, 8, 0,
                4, 7, 24, 6, 10, 0, 22],
            [24, 0, 0, 0, 0, 7, 4, 0, 18, 1, 20, 13, 16, 22, 8, 6, 11, 0,
                19, 17, 0, 0, 0, 0, 2],
            [12, 14, 11, 5, 16, 0, 0, 0, 0, 0, 3, 2, 7, 6, 25, 0, 0, 0,
                0, 0, 20, 17, 21, 4, 9]
        ]
        self.assertTrue(Tests.create_situation(input_puzzle))

    def test_first_rule(self):
        input_puzzle = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        points = [Point(0, 0), Point(2, 1)]
        self.assertTrue(Tests.create_situation(input_puzzle, -1, 2,
                                               points=points))

    def test_second_rule(self):
        input_puzzle = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertTrue(Tests.create_situation(input_puzzle, -1, None, 2))

    def test_all_rule_together(self):
        input_puzzle = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        points = [Point(1, 3), Point(2, 0)]
        self.assertTrue(Tests.create_situation(input_puzzle, -1, 2, 3,
                                               points=points))

    def test_check_square(self):
        square_list = [i**2 for i in range(100)]
        for i in square_list:
            self.assertTrue(ExtractInputData.is_square(i))
        self.assertFalse(ExtractInputData.is_square(-100))

    def test_check_size(self):
        for i in range(1, 50):
            matrix = [[] for x in range(i)]
            for j in range(1, 50):
                for t in range(len(matrix)):
                    matrix[t] = [0 for y in range(j)]
                if ExtractInputData.is_square(i) and i == j:
                    self.assertTrue(ExtractInputData.check_correct_size(
                        matrix))
                else:
                    self.assertFalse(ExtractInputData.check_correct_size(
                        matrix))

    def test_transformation(self):
        list_of_lines = [
                            '[1, 2, 3, 4]',
                            '[5 6 7 8]',
                            '[9,10,11,12]',
                            '[12, 13, 14, 15]'
                        ]
        result = [
                    [1, 2, 3, 4],
                    [5, 6, 7, 8],
                    [9, 10, 11, 12],
                    [12, 13, 14, 15]
                 ]
        quick_flag = False
        self.assertEqual(ExtractInputData.transformation(list_of_lines,
                                                         quick_flag), result)

    def test_transformation_incorrect_input(self):
        list_of_lines = [
                            '[1, 2, 3, 4]',
                            '[5 6 7 8]',
                            '[9,10,11,12]'
                        ]
        quick_flag = False
        with self.assertRaises(IncorrectSudokuSizeError):
            ExtractInputData.transformation(list_of_lines, quick_flag)

    def test_quick_transformation(self):
        list_of_lines1 = [
                            '[1, 2, 3, 4]'
                         ]
        result1 = [
                    [1, 2, 3, 4],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                 ]
        quick_flag = True
        self.assertEqual(ExtractInputData.transformation(list_of_lines1,
                                                         quick_flag), result1)
        list_of_lines2 = [
                            '[0, 0, 0, 0]'
                         ]

        result2 = [
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                 ]
        self.assertEqual(ExtractInputData.transformation(list_of_lines2,
                                                         quick_flag), result2)

    def test_read_sudoku(self):
        source = tempfile.TemporaryFile('w+')
        source.write('[1, 2, 3, 4]\n'
                     '[1,2,3,4]\n'
                     '[1 2 3 4]\n')
        source.seek(0)

        result = [
                    '[1, 2, 3, 4]\n',
                    '[1,2,3,4]\n',
                    '[1 2 3 4]\n'
                 ]

        self.assertEqual(ExtractInputData.read_sudoku(source), result)
        source.close()

    def test_read_incorrect_sudoku(self):
        source = tempfile.TemporaryFile('w+')
        source.write('[1, 2, 3, 4]\n'
                     '[1,2,3,4\n'
                     '[1 2 3 4]\n')
        source.seek(0)

        result = 2

        self.assertEqual(ExtractInputData.read_sudoku(source), result)
        source.close()

    def test_read_points(self):
        source = tempfile.TemporaryFile('w+')
        source.write('(1, 2)\n'
                     '(1 2)\n'
                     '(1,2)\n')
        source.seek(0)

        result = ExtractInputData.read_first_rule_points(source)[0]

        self.assertIsInstance(result, Point)
        self.assertEqual((result.row, result.column), (1, 2))
        source.close()

    def test_read_fail_points(self):
        source = tempfile.TemporaryFile('w+')
        source.write('(1, 2)\n'
                     '(1 2)\n'
                     '(a,2)\n')
        source.seek(0)

        result = 3

        self.assertEqual(ExtractInputData.read_first_rule_points(source),
                         result)
        source.close()


if __name__ == '__main__':
    unittest.main()
