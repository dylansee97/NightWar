from tabulate import tabulate

from human import *
from skill import *


class Team:
    def __init__(self, app, name, members):
        self.app = app
        self.name = name
        self.members = members

        for member in members:
            member.team = self

    def team_is_alive(self):
        return any([human.is_alive() for human in self.members])

    def get_speed(self):
        return sum([human.speed for human in self.members])
