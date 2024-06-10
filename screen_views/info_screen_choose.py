from kivy.graphics import Color, Line, Rectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from screen_views.results_screen_choose import ResultsScreenChoose
from sudoku_solver import SudokuSolver


class InfoScreenChoose(Screen):
    def __init__(self, message, board=None, wrong=None, **kwargs):
        super(InfoScreenChoose, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical")
        self.wrong_tiles = wrong if wrong else []

        with self.canvas.before:
            Color(0.615686, 0.517647, 0.666667, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

        message_label = Label(text=message, size_hint=(1, 0.1))
        self.layout.add_widget(message_label)

        content_layout = BoxLayout(orientation="vertical")

        if board:
            recognized_label = Label(text="Recognized Sudoku grid:", size_hint=(1, 0.1))
            content_layout.add_widget(recognized_label)

            edit_label = Label(
                text="You can edit the board below or import a better picture",
                size_hint=(1, 0.1),
            )
            content_layout.add_widget(edit_label)

            self.grid_layout = GridLayout(
                cols=9,
                rows=9,
                size_hint=(None, None),
                size=(450, 450),
                spacing=0,
            )
            self.grid_layout.bind(minimum_size=self.grid_layout.setter("size"))

            cell_size = 50
            font_size = 30

            self.inputs = []

            for r_id, row in enumerate(board):
                row_inputs = []
                for c_id, number in enumerate(row):
                    if (r_id, c_id) in self.wrong_tiles:
                        text_input = TextInput(
                            text=str(number) if number != 0 else "",
                            size_hint=(None, None),
                            size=(cell_size, cell_size),
                            multiline=False,
                            input_filter=self.only_one_digit,
                            halign="center",
                            font_size=font_size,
                            padding=(0, (cell_size - font_size - 3) / 2),
                            background_color=(1, 0, 0, 0.75),
                        )
                    else:
                        text_input = TextInput(
                            text=str(number) if number != 0 else "",
                            size_hint=(None, None),
                            size=(cell_size, cell_size),
                            multiline=False,
                            input_filter=self.only_one_digit,
                            halign="center",
                            font_size=font_size,
                            padding=(0, (cell_size - font_size - 3) / 2),
                        )
                    text_input.bind(text=self.validate_digit)

                    with text_input.canvas.before:
                        Color(0, 0, 0, 1)
                        text_input.rect = Line(
                            rectangle=(
                                text_input.x,
                                text_input.y,
                                text_input.width,
                                text_input.height,
                            ),
                            width=0.1,
                        )
                    text_input.bind(
                        pos=self.update_textinput_border,
                        size=self.update_textinput_border,
                    )

                    self.grid_layout.add_widget(text_input)
                    row_inputs.append(text_input)
                self.inputs.append(row_inputs)

            with self.grid_layout.canvas.after:
                Color(0, 0, 0, 1)
                self.grid_layout.outer_border = Line(
                    rectangle=(0, 0, cell_size * 9, cell_size * 9), width=2
                )

                self.grid_layout.subgrid_borders = []
                for i in range(1, 3):
                    self.grid_layout.subgrid_borders.append(
                        Line(
                            points=[
                                0,
                                cell_size * 3 * i,
                                cell_size * 9,
                                cell_size * 3 * i,
                            ],
                            width=2,
                        )
                    )
                    self.grid_layout.subgrid_borders.append(
                        Line(
                            points=[
                                cell_size * 3 * i,
                                0,
                                cell_size * 3 * i,
                                cell_size * 9,
                            ],
                            width=2,
                        )
                    )

            self.grid_layout.bind(
                pos=self.update_grid_borders, size=self.update_grid_borders
            )

            anchor_layout = AnchorLayout(anchor_x="center", anchor_y="center")
            anchor_layout.add_widget(self.grid_layout)
            content_layout.add_widget(anchor_layout)

        buttons_layout = BoxLayout(size_hint=(1, None), height=50)

        ok_button = Button(text="Go back")
        ok_button.bind(on_press=self.dismiss)
        buttons_layout.add_widget(ok_button)

        if board:
            solve_button = Button(text="Solve")
            solve_button.bind(on_press=self.solve_sudoku)
            buttons_layout.add_widget(solve_button)

        content_layout.add_widget(buttons_layout)
        self.layout.add_widget(content_layout)
        self.add_widget(self.layout)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

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
            # Update horizontal subgrid borders
            instance.subgrid_borders[2 * (i - 1)].points = [
                instance.x,
                instance.y + cell_size * 3 * i,
                instance.x + instance.width,
                instance.y + cell_size * 3 * i,
            ]
            # Update vertical subgrid borders
            instance.subgrid_borders[2 * (i - 1) + 1].points = [
                instance.x + cell_size * 3 * i,
                instance.y,
                instance.x + cell_size * 3 * i,
                instance.y + instance.height,
            ]

    def dismiss(self, instance):
        self.manager.current = "choose"
        self.manager.remove_widget(self)

    def only_one_digit(self, substring, from_undo=False):
        return substring if substring in "123456789" else ""

    def validate_digit(self, instance, value):
        if len(value) > 1 or (value and value not in "123456789"):
            instance.text = ""
        if not value:
            instance.background_color = (1, 1, 1, 1)

    def solve_sudoku(self, instance):
        sudoku = [
            [int(cell.text) if cell.text else 0 for cell in row] for row in self.inputs
        ]

        solver = SudokuSolver(sudoku)

        if solver.is_initial_board_valid():
            if solver.solve_sudoku():
                solved_sudoku = solver.board
                results_screen = ResultsScreenChoose(
                    solved_sudoku, name="results_choose"
                )
                self.manager.add_widget(results_screen)
                self.manager.current = "results_choose"
            else:
                info_screen = InfoScreenChoose(
                    "No solution exists.", name="info_no_solution"
                )
                self.manager.add_widget(info_screen)
                self.manager.current = "info_no_solution"
        else:
            info_screen = InfoScreenChoose(
                "The initial Sudoku board is invalid.",
                name="info_invalid_board",
                board=sudoku,
            )
            self.manager.add_widget(info_screen)
            self.manager.current = "info_invalid_board"
