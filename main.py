from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

from building import Floor
from grid_square import GridSquare, GridSquareSelection


class NightWar(App):
    def __init__(self, **kwargs):
        super().__init__()
        self.width = kwargs["width"]
        self.height = kwargs["height"]
        self.sm = ScreenManager()
        Window.size = (800, 600)  # width, height

        self.turn = 1

        self.team_1_grid = [
            [None for _ in range(self.width)] for _ in range(self.height)
        ]
        self.team_2_grid = [
            [None for _ in range(self.width)] for _ in range(self.height)
        ]

    def make_main_screen_widget(self):
        main_screen_widget = GridLayout(cols=3)
        board = GridLayout(
            cols=self.width,
            pos=(0, 0),
            size=(500, 500),
        )

        # team 2 on top
        for i in range(self.height):
            for j in range(self.width):
                obj = (
                    self.team_2_grid[i][j].obj
                    if isinstance(self.team_2_grid[i][j], Button)
                    else Floor(self, "Floor")
                )
                board.add_widget(GridSquare(location=(i, j), obj=obj, team=2))

        # team 1 on btm
        for i in range(self.height):
            for j in range(self.width):
                obj = (
                    self.team_1_grid[i][j].obj
                    if isinstance(self.team_1_grid[i][j], GridSquareSelection)
                    else Floor(self, "Floor")
                )
                board.add_widget(
                    GridSquare(location=(i + self.height, j), obj=obj, team=1)
                )

        main_screen_widget.add_widget(Button(text="Team 1 stats", size_hint_x=0.2))
        main_screen_widget.add_widget(board)
        main_screen_widget.add_widget(Button(text="Team 2 stats", size_hint_x=0.2))

        return main_screen_widget

    def make_team_1_selection_widget(self):
        top_board = GridLayout(cols=1)
        board = GridLayout(
            cols=self.width,
            pos=(0, 0),
            size=(500, 500),
        )
        for i in range(self.height):
            for j in range(self.width):
                board.add_widget(
                    GridSquareSelection(
                        app=self, location=(i + self.height, j), obj=None, team=1
                    )
                )

        top_board.add_widget(Label(text="Team 1 selection", size_hint_y=0.1))
        top_board.add_widget(board)
        top_board.add_widget(
            Button(
                text="Done",
                size_hint_y=0.1,
                on_press=lambda _: self.sm.switch_to(self.team_2_selection_screen),
            )
        )
        return top_board

    def make_team_2_selection_widget(self):
        top_board = GridLayout(cols=1)
        board = GridLayout(
            cols=self.width,
            pos=(0, 0),
            size=(500, 500),
        )
        for i in range(self.height):
            for j in range(self.width):
                board.add_widget(
                    GridSquareSelection(app=self, location=(i, j), obj=None, team=2)
                )

        top_board.add_widget(Label(text="Team 2 selection", size_hint_y=0.1))
        top_board.add_widget(board)
        top_board.add_widget(
            Button(
                text="Done",
                size_hint_y=0.1,
                on_press=lambda _: self.build_main_screen(),
            )
        )
        return top_board

    def build_main_screen(self):
        self.main_screen = Screen(name="main_screen")
        main_screen_widget = self.make_main_screen_widget()
        self.main_screen.add_widget(main_screen_widget)
        self.sm.add_widget(self.main_screen)

        self.sm.switch_to(self.main_screen)

    def build(self):

        # initialising the screens
        self.team_1_selection_screen = Screen(name="team_1_selection")
        self.team_2_selection_screen = Screen(name="team_2_selection")

        # making the widgets to put inside the screens
        team_1_selection_widget = self.make_team_1_selection_widget()
        team_2_selection_widget = self.make_team_2_selection_widget()

        # adding the widgets to each screen
        self.team_1_selection_screen.add_widget(team_1_selection_widget)
        self.team_2_selection_screen.add_widget(team_2_selection_widget)

        # adding the screens to screen manager
        self.sm.add_widget(self.team_1_selection_screen)
        self.sm.add_widget(self.team_2_selection_screen)

        return self.sm


if __name__ == "__main__":
    app = NightWar(width=2, height=2)
    app.run()
