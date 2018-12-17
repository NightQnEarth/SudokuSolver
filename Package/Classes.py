class AdditionalParams:
    def __init__(self, decisions_number=1, generate=None, first_rule=None,
                 second_rule=None, gui_off=None):
        self.decisions_number = decisions_number
        self.generate = generate
        self.first_rule = first_rule
        self.second_rule = second_rule
        self.gui_off = gui_off

    def __repr__(self):
        return 'AdditionalParams({!r}, {!r}, {!r}, {!r}, {!r})'\
            .format(self.decisions_number, self.generate, self.first_rule,
                    self.second_rule, self.gui_off)


class Point:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __str__(self):
        return '({}, {})'.format(self.row, self.column)
