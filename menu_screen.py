from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout


class MenuScreen(RelativeLayout):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.gui()

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def gui(self):
        # Window.size = (339, 600)
        self.w1 = self
        with self.w1.canvas.before:
            Color(0.615686, 0.517647, 0.666667, 1)
            self.rect = Rectangle(size=self.w1.size, pos=self.w1.pos)
        self.w1.bind(pos=self.update_rect, size=self.update_rect)
        self.button1 = Button(
            text="Insert sudoku manually",
            pos_hint={"x": 0.117994, "y": 0.38},
            size_hint=(0.766962, 0.0866667),
            font_family="Lucida Sans",
            font_size="14",
            background_color=[0.192157, 0.192157, 0.254902, 1],
            on_press=self.go_to_manual_input,
        )
        self.w1.add_widget(self.button1)
        self.button2 = Button(
            text="Take picture",
            pos_hint={"x": 0.117994, "y": 0.246667},
            size_hint=(0.766962, 0.0866667),
            font_family="Lucida Sans",
            font_size="14",
            background_color=[0.192157, 0.192157, 0.254902, 1],
            on_press=self.go_to_camera,
        )
        self.w1.add_widget(self.button2)
        self.button3 = Button(
            text="Choose from gallery",
            pos_hint={"x": 0.117994, "y": 0.113333},
            size_hint=(0.766962, 0.0866667),
            font_family="Lucida Sans",
            font_size="14",
            background_color=[0.192157, 0.192157, 0.254902, 1],
            on_press=self.go_to_choosing_photo,
        )
        self.w1.add_widget(self.button3)
        self.image1 = Image(
            source="public/logo.png",
            allow_stretch=True,
            pos_hint={"x": 0.0589971, "y": 0.451667},
            size_hint=(0.882006, 0.498333),
        )
        self.w1.add_widget(self.image1)
        return self.w1

    def go_to_manual_input(self, instance):
        self.manager.current = "manual"

    def go_to_camera(self, instance):
        self.manager.current = "camera"

    def go_to_choosing_photo(self, instance):
        self.manager.current = "choose"


class MainApp(App):
    def build(self):
        self.root = MenuScreen()
        return self.root


if __name__ == "__main__":
    MainApp().run()
