from kivy.graphics import Color, Rectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from sudoku_solver import SudokuSolver


class ManualInputScreen(Screen):
    def __init__(self, **kwargs):
        super(ManualInputScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical")
        self.add_widget(self.layout)
        self.gui()

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def gui(self):
        with self.canvas.before:
            Color(0.615686, 0.517647, 0.666667, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

        back_button = Button(text="Back to Main Screen", size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)

        float_layout = FloatLayout(size_hint=(1, 0.9))

        self.grid = GridLayout(cols=9, rows=9, size_hint=(None, None), spacing=1)

        cell_size = 100
        self.grid.size = (cell_size * 9, cell_size * 9)
        font_size = 50

        self.inputs = [
            [
                TextInput(
                    multiline=False,
                    input_filter="int",
                    halign="center",
                    size_hint=(None, None),
                    size=(cell_size, cell_size),
                    font_size=font_size,
                    padding=(0, (cell_size - font_size - 3) / 2),
                )
                for _ in range(9)
            ]
            for _ in range(9)
        ]

        for row in self.inputs:
            for cell in row:
                self.grid.add_widget(cell)

        anchor_layout = AnchorLayout(
            anchor_x="center", anchor_y="top", size_hint=(1, 1)
        )
        anchor_layout.add_widget(self.grid)

        float_layout.add_widget(anchor_layout)

        solve_button = Button(text="Solve", size_hint=(1, 0.1))
        solve_button.bind(on_press=self.solve_sudoku)
        self.layout.add_widget(float_layout)
        self.layout.add_widget(solve_button)

    def solve_sudoku(self, instance):
        sudoku = [
            [int(cell.text) if cell.text else 0 for cell in row] for row in self.inputs
        ]

        solver = SudokuSolver(sudoku)

        if solver.is_initial_board_valid():
            if solver.solve_sudoku():
                print("\nSolved Sudoku:")
                solver.print_board()

            else:
                print("No solution exists.")
        else:
            print("The initial Sudoku board is invalid.")

    def go_back(self, instance):
        self.manager.current = "menu"
        self.manager.transition.direction = "left"
