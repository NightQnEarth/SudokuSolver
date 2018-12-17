import sys
import argparse
import re
from Package.Classes import AdditionalParams, Point
from Package.Exceptions import *
from argparse import RawTextHelpFormatter
from Package.GenerateSudoku import SudokuGenerate


def create_argument_parser():
    version = "1.618"

    just_generate_help = ('Флаг-параметр --just-generate принимается, '
                          'если требуется подать на выход только '
                          'сгенерированное судоку.')
    filename_help = ('В качестве параметра запуска принимается имя файла с '
                     'судоку, которое вы хотите решить.')
    decisions_number_help = ('Количество вариантов решения судоку.\nЕсли '
                             'необходимы все решения, задать равным -1.')
    classic_entry_help = ('Флаг-параметр --classic-entry принимается, '
                          'в случае если пользователь\nне хочет использовать'
                          ' функцию быстрого ввода.')
    first_rule_help = ('Флаг-параметр --first-rule принимается, '
                       'если требуются только те решения судоку,\nу которых '
                       'разница значений указанных пользователем клеток  и '
                       'соседних с ними клеток не превосходит 2.')
    second_rule_help = ('Максимальное количество повторяющихся элементов на'
                        ' каждой диагонали судоку.')
    description = ('Это программа для решения судоку лёгкого и среднего '
                   'уровней сложности.')
    epilog = ('\n\nКод выхода "0"  - Программа отработала успешно.\nКод '
              'выхода "1"  - Не введено ни одной строки судоку.'
              '\nКод выхода "2"  - Неверный размер судоку. Вводимое '
              'судоку должно иметь размер (N^2)x(N^2).\nКод выхода "3"  - '
              'Неверный формат ввода строки судоку.'
              '\nКод выхода "4"  - Неверно задан параметр -n.\nКод выхода '
              '"5"  - Изначально некорректно заданное судоку,'
              ' то есть заполнение пазла не'
              ' соответствует классическим правилам игры.\nКод выхода "6"  -'
              ' После введения параметра '
              '-f пользователем не было введено ни одной точки.\nКод '
              'выхода "7"  - Координаты введённой точки не '
              'соответствуют размеру введённого судоку.'
              '\nКод выхода "8"  - Неверно задан параметр -s.\nКод выхода "9" '
              ' - Неверный формат ввода строки с точкой.\nКод выхода "10" - '
              'Неверно задан размер для генерации судоку.\nКод выхода "11" - '
              'Неверно задан процент заполнения генерируемого судоку.\nКод '
              'выхода "12" - Введено неверное число параметров '
              'генерации судоку.\n"13" - Не введены команды "s" или "g".'
              '\n\nMay 2017, Ural Federal '
              'University')
    subparsers_description = 'Генерируется и решается произвольное судоку.'
    generate_help = ('Первыми обязательными параметрами задаются размер '
                     'желаемого судоку и процент его заполнения.')
    subparsers_help = ('Для запуска в стандартном режиме вводится команда '
                       '"s".\nДля получения справки введите "s '
                       '--help".\n\nДля запуска в режиме генератора вводится '
                       'команда "g"\nДля получения справки введите "g '
                       '--help".')
    gui_output_help = ('Введите "--GUI-off" или "-i", чтобы отключить '
                       'графический интерфейс.')

    parser = argparse.ArgumentParser(
        prog='SudokuSolver',
        description=description,
        epilog=epilog,
        add_help=False,
        formatter_class=RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(
        title='Команды',
        description=subparsers_description,
        help=subparsers_help,
        metavar='s|g'
    )
    param_group = parser.add_argument_group(
        title='Параметры запуска'
    )
    param_group.add_argument(
        '--help', '-h',
        action='help',
        help='Справка по использванию программы.'
    )
    parser_generator = subparsers.add_parser(
        'g',
        add_help=False
    )
    generator_param_group = parser_generator.add_argument_group(
        title='Параметры запуска'
    )
    generator_param_group.add_argument(
        '--help', '-h',
        action='help',
        help='Справка по использванию программы.'
    )
    generator_param_group.add_argument(
        'size_percent',
        nargs=2,
        type=int,
        help=generate_help,
    )
    generator_param_group.add_argument(
        '--decisions-number', '-n',
        type=int,
        default=1,
        help=decisions_number_help,
        metavar=''
    )
    generator_param_group.add_argument(
        '--first-rule', '-f',
        action='store_const',
        const=2,
        help=first_rule_help
    )
    generator_param_group.add_argument(
        '--second-rule', '-s',
        default=None,
        type=int,
        help=second_rule_help,
        metavar=''
    )
    generator_param_group.add_argument(
        '--GUI-off', '-i',
        action='store_true',
        help=gui_output_help
    )
    generator_param_group.add_argument(
        '--just-generate', '-j',
        action='store_true',
        help=just_generate_help
    )
    standard_parser = subparsers.add_parser(
        's',
        add_help=False
    )
    standard_param_group = standard_parser.add_argument_group(
        title='Параметры запуска'
    )
    mutually_exclusive_params = \
        standard_param_group.add_mutually_exclusive_group()

    mutually_exclusive_params.add_argument(
        '--help', '-h',
        action='help',
        help='Справка по использванию команды.\n'
    )
    mutually_exclusive_params.add_argument(
        '--version', '-v',
        action='version',
        help='Вывод версии программы.\n',
        version='%(prog)s {}'.format(version)
    )
    mutually_exclusive_params.add_argument(
        'filename',
        nargs='?',
        type=argparse.FileType(),
        help=filename_help
    )
    standard_param_group.add_argument(
        '--decisions-number', '-n',
        type=int,
        default=1,
        help=decisions_number_help,
        metavar=''
    )
    standard_param_group.add_argument(
        '--classic-entry', '-c',
        action='store_false',
        help=classic_entry_help
    )
    standard_param_group.add_argument(
        '--first-rule', '-f',
        action='store_const',
        const=2,
        help=first_rule_help
    )
    standard_param_group.add_argument(
        '--second-rule', '-s',
        default=None,
        type=int,
        help=second_rule_help,
        metavar=''
    )
    standard_param_group.add_argument(
        '--GUI-off', '-i',
        action='store_true',
        help=gui_output_help
    )

    return parser


def is_square(number):
    if number in {0, 1, 4, 9}:
        return True
    elif number > 9:
        for i in range(number // 2):
            if i**2 == number:
                return True
    return False


def check_correct_size(puzzle):
    row_count = len(puzzle)
    if row_count == 0 or not is_square(row_count):
        return False
    for row in puzzle:
        if len(row) != row_count:
            return False
    return True


def check_correct_point(puzzle, point):
    size = len(puzzle)
    return 0 <= point.row < size and 0 <= point.column < size


def transformation(source, quick_entry_flag):
    number_filter = re.compile(r'\d+')
    puzzle = []
    max_value = 0
    max_size = 0
    for line in source:
        row = []
        for value in number_filter.findall(line):
            row.append(int(value))
            if int(value) > max_value:
                max_value = int(value)
        if len(row) > max_size:
            max_size = len(row)
        puzzle.append(row)
    max_size = max(max_size, len(puzzle))
    new_size = max(max_size, max_value)

    if quick_entry_flag:
        for list_ in puzzle:
            if new_size != 0 and (new_size - len(list_)) < 0:
                raise IncorrectSudokuSizeError
            for j in range(new_size - len(list_)):
                list_.append(0)
        for i in range(new_size - len(puzzle)):
            puzzle.append([0 for _ in range(new_size)])

    if not check_correct_size(puzzle):
        raise IncorrectSudokuSizeError
    return puzzle


def read_sudoku(source):
    list_extract = re.compile(r'(\s*\[(?:\d+((,)|(, )|( )))*\d+\],?\s*\n*)')
    empty_line = re.compile(r'(\n|\s|\a|\t)+')
    list_of_line = []
    failed_line = 0
    for line in source:
        failed_line += 1
        if list_extract.fullmatch(line):
            list_of_line.append(line)
        elif empty_line.fullmatch(line):
            continue
        else:
            return failed_line

    if not list_of_line:
        raise NotEnteredSudokuError

    return list_of_line


def read_first_rule_points(source):
    point_extract = re.compile(r'\s*(\(\d+(?:(?:,)|(?: )|(?:, '
                               r'))\d+\))\s*\n*')
    coordinate_extract = re.compile(r'\d+')
    empty_line = re.compile(r'(\n|\s|\a|\t)+')
    list_of_points = []
    failed_line = 0
    flag_set = set()
    for line in source:
        failed_line += 1
        if point_extract.fullmatch(line):
            point = point_extract.fullmatch(line).group()
            row = int(coordinate_extract.findall(point)[0])
            col = int(coordinate_extract.findall(point)[1])
            if (row, col) not in flag_set:
                list_of_points.append(Point(row, col))
                flag_set.add((row, col))
        elif empty_line.fullmatch(line):
            continue
        else:
            return failed_line

    if len(list_of_points) == 0:
        raise NotEnteredPointsError
    return list_of_points


def input_puzzle():
    parser = create_argument_parser()

    try:
        parser.parse_args().decisions_number
    except AttributeError:
        parser.print_help()
        raise DidntChooseCommandError

    if 'size_percent' not in parser.parse_args():
        parser.add_argument(
            '--size_percent',
            default=None,
            required=False
        )
    namespace = parser.parse_args()

    additional_params = AdditionalParams(
        namespace.decisions_number,
        namespace.size_percent,
        namespace.first_rule,
        namespace.second_rule,
        namespace.GUI_off
    )
    solve = None

    if namespace.size_percent:
        if len(namespace.size_percent) != 2:
            raise IncorrectGenerateParamsCountError
        size = namespace.size_percent[0]
        percent = namespace.size_percent[1]
        if size <= 0:
            raise IncorrectGenerateSizeError
        elif not is_square(size):
            raise IncorrectSudokuSizeError
        elif not (0 <= percent <= 100):
            raise IncorrectGeneratePercentError
        if not namespace.second_rule and not namespace.first_rule and \
                namespace.decisions_number == 1:
            solve, puzzle = SudokuGenerate.generate_sudoku(size, percent, True)
        else:
            puzzle = SudokuGenerate.generate_sudoku(size, percent)

        if namespace.just_generate:
            return puzzle
    else:
        if namespace.filename:
            list_of_line_or_number = read_sudoku(namespace.filename)
        else:
            print('Введите судоку:')
            list_of_line_or_number = read_sudoku(sys.stdin)
        if not isinstance(list_of_line_or_number, int):
            list_of_line = list_of_line_or_number
            puzzle = transformation(list_of_line, namespace.classic_entry)
        else:
            failed_number = list_of_line_or_number
            raise IncorrectSudokuLineFormatError(failed_number)

    if not (additional_params.decisions_number > 0 or
            additional_params.decisions_number == -1):
        raise IncorrectDecisionsNumberError

    list_of_first_rule_point = []

    if additional_params.second_rule is not None:
        if additional_params.second_rule < 1:
            raise IncorrectSecondRuleParamError

    if additional_params.first_rule:
        print('Введите набор точек, для которых выполняется first-rule:')
        list_of_first_rule_point = read_first_rule_points(sys.stdin)
        if isinstance(list_of_first_rule_point, int):
            failed_number = list_of_first_rule_point
            raise IncorrectPointLineFormatError(failed_number)
        for point in list_of_first_rule_point:
            if not check_correct_point(puzzle, point):
                raise IncorrectPointCoordinatesError(point)

    return puzzle, additional_params, list_of_first_rule_point, solve
