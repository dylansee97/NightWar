from tabulate import tabulate

from building import *
from human import *
from skill import *
from team import *


class Game:
    def __init__(self, width, height) -> None:
        self.width, self.height = width, height
        self.team1 = None
        self.team2 = None
        self.grid1 = [
            [Building(self,"Floor", visible=False) for _ in range(width)]
            for _ in range(height)
        ]
        self.grid2 = [
            [Building(self,"Floor", visible=False) for _ in range(width)]
            for _ in range(height)
        ]

        self.turn = 1

    def print_map(self):
        total_grid = (
            self.grid1 + [[Building(self,"Wall") for _ in range(self.width)]] + self.grid2
        )
        header = range(self.width)
        index = list(range(self.height)) + [""] + list(range(self.height))

        total_grid = tabulate(
            total_grid, headers=header, showindex=index, tablefmt="grid"
        ).split("\n")

        team1_hp = [[human.name, human.hp] for human in self.team1.members]
        team2_hp = [[human.name, human.hp] for human in self.team2.members]

        team_table = tabulate(
            team1_hp + team2_hp, headers=["Name", "HP"], tablefmt="simple"
        ).split("\n")

        longer = max(len(total_grid), len(team_table))
        for ele in [total_grid, team_table]:
            diff = abs(len(ele) - longer)
            for _ in range(diff):
                ele.append(" " * len(ele[0]))

        for grid_part, team_part in zip(total_grid, team_table):
            print(f"{grid_part}           {team_part}")

        # print(tabulate(total_grid, headers=header, showindex=index, tablefmt="grid"))

    def print_side(self, grid):
        print(tabulate(grid, tablefmt="grid"))

    def initialise_team(self, team, grid, num):
        if num == 1:
            self.team1 = team
        else:
            self.team2 = team
        for human in team.members:
            row_idx = human.row_idx
            col_idx = human.col_idx
            grid[row_idx][col_idx] = human

    def fight(self, team1, team2):
        self.initialise_team(team1, self.grid1, 1)
        self.initialise_team(team2, self.grid2, 2)

        self.print_map()

        speed1 = team1.get_speed()
        speed2 = team2.get_speed()
        first = team1 if speed1 >= speed2 else team2
        second = team1 if speed1 < speed2 else team2

        grid_map = {team1: self.grid1, team2: self.grid2}

        enemy_map = {team1: self.grid2, team2: self.grid1}

        players = first.members + second.members
        players = sorted(players, key=lambda human: human.speed, reverse=True)

        while team1.team_is_alive() and team2.team_is_alive():
            for human in players:
                if team1.team_is_alive() and team2.team_is_alive():
                    if human.is_alive():
                        while True:
                            skill_to_use = human.choose_move()
                            print("choose row", end=" ")
                            row_idx = int(input().strip())
                            print("choose column", end=" ")
                            col_idx = int(input().strip())
                            try:
                                skill_to_use.invoke(
                                    human,
                                    grid_map[human.team],
                                    enemy_map[human.team],
                                    row_idx,
                                    col_idx,
                                    self.turn
                                )
                                self.turn += 1
                                break
                            except Exception as e:
                                print(e)
                                continue

                        self.print_map()

        if team1.team_is_alive():
            print(f"{team1.name} win!")
        else:
            print(f"{team2.name} win!")


game = Game(width=10, height=3)

punch = BasicAttack("punch", 35)
lpunch = LightPunch("light punch", 35)
teleport = Teleport("teleport", 0)
fuckteam = Fuckteam("fuckteam", 999)
reveal = RevealingLight("revealing light", 0)

#def __init__(self, app, name, hp, speed, defense, type, skills, row_idx, col_idx)
a = Human(game,"ben", 10, 32, 5, "fire", [punch, reveal, teleport, fuckteam], 0, 0)
b = Human(game,"dylan", 10, 32, 5, "fire", [punch, lpunch, teleport, fuckteam], 1, 0)

c = Human(game,"brandon", 10, 32, 5, "fire", [punch, reveal], 0, 1)
d = Human(game,"karl", 100, 32, 0, "fire", [punch, lpunch], 1, 1)


# (self, name, hp, speed, defense, type, skills, row_idx, col_idx)
team1 = Team(game, "gay team", [a, b])
team2 = Team(game,"straight team", [c, d])


game.fight(team1, team2)
