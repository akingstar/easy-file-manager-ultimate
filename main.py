import os
from kivy.app import App
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

Window.clearcolor = (0.055, 0.065, 0.09, 1)

class EasyFileManager(App):
    def build(self):
        self.current_path = "/storage/emulated/0"
        self.root_layout = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(8)
        )

        header = BoxLayout(size_hint_y=None, height=dp(55))
        header.add_widget(Label(
            text="[b]EASY FILE MANAGER[/b]",
            markup=True,
            font_size="21sp",
            color=(0.3, 0.75, 1, 1)
        ))
        self.root_layout.add_widget(header)

        self.path_input = TextInput(
            text=self.current_path,
            multiline=False,
            size_hint_y=None,
            height=dp(45),
            font_size="14sp"
        )
        self.path_input.bind(on_text_validate=self.open_path)
        self.root_layout.add_widget(self.path_input)

        toolbar = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(5))
        for title, action in [
            ("BACK", self.go_back),
            ("HOME", self.go_home),
            ("REFRESH", self.refresh)
        ]:
            btn = Button(text=title, on_release=action)
            toolbar.add_widget(btn)
        self.root_layout.add_widget(toolbar)

        self.info = Label(
            text="Loading files...",
            size_hint_y=None,
            height=dp(28),
            halign="left"
        )
        self.root_layout.add_widget(self.info)

        self.scroll = ScrollView()
        self.file_list = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(4)
        )
        self.file_list.bind(minimum_height=self.file_list.setter("height"))
        self.scroll.add_widget(self.file_list)
        self.root_layout.add_widget(self.scroll)

        self.refresh()
        return self.root_layout

    def refresh(self, *args):
        self.file_list.clear_widgets()
        path = self.current_path
        self.path_input.text = path

        try:
            entries = sorted(
                os.scandir(path),
                key=lambda item: (not item.is_dir(), item.name.lower())
            )
            count = 0

            for entry in entries:
                name = ("📁 " if entry.is_dir() else "📄 ") + entry.name
                btn = Button(
                    text=name,
                    size_hint_y=None,
                    height=dp(48),
                    halign="left",
                    background_normal="",
                    background_color=(0.12, 0.15, 0.21, 1)
                )
                btn.bind(on_release=lambda b, e=entry: self.open_entry(e))
                self.file_list.add_widget(btn)
                count += 1

            self.info.text = f"{count} items"
        except Exception as error:
            self.info.text = f"Access error: {error}"

    def open_entry(self, entry):
        if entry.is_dir():
            self.current_path = entry.path
            self.refresh()

    def open_path(self, *args):
        path = os.path.abspath(os.path.expanduser(self.path_input.text))
        if os.path.isdir(path):
            self.current_path = path
            self.refresh()
        else:
            self.info.text = "Folder not found"

    def go_back(self, *args):
        parent = os.path.dirname(self.current_path.rstrip("/"))
        if parent:
            self.current_path = parent
            self.refresh()

    def go_home(self, *args):
        self.current_path = "/storage/emulated/0"
        self.refresh()

if __name__ == "__main__":
    EasyFileManager().run()
