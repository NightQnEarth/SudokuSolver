class ExtractInputDataExceptions(Exception):
    pass


class NotEnteredSudokuError(ExtractInputDataExceptions):
    def __str__(self):
        return 'Вы не ввели ни одной строки судоку.'

    @staticmethod
    def return_exit_code():
        return 1


class IncorrectSudokuSizeError(ExtractInputDataExceptions):
    def __str__(self):
        return 'Некорректный размер судоку.'

    @staticmethod
    def return_exit_code():
        return 2


class IncorrectSudokuLineFormatError(ExtractInputDataExceptions):
    def __init__(self, line_number):
        self.line_number = line_number

    def __str__(self):
        return 'Неверный формат ввода судоку, строка ' \
               '{}.'.format(self.line_number)

    @staticmethod
    def return_exit_code():
        return 3


class IncorrectDecisionsNumberError(ExtractInputDataExceptions):
    def __str__(self):
        return 'Неверный ввод параметра -n.'

    @staticmethod
    def return_exit_code():
        return 4


class IncorrectSudokuError(Exception):
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __str__(self):
        return 'Некорректно задана позиция ({}, {}). Судоку не имеет ' \
               'решений.'.format(self.row, self.column)

    @staticmethod
    def return_exit_code():
        return 5


class NotEnteredPointsError(ExtractInputDataExceptions):
    def __str__(self):
        return 'Не введено ни одной точки.'

    @staticmethod
    def return_exit_code():
        return 6


class IncorrectPointCoordinatesError(ExtractInputDataExceptions):
    def __init__(self, point):
        self.point = point

    def __str__(self):
        return 'Координаты точки {} не соответствуют' \
               ' размеру введённого судоку.'.format(self.point)

    @staticmethod
    def return_exit_code():
        return 7


class IncorrectSecondRuleParamError(ExtractInputDataExceptions):
    def __str__(self):
        return 'Неверно задан параметр -s.'

    @staticmethod
    def return_exit_code():
        return 8


class IncorrectPointLineFormatError(ExtractInputDataExceptions):
    def __init__(self, line_number):
        self.line_number = line_number

    def __str__(self):
        return 'Неверный формат ввода точки, строка ' \
               '{}.'.format(self.line_number)

    @staticmethod
    def return_exit_code():
        return 9


class IncorrectGenerateSizeError(ExtractInputDataExceptions):
    def __str__(self):
        return 'Неверно задан размер для генерации судоку.'

    @staticmethod
    def return_exit_code():
        return 10


class IncorrectGeneratePercentError(ExtractInputDataExceptions):
    def __str__(self):
        return 'Неверно задан процент заполнения генерируемого судоку.'

    @staticmethod
    def return_exit_code():
        return 11


class IncorrectGenerateParamsCountError(ExtractInputDataExceptions):
    def __str__(self):
        return 'Введено неверное число параметров генерации судоку.'

    @staticmethod
    def return_exit_code():
        return 12


class DidntChooseCommandError(ExtractInputDataExceptions):
    def __str__(self):
        return 'Не введены команды "s" или "g".'

    @staticmethod
    def return_exit_code():
        return 13
