from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from plyer import camera, filechooser

from sudoku_solver import SudokuSolver

# Load the .kv file
Builder.load_file("menu.kv")


class MenuScreen(Screen):
    def go_to_manual_input(self):
        self.manager.current = "manual"

    def go_to_camera(self):
        self.manager.current = "camera"

    def go_to_choosing_photo(self):
        self.manager.current = "choose"


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


class TakePhotoScreen(Screen):
    def __init__(self, **kwargs):
        super(TakePhotoScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")

        take_photo_button = Button(text="Zrób zdjęcie")
        take_photo_button.bind(on_press=self.take_photo)
        layout.add_widget(take_photo_button)

        self.add_widget(layout)

    def take_photo(self, instance):
        camera.take_picture(on_complete=self.picture_taken, filename="sudoku.jpg")

    def picture_taken(self, path):
        if path:
            # preprocess the image
            preprocessed = self.preprocess_image(path)
            # Here you would process the image with the model
            self.recognize_digits(preprocessed)

    def preprocess_image(self, image):
        # Here you would preprocess the image before digit recognition
        pass

    def recognize_digits(self, image):
        # Here you would recognize the digits in the image
        pass


class ChoosePhotoScreen(Screen):
    def __init__(self, **kwargs):
        super(ChoosePhotoScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")

        choose_photo_button = Button(text="Wybierz zdjęcie z galerii")
        choose_photo_button.bind(on_press=self.choose_photo)
        layout.add_widget(choose_photo_button)

        self.add_widget(layout)

    def choose_photo(self, instance):
        filechooser.open_file(on_selection=self.file_chosen)

    def file_chosen(self, selection):
        if selection:
            # preprocess the image
            preprocessed = self.preprocess_image(selection[0])
            # Here you would process the image with the model
            self.recognize_digits(preprocessed)

    def preprocess_image(self, image):
        # Here you would preprocess the image before digit recognition
        pass

    def recognize_digits(self, image):
        # Here you would recognize the digits in the image
        pass


# class SudokuSolution(Screen):
#     def __init__(self, **kwargs):
#         super(SudokuSolution, self).__init__(**kwargs)
#         layout = BoxLayout(orientation="vertical")

#         self.add_widget(layout)

#     def show_solution(self, instance):


class SudokuApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(ManualInputScreen(name="manual"))
        sm.add_widget(TakePhotoScreen(name="camera"))
        sm.add_widget(ChoosePhotoScreen(name="choose"))
        return sm


if __name__ == "__main__":
    SudokuApp().run()
