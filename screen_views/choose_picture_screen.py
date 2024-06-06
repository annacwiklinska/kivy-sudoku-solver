import cv2
import joblib
import numpy as np
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from image_preprocessor import ImagePreprocessor
from model.model import DigitRecognizeModel  # noqa
from screen_views.info_screen_choose import InfoScreenChoose
from screen_views.results_screen_choose import ResultsScreenChoose
from sudoku_solver import SudokuSolver


class FileChooserPopup(Popup):
    def __init__(self, callback, **kwargs):
        super(FileChooserPopup, self).__init__(**kwargs)
        self.callback = callback

        file_chooser = FileChooserListView()
        file_chooser.bind(on_submit=self.on_submit)
        file_chooser.bind(on_canceled=self.dismiss)
        self.content = file_chooser

    def on_submit(self, instance, selected_file, touch):
        self.callback(selected_file)
        self.dismiss()


class ChoosePictureScreen(Screen):
    def __init__(self, **kwargs):
        super(ChoosePictureScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation="vertical")

        with layout.canvas.before:
            Color(0.615686, 0.517647, 0.666667, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)

        layout.bind(size=self._update_rect, pos=self._update_rect)

        back_button = Button(text="Back to Main Screen", size_hint=(1, 0.15))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        tips_label = Label(
            text="[b]Tips for choosing a picture:[/b]",
            size_hint=(1, 0.15),
            markup=True,
            font_size=30,
        )
        layout.add_widget(tips_label)

        tips_widget = BoxLayout(orientation="vertical")

        labels = [
            "1. Screenshots and clear images work best for digit recognition.",
            "2. Make sure the picture is not warped or distorted.",
            "3. Ensure good lighting to avoid shadows.",
            "4. Avoid blurry images by holding the camera steady.",
            "5. Crop the image to include only the relevant area.",
            "6. Use a high-resolution image for better accuracy.",
            "7. Check the image orientation before uploading.",
        ]

        for text in labels:
            label = Label(
                text=text,
                height=50,
                font_size=20,
            )
            tips_widget.add_widget(label)

        layout.add_widget(tips_widget)

        choose_photo_button = Button(
            text="Choose picture from gallery", size_hint=(1, 0.15)
        )
        choose_photo_button.bind(on_press=self.choose_photo)
        layout.add_widget(choose_photo_button)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def choose_photo(self, instance):
        file_chooser_popup = FileChooserPopup(
            callback=self.file_chosen, title="Choose a picture"
        )
        file_chooser_popup.open()

    def file_chosen(self, selection):
        if selection:
            print(selection)
            digits = self.image_prep(selection[0])
            if digits is not None:
                sudoku = self.image_recognition(digits)
                self.solve_sudoku(sudoku)

    def image_prep(self, image_path):
        preprocessor = ImagePreprocessor(image_path)
        cells = preprocessor.process_image()
        if cells is None:
            info_screen = InfoScreenChoose(
                "No Sudoku board found in the image.", name="info_no_board"
            )
            self.manager.add_widget(info_screen)
            self.manager.current = "info_no_board"
        else:
            return cells

    def image_recognition(self, cells):
        digits = []

        model = joblib.load("model.pkl")

        for cell in cells:
            if cell is False:
                digits.append(0)
            else:
                cell = cv2.resize(cell, (28, 28))
                cell = cv2.dilate(cell, (3, 3))
                cell = cell.reshape(1, -1)
                cell = cell / 255.0
                digit = model.predict(cell)
                digits.append(digit[0])

        digits = np.array(digits).reshape(9, 9)
        digits = digits.tolist()
        print(digits)
        return digits

    def solve_sudoku(self, sudoku):
        solver = SudokuSolver(sudoku)

        if solver.is_initial_board_valid():
            if solver.solve_sudoku():
                solved_sudoku = solver.board
                print(solved_sudoku)
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

    def go_back(self, instance):
        self.manager.current = "menu"
        self.manager.transition.direction = "left"

