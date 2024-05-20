from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from plyer import camera, filechooser

from sudoku_solver import SudokuSolver


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")

        manual_button = Button(text="Wprowadź Sudoku ręcznie")
        manual_button.bind(on_press=self.go_to_manual_input)
        layout.add_widget(manual_button)

        photo_button = Button(text="Ze zdjęcia")
        photo_button.bind(on_press=self.go_to_photo_input)
        layout.add_widget(photo_button)

        self.add_widget(layout)

    def go_to_manual_input(self, instance):
        self.manager.current = "manual"

    def go_to_photo_input(self, instance):
        self.manager.current = "photo"


class ManualInputScreen(Screen):
    def __init__(self, **kwargs):
        super(ManualInputScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")

        # Create a FloatLayout to manage the square grid layout
        float_layout = FloatLayout(size_hint=(1, 0.9))

        self.grid = GridLayout(cols=9, rows=9, size_hint=(None, None), spacing=1)

        cell_size = 40
        self.grid.size = (cell_size * 9, cell_size * 9)
        font_size = 25

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

        solve_button = Button(text="Rozwiąż", size_hint=(1, 0.1))
        solve_button.bind(on_press=self.solve_sudoku)
        layout.add_widget(float_layout)
        layout.add_widget(solve_button)

        self.add_widget(layout)

    def solve_sudoku(self, instance):
        # Get the values from the input fields
        sudoku = [
            [int(cell.text) if cell.text else 0 for cell in row] for row in self.inputs
        ]

        solver = SudokuSolver()
        solver.grid = sudoku

        if solver.solve_sudoku():
            solver.print_grid()
        else:
            print("No solution exists")


class PhotoInputScreen(Screen):
    def __init__(self, **kwargs):
        super(PhotoInputScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")

        take_photo_button = Button(text="Zrób zdjęcie")
        take_photo_button.bind(on_press=self.take_photo)
        layout.add_widget(take_photo_button)

        choose_photo_button = Button(text="Wybierz zdjęcie z galerii")
        choose_photo_button.bind(on_press=self.choose_photo)
        layout.add_widget(choose_photo_button)

        self.add_widget(layout)

    def take_photo(self, instance):
        camera.take_picture(on_complete=self.picture_taken, filename="sudoku.jpg")

    def choose_photo(self, instance):
        filechooser.open_file(on_selection=self.file_chosen)

    def picture_taken(self, path):
        if path:
            # Here you would process the taken picture
            pass

    def file_chosen(self, selection):
        if selection:
            # Here you would process the chosen file
            pass


class SudokuApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(ManualInputScreen(name="manual"))
        sm.add_widget(PhotoInputScreen(name="photo"))
        return sm


if __name__ == "__main__":
    SudokuApp().run()
