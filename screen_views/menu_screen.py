from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0.615686, 0.517647, 0.666667, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation="vertical", spacing=10, padding=50)

        image = Image(
            source="public/logo.png",
            allow_stretch=True,
            size_hint=(0.882006, 0.498333),
            pos_hint={"center_x": 0.5},
        )
        layout.add_widget(image)

        button_manual = Button(
            text="Insert sudoku manually",
            size_hint=(0.766962, 0.0866667),
            font_size=30,
            background_normal="",
            background_color=(0.192157, 0.192157, 0.254902, 1),
            pos_hint={"center_x": 0.5},
        )
        button_manual.bind(on_press=self.go_to_manual_input)
        layout.add_widget(button_manual)

        button_gallery = Button(
            text="Choose from gallery",
            size_hint=(0.766962, 0.0866667),
            font_size=30,
            background_normal="",
            background_color=(0.192157, 0.192157, 0.254902, 1),
            pos_hint={"center_x": 0.5},
        )
        button_gallery.bind(on_press=self.go_to_choosing_photo)
        layout.add_widget(button_gallery)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def go_to_manual_input(self, instance):
        self.manager.current = "manual"

    def go_to_choosing_photo(self, instance):
        self.manager.current = "choose"
