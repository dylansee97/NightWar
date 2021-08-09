from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

from app import a, b, c, d

DEFAULT_COUNT = 3
HEROES = {"a": a, "b": b, "c": c, "d": d}
HEROES_COUNT = {k: DEFAULT_COUNT for k in HEROES}

# colours specified in (R,G,B,A)
LIGHT_BLUE = (1, 2, 3, 1)
LIGHT_RED = (10, 2, 1, 1)
TEAM_COLOUR = {1: LIGHT_BLUE, 2: LIGHT_RED}


class GridSquare(Button):
    def __init__(self, **kwargs):
        super().__init__()

        self.obj = kwargs["obj"]
        self.background_color = TEAM_COLOUR[kwargs["team"]]
        self.text = repr(self.obj) if self.obj else ""
        self.location = kwargs["location"]
        self.row, self.col = kwargs["location"]

    def refresh_text(self, new_text):
        self.text = new_text

    def on_press(self):
        pass


class GridSquareSelection(Button):
    def __init__(self, **kwargs):
        super().__init__()
        self.app = kwargs["app"]
        self.team_grid = (
            self.app.team_1_grid if kwargs["team"] == 1 else self.app.team_2_grid
        )
        self.obj = kwargs["obj"]
        self.background_color = TEAM_COLOUR[kwargs["team"]]
        self.text = self.obj.get_selection_display() if self.obj else ""
        self.location = kwargs["location"]
        self.row, self.col = kwargs["location"]

    def refresh_text(self, new_text):
        self.text = new_text

    def on_press(self):
        def popup_btn_on_press(popup, selection):
            def callback(button_object):
                self.obj = HEROES[selection]
                HEROES_COUNT[selection] -= 1
                self.refresh_text(self.obj.name)
                self.team_grid[self.row % self.app.height][self.col] = self
                popup.dismiss()

            return callback

        popup_content = GridLayout(cols=1)
        popup = Popup(
            title="Choose hero",
            content=popup_content,
            size_hint=(None, None),
            size=(400, 400),
        )
        for hero_name in HEROES:
            if HEROES_COUNT[hero_name] > 0:
                popup_content.add_widget(
                    Button(
                        text=hero_name, on_press=popup_btn_on_press(popup, hero_name)
                    )
                )
        popup.open()
