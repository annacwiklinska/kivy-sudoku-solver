from kivy.graphics import Color, Line, Rectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class ResultsScreenChoose(Screen):
    def __init__(self, solved_sudoku, **kwargs):
        super(ResultsScreenChoose, self).__init__(**kwargs)
        self.solved_sudoku = solved_sudoku
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
        back_button.bind(on_press=self.go_menu)
        self.layout.add_widget(back_button)

        message_label = Label(text="Done", font_size=24, size_hint=(1, 0.1))
        self.layout.add_widget(message_label)

        float_layout = FloatLayout(size_hint=(1, 0.9))

        self.grid = GridLayout(cols=9, rows=9, size_hint=(None, None), spacing=0)

        cell_size = 50
        self.grid.size = (cell_size * 9, cell_size * 9)
        font_size = 30

        for row in self.solved_sudoku:
            for value in row:
                cell = Button(
                    text=str(value),
                    size_hint=(None, None),
                    size=(cell_size, cell_size),
                    font_size=font_size,
                    halign="center",
                    valign="middle",
                    disabled=True,
                    background_color=(0.77, 1, 0.67, 1),
                    background_disabled_normal="",
                    disabled_color=(0, 0, 0, 1),
                )
                cell.bind(size=cell.setter("text_size"))

                with cell.canvas.after:
                    Color(0, 0, 0, 1)
                    cell.rect = Line(
                        rectangle=(cell.x, cell.y, cell.width, cell.height), width=1
                    )
                cell.bind(
                    pos=self.update_textinput_border, size=self.update_textinput_border
                )

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

        self.layout.add_widget(float_layout)

        buttons_layout = BoxLayout(size_hint=(1, 0.1))

        back_button = Button(text="Go back", size_hint=(1, 1))
        back_button.bind(on_press=self.go_back)
        buttons_layout.add_widget(back_button)

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

    def go_back(self, instance):
        self.manager.current = "choose"
        self.manager.transition.direction = "left"
        self.manager.remove_widget(self)

    def go_menu(self, instance):
        self.manager.current = "menu"
        self.manager.transition.direction = "left"
        # delete this screen from screen manager
        self.manager.remove_widget(self)
