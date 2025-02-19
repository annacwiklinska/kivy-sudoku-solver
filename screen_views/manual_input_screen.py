from kivy.graphics import Color, Line, Rectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from screen_views.info_screen_manual import InfoScreenManual
from screen_views.results_screen_manual import ResultsScreenManual
from sudoku_solver import SudokuSolver


class ManualInputScreen(Screen):
    def __init__(self, **kwargs):
        super(ManualInputScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical")
        self.wrong_tiles = []
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

        self.grid = GridLayout(cols=9, rows=9, size_hint=(None, None), spacing=0)

        cell_size = 50
        self.grid.size = (cell_size * 9, cell_size * 9)
        font_size = 30

        self.inputs = [
            [
                TextInput(
                    multiline=False,
                    input_filter=self.only_one_digit,
                    halign="center",
                    size_hint=(None, None),
                    size=(cell_size, cell_size),
                    font_size=font_size,
                    padding=(0, (cell_size - font_size - 3) / 2),
                    cursor=(0, 0),
                )
                for _ in range(9)
            ]
            for _ in range(9)
        ]

        for row in self.inputs:
            for cell in row:
                with cell.canvas.before:
                    Color(0, 0, 0, 1)
                    cell.rect = Line(
                        rectangle=(cell.x, cell.y, cell.width, cell.height), width=0.1
                    )
                cell.bind(
                    pos=self.update_textinput_border, size=self.update_textinput_border
                )
                cell.bind(text=self.validate_digit)
                self.grid.add_widget(cell)

        with self.grid.canvas.after:
            Color(0, 0, 0, 1)
            self.grid.outer_border = Line(
                rectangle=(0, 0, cell_size * 9, cell_size * 9), width=2
            )

            self.grid.subgrid_borders = []
            for i in range(1, 3):
                self.grid.subgrid_borders.append(
                    Line(
                        points=[0, cell_size * 3 * i, cell_size * 9, cell_size * 3 * i],
                        width=2,
                    )
                )
                self.grid.subgrid_borders.append(
                    Line(
                        points=[cell_size * 3 * i, 0, cell_size * 3 * i, cell_size * 9],
                        width=2,
                    )
                )

        self.grid.bind(pos=self.update_grid_borders, size=self.update_grid_borders)

        anchor_layout = AnchorLayout(
            anchor_x="center", anchor_y="top", size_hint=(1, 1)
        )

        anchor_layout.add_widget(self.grid)

        float_layout.add_widget(anchor_layout)

        buttons_layout = BoxLayout(size_hint=(1, 0.1))

        solve_button = Button(text="Solve", size_hint=(0.5, 1))
        solve_button.bind(on_press=self.solve_sudoku)
        buttons_layout.add_widget(solve_button)

        clear_button = Button(text="Clear", size_hint=(0.5, 1))
        clear_button.bind(on_press=self.clear_inputs)
        buttons_layout.add_widget(clear_button)

        self.layout.add_widget(float_layout)
        self.layout.add_widget(buttons_layout)

    def update_textinput_border(self, instance, value):
        instance.rect.points = [
            instance.x,
            instance.y,
            instance.x + instance.width,
            instance.y,
            instance.x + instance.width,
            instance.y + instance.height,
            instance.x,
            instance.y + instance.height,
            instance.x,
            instance.y,
        ]

    def update_grid_borders(self, instance, value):
        cell_size = instance.width / 9

        instance.outer_border.rectangle = (
            instance.x,
            instance.y,
            instance.width,
            instance.height,
        )

        for i in range(1, 3):
            instance.subgrid_borders[2 * (i - 1)].points = [
                instance.x,
                instance.y + cell_size * 3 * i,
                instance.x + instance.width,
                instance.y + cell_size * 3 * i,
            ]
            instance.subgrid_borders[2 * (i - 1) + 1].points = [
                instance.x + cell_size * 3 * i,
                instance.y,
                instance.x + cell_size * 3 * i,
                instance.y + instance.height,
            ]

    def only_one_digit(self, substring, from_undo=False):
        return substring if substring in "123456789" else ""

    def validate_digit(self, instance, value):
        if len(value) > 1 or (value and value not in "123456789"):
            instance.text = ""
        if not value:
            instance.background_color = (1, 1, 1, 1)

    def update_wrong_tiles(self):
        for row_index, row in enumerate(self.inputs):
            for col_index, cell in enumerate(row):
                if (row_index, col_index) in self.wrong_tiles:
                    cell.background_color = (1, 0, 0, 0.75)

    def update_tiles(self):
        for row_index, row in enumerate(self.inputs):
            for col_index, cell in enumerate(row):
                if (row_index, col_index) in self.wrong_tiles:
                    cell.background_color = (1, 1, 1, 1)

    def solve_sudoku(self, instance):
        sudoku = [
            [int(cell.text) if cell.text else 0 for cell in row] for row in self.inputs
        ]

        solver = SudokuSolver(sudoku)

        if solver.is_initial_board_valid():
            if solver.solve_sudoku():
                solved_sudoku = solver.board
                results_screen = ResultsScreenManual(
                    solved_sudoku, name="results_manual"
                )
                self.manager.add_widget(results_screen)
                self.manager.current = "results_manual"
            else:
                info_screen = InfoScreenManual(
                    "No solution exists.", name="info_no_solution"
                )
                self.manager.add_widget(info_screen)
                self.manager.current = "info_no_solution"
        else:
            info_screen = InfoScreenManual(
                "The initial Sudoku board is invalid.", name="info_invalid_board"
            )
            self.manager.add_widget(info_screen)
            self.manager.current = "info_invalid_board"
            self.wrong_tiles = solver.invalid_tiles

    def clear_inputs(self, instance):
        for row in self.inputs:
            for cell in row:
                cell.text = ""

    def go_back(self, instance):
        self.manager.current = "menu"
        self.manager.transition.direction = "left"
