from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from plyer import filechooser


class ChoosePictureScreen(Screen):
    def __init__(self, **kwargs):
        super(ChoosePictureScreen, self).__init__(**kwargs)
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
