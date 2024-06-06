from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from model.model import DigitRecognizeModel  # noqa
from screen_views.choose_picture_screen import ChoosePictureScreen
from screen_views.manual_input_screen import ManualInputScreen
from screen_views.menu_screen import MenuScreen


class SudokuApp(App):
    def build(self):
        Window.size = (600, 800)
        Window.minimum_width = 600
        Window.minimum_height = 800

        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(ManualInputScreen(name="manual"))
        sm.add_widget(ChoosePictureScreen(name="choose"))
        return sm


if __name__ == "__main__":
    SudokuApp().run()
