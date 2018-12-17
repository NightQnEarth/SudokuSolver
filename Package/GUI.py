import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QDesktopWidget, QMessageBox, qApp, QAction,
    QGridLayout, QWidget, QStyle, QPushButton, QScrollArea, QVBoxLayout,
    QHBoxLayout, QLabel)
from PyQt5.QtGui import QFont, QCloseEvent
from PyQt5.QtCore import Qt, QCoreApplication
from Package.Peek import peek
import math
from enum import Enum


class Direction(Enum):
    Left = 1
    Right = 2


class Window(QMainWindow):
    def __init__(self, generator):
        super().__init__()
        self.generator = generator
        self.flag = True
        self.previous_solution_btm = QPushButton()
        self.next_solution_btm = QPushButton()
        self.toolbar = self.addToolBar('')
        self.message_box = QMessageBox()
        self.solutions_pool = []
        self.current_solutions_index = 0
        self.generator_is_end = False
        self.init_user_interface()

    def init_user_interface(self):
        self.resize(300, 350)
        self.setWindowIcon(self.style().standardIcon(
            QStyle.SP_TitleBarMenuButton))
        self.setWindowTitle('Sudoku Solver')
        self.arrows_create()
        self.statusBar()
        self.toolbar_create()
        check_empty = peek(self.generator)

        if check_empty is None:
            self.create_empty_message()
        else:
            self.generator = check_empty[1]
            self.solutions_pool.append(next(self.generator))
            central_widget = self.grid_create(
                self.solutions_pool[self.current_solutions_index], True)

        self.move_center()

        desktop_geometry = QApplication.desktop().availableGeometry()

        if not desktop_geometry.contains(
                self.frameGeometry()):
            scroll_area = QScrollArea()
            scroll_area.setWidget(central_widget)
            scroll_area.setWidgetResizable(True)
            scroll_area.setFocusPolicy(Qt.NoFocus)
            self.setCentralWidget(scroll_area)
            if desktop_geometry.width() <= \
                    self.frameSize().width():
                self.setFixedWidth(
                    desktop_geometry.width())
            if desktop_geometry.height() <= \
                self.frameSize().height() + \
                    scroll_area.horizontalScrollBar().height():
                self.setFixedHeight(
                    desktop_geometry.height() -
                    scroll_area.horizontalScrollBar().height())
            self.move_center()

        self.show()

    def keyPressEvent(self, key):
        if (key.key() == Qt.Key_Right or (key.key() == Qt.Key_Return and
            QApplication.focusWidget() == self.next_solution_btm)) and \
                self.next_solution_btm.isEnabled():
            self.next_solution_btm.clicked.emit()
        elif (key.key() == Qt.Key_Left or (key.key() == Qt.Key_Return and
              QApplication.focusWidget() == self.previous_solution_btm)) and \
                self.previous_solution_btm.isEnabled():
                self.previous_solution_btm.clicked.emit()
        elif key.key() == Qt.Key_Escape:
            self.closeEvent(QCloseEvent())
        elif (key.key() == Qt.Key_Return and not isinstance(self, Window) and
              QApplication.focusWidget() == self.exit_button):
            self.exit_button.clicked.emit()

    def move_center(self):
        self.move(self.width() * -2, 0)
        self.show()
        exact_window_form = self.frameGeometry()
        exact_desktop_center = QDesktopWidget().availableGeometry().center()
        exact_window_form.moveCenter(exact_desktop_center)
        self.move(exact_window_form.topLeft())

    def closeEvent(self, event):
        caption = 'Confirm Exit'
        question = 'Are you sure you want to exit Sudoku Solver?'
        reply = self.message_box.question(
            self,
            caption,
            question,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        if reply == self.message_box.Yes:
            QCoreApplication.exit()
        else:
            event.ignore()

    def toolbar_create(self):
        exit_action = QAction(self.style().standardIcon(
            QStyle.SP_DialogCloseButton), '', self)
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(qApp.quit)
        self.toolbar.setFloatable(False)

        self.toolbar.addAction(exit_action)

    def arrows_create(self):
        self.previous_solution_btm.setIcon(self.style().standardIcon(
            QStyle.SP_ArrowBack))
        self.previous_solution_btm.setStatusTip('Previous solution')
        self.previous_solution_btm.setFocusPolicy(Qt.NoFocus)

        self.next_solution_btm.setIcon(self.style().standardIcon(
            QStyle.SP_ArrowForward))
        self.next_solution_btm.setStatusTip('Next solution')
        self.next_solution_btm.setFocusPolicy(Qt.NoFocus)

        self.previous_solution_btm.clicked.connect(self.arrow_left)
        self.next_solution_btm.clicked.connect(self.arrow_right)

    def grid_create(self, puzzle, return_flag=False):
        central_widget = QWidget(self)
        if len(puzzle) == 1:
            grid = QGridLayout()
            grid.setSpacing(0)
            Window.simple_button_create(grid, puzzle)
            grid.addWidget(self.previous_solution_btm, 1, 0)
            grid.addWidget(self.next_solution_btm, 1, 1)
            central_widget.setLayout(grid)
        else:
            square_size = int(math.sqrt(len(puzzle)))
            v_box = QVBoxLayout()
            v_box.setSpacing(3)
            for i in range(square_size):
                h_box = QHBoxLayout()
                h_box.setSpacing(3)
                for j in range(square_size):
                    grid_square = QGridLayout()
                    grid_square.setSpacing(0)
                    for row in range(square_size):
                        for column in range(square_size):
                            Window.simple_button_create(
                                grid_square, puzzle,
                                row + square_size * i,
                                column + square_size
                                * j, row, column, 1, 1
                            )
                    if i + 1 == square_size:
                        if j == 0:
                            grid_square.addWidget(
                                self.previous_solution_btm,
                                square_size, 0, 1,
                                square_size
                            )
                        elif j + 1 == square_size:
                            grid_square.addWidget(
                                self.next_solution_btm,
                                square_size, 0, 1,
                                square_size
                            )
                        else:
                            grid_square.addWidget(
                                self.create_empty_widget(),
                                square_size, 0, 1,
                                square_size
                            )
                    h_box.addLayout(grid_square)
                v_box.addLayout(h_box)
            central_widget.setLayout(v_box)

        if self.flag:
            self.previous_solution_btm.setDisabled(True)
            check_end = peek(self.generator)
            if check_end is None:
                self.next_solution_btm.setDisabled(True)
            else:
                self.generator = check_end[1]
            self.flag = False

        self.update()

        self.setCentralWidget(central_widget)

        if return_flag:
            return central_widget

    def arrow_right(self):
        self.current_solutions_index += 1
        self.previous_solution_btm.setEnabled(True)

        if self.generator_is_end:
            if self.current_solutions_index + 1 == len(self.solutions_pool):
                self.next_solution_btm.setDisabled(True)
            self.grid_create(self.solutions_pool[self.current_solutions_index])
        else:
            if self.current_solutions_index == len(self.solutions_pool):
                next_solution = next(self.generator)
                self.solutions_pool.append(next_solution)
                self.grid_create(next_solution)

                check_end = peek(self.generator)
                if check_end is None:
                    self.next_solution_btm.setDisabled(True)
                    self.generator_is_end = True
                else:
                    self.generator = check_end[1]
            else:
                self.grid_create(
                    self.solutions_pool[self.current_solutions_index])

    def arrow_left(self):
        self.current_solutions_index -= 1
        if self.current_solutions_index == 0:
            self.previous_solution_btm.setDisabled(True)
        self.next_solution_btm.setEnabled(True)
        self.grid_create(self.solutions_pool[self.current_solutions_index])

    @staticmethod
    def simple_button_create(grid, puzzle, row=0, column=0, grid_row=0,
                             grid_column=0, x=1, y=2):
        button = QPushButton(str(puzzle[row][column]))
        button.setStatusTip(button.text())
        button.setMinimumSize(28, 28)
        button.setMaximumSize(1920, 1920)
        button.setFont(QFont('Times', 14))
        button.setFocusPolicy(Qt.NoFocus)
        grid.addWidget(button, grid_row, grid_column, x, y)

    @staticmethod
    def create_empty_widget():
        label = QLabel()
        label.setFixedHeight(24)
        label.setFocusPolicy(Qt.NoFocus)

        return label

    def create_empty_message(self):
        grid = QGridLayout()
        grid.setSpacing(0)
        label = QLabel("Don't decisions")
        label.setFont(QFont('Times', 18))
        label.setAlignment(Qt.AlignCenter)
        self.exit_button = QPushButton()
        self.exit_button.setStatusTip('Exit')
        self.exit_button.setIcon(self.style().standardIcon(
            QStyle.SP_DialogApplyButton))
        self.exit_button.clicked.connect(qApp.quit)
        grid.addWidget(label)
        grid.addWidget(self.exit_button)
        central_widget = QWidget()
        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)
        self.removeToolBar(self.toolbar)


def gui_create(solutions):
    application = QApplication(sys.argv)
    window = Window(solutions)
    sys.exit(application.exec_())
