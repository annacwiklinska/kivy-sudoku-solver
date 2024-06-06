from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class InfoScreenManual(Screen):
    def __init__(self, message, **kwargs):
        super(InfoScreenManual, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical")

        with self.canvas.before:
            Color(0.615686, 0.517647, 0.666667, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

        message_label = Label(text=message, size_hint=(1, 0.8))
        ok_button = Button(text="Go back to manual input", size_hint=(1, 0.1))
        ok_button.bind(on_press=self.dismiss)

        self.layout.add_widget(message_label)
        self.layout.add_widget(ok_button)
        self.add_widget(self.layout)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def dismiss(self, instance):
        self.manager.current = "manual"
