class TimeVariable(object):
    def __init__(self, app, value, default, created, expiry) -> None:
        self.app = app
        self.value = value
        self.default = default
        self.created = created
        self.expiry = expiry

    def expired(self, current) -> bool:
        return True if current > self.created + self.expiry else False

    def get_value(self) -> str:
        return self.value if not self.expired(self.app.turn) else self.default

    def set_value(self, new_value, new_defailt, current, expiry=999):
        self.value = new_value
        self.default = new_defailt
        self.created = current
        self.expiry = expiry

    def __repr__(self) -> str:
        return self.get_value()

    def __str__(self) -> str:
        return self.get_value()
