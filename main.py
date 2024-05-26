from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from plyer import camera, filechooser

from manual_input_screen import ManualInputScreen
from menu_screen import MenuScreen

# class ManualResultScreen(Screen):
#     def __init__(self, **kwargs):
#         super(ManualResultScreen, self).__init__(**kwargs)
#         self.layout = BoxLayout(orientation="vertical")
#         self.add_widget(self.layout)
#         self.display_result()

#     def display_result(self):
#         # Assuming you have a solver instance available with the solved Sudoku puzzle
#         pass

#         # Create a label to display the solved Sudoku puzzle
#         result_label = Label(text="Solved Sudoku:", font_size=24, size_hint=(1, 0.9))
#         self.layout.add_widget(result_label)

#         for row in solved_sudoku:
#             row_text = " ".join(map(str, row))
#             row_label = Label(
#                 text=row_text, font_size=18, size_hint=(1, None), height=40
#             )
#             self.layout.add_widget(row_label)

#         # Add a button to go back to the manual input screen
#         back_button = Button(text="Back to Input Screen", size_hint=(1, 0.1))
#         back_button.bind(on_press=self.go_back)
#         self.layout.add_widget(back_button)

#     def go_back(self, instance):
#         self.manager.current = "manual"
#         self.manager.transition.direction = "left"


class TakePhotoScreen(Screen):
    def __init__(self, **kwargs):
        super(TakePhotoScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")

        take_photo_button = Button(text="Zrób zdjęcie", size_hint=(1, 0.1))
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
