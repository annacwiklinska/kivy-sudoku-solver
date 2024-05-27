from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from screen_views.choose_picture_screen import ChoosePictureScreen
from screen_views.manual_input_screen import ManualInputScreen
from screen_views.menu_screen import MenuScreen


class SudokuApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(ManualInputScreen(name="manual"))
        sm.add_widget(ChoosePictureScreen(name="choose"))
        return sm


if __name__ == "__main__":
    SudokuApp().run()
