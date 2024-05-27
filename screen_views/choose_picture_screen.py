from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from plyer import filechooser


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
            text="[b]Tips for choosing a picture:[/b]", size_hint=(1, 0.2), markup=True
        )
        layout.add_widget(tips_label)

        tips_widget = BoxLayout(orientation="vertical")
        tips_text1 = Label(text="1. Screenshots work best for digit recognition.")
        tips_widget.add_widget(tips_text1)

        tips_text2 = Label(text="2. Make sure the picture is not warped or distorted.")
        tips_widget.add_widget(tips_text2)

        tips_text3 = Label(text="3. Ensure good lighting to avoid shadows.")
        tips_widget.add_widget(tips_text3)

        tips_text4 = Label(text="4. Avoid blurry images by holding the camera steady.")
        tips_widget.add_widget(tips_text4)

        tips_text5 = Label(text="5. Crop the image to include only the relevant area.")
        tips_widget.add_widget(tips_text5)

        tips_text6 = Label(text="6. Use a high-resolution image for better accuracy.")
        tips_widget.add_widget(tips_text6)

        tips_text7 = Label(text="7. Check the image orientation before uploading.")
        tips_widget.add_widget(tips_text7)

        layout.add_widget(tips_widget)

        choose_photo_button = Button(
            text="Wybierz zdjęcie z galerii", size_hint=(1, 0.15)
        )
        choose_photo_button.bind(on_press=self.choose_photo)
        layout.add_widget(choose_photo_button)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def choose_photo(self, instance):
        filechooser.open_file(
            on_selection=self.file_chosen, on_canceled=self.file_not_chosen
        )

    def file_not_chosen(self, instance):
        print("File not chosen")
        self.manager.current = "menu"

    def file_chosen(self, selection):
        if selection:
            print(selection)
            preprocessed = self.preprocess_image(selection[0])
            self.recognize_digits(preprocessed)

    def preprocess_image(self, image):
        print("im preprocessing")

    def recognize_digits(self, image):
        print("im recognizing")

    def go_back(self, instance):
        self.manager.current = "menu"
        self.manager.transition.direction = "left"
