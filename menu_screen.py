from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_file("menu.kv")


class MenuScreen(Screen):
    def go_to_manual_input(self):
        self.manager.current = "manual"

    def go_to_camera(self):
        self.manager.current = "camera"

    def go_to_choosing_photo(self):
        self.manager.current = "choose"
