from kivy.graphics import Color, Rectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class ResultsScreenManual(Screen):
    def __init__(self, solved_sudoku, **kwargs):
        super(ResultsScreenManual, self).__init__(**kwargs)
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

        message_label = Label(text="Done!", font_size=24, size_hint=(1, 0.1))
        self.layout.add_widget(message_label)

        float_layout = FloatLayout(size_hint=(1, 0.9))

        self.grid = GridLayout(cols=9, rows=9, size_hint=(None, None), spacing=1)

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
                self.grid.add_widget(cell)

        anchor_layout = AnchorLayout(
            anchor_x="center", anchor_y="top", size_hint=(1, 1)
        )
        anchor_layout.add_widget(self.grid)

        float_layout.add_widget(anchor_layout)

        self.layout.add_widget(float_layout)

        buttons_layout = BoxLayout(size_hint=(1, 0.1))

        back_button = Button(text="Go back", size_hint=(0.5, 1))
        back_button.bind(on_press=self.go_back)
        buttons_layout.add_widget(back_button)

        new_sudoku_button = Button(text="New Sudoku", size_hint=(0.5, 1))
        new_sudoku_button.bind(on_press=self.new_sudoku)
        buttons_layout.add_widget(new_sudoku_button)

        self.layout.add_widget(buttons_layout)

    def go_back(self, instance):
        self.manager.current = "manual"
        self.manager.transition.direction = "left"
        self.manager.remove_widget(self)

    def new_sudoku(self, instance):
        manual_screen = self.manager.get_screen("manual")
        manual_screen.clear_inputs(instance)
        self.manager.current = "manual"
        self.manager.transition.direction = "left"
        self.manager.remove_widget(self)
        
    def go_menu(self, instance):
        self.manager.current = "menu"
        self.manager.transition.direction = "left"
        self.manager.remove_widget(self)
