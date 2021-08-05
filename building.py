from time_variable import TimeVariable


class Building:
    def __init__(self, app, name, visible: bool = True) -> None:
        self.name = name
        self.app = app
        self.visible = TimeVariable(
            app=self.app, value=False, default=True, created=1, expiry=999
        )

    def __repr__(self) -> str:
        return self.name if self.visible.get_value() else ""
