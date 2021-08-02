from building import *
from human import Human


class Skill(object):
    def __init__(self, name, damage):
        self.damage = damage
        self.name = name
        # self.human = human

    def get_name(self):
        return self.name

    def invoke(
        self, caller: Human, caller_grid: list, grid: list, row_idx: int, col_idx: int,current:int
    ):
        pass


class BasicAttack(Skill):
    """
    Just punch the location and deal damage
    """

    def invoke(self, caller, caller_grid, grid, row_idx, col_idx,current):
        enemy = grid[row_idx][col_idx]
        if isinstance(enemy, Human):
            enemy.hp -= self.damage
            print(f"{enemy.name} takes {self.damage} damage and left {enemy.hp} hp")
            # print(enemy.name + " takes " + self.damage + " damage and left " + enemy.hp + " hp")
        else:  # damage floor by 1
            pass
            # enemy.hp -= 1


class LightPunch(Skill):
    """
    Punch the location and reveal the adjacent areas
    """

    def invoke(self, caller, caller_grid, grid, row_idx, col_idx,current):
        x_axis = [0, 0, -1, 1]
        y_axis = [-1, 1, 0, 0]
        enemy = grid[row_idx][col_idx]
        if isinstance(enemy, Human):
            enemy.hp -= self.damage
            enemy.visible = True
            print(f"{enemy.name} takes {self.damage} damage and left {enemy.hp} hp")

        for x, y in zip(x_axis, y_axis):
            try:
                adj = grid[row_idx + x][col_idx + y]
                if isinstance(adj, Human):
                    adj.visible = True
            except IndexError:
                continue

            # print(enemy.name + " takes " + self.damage + " damage and left " + enemy.hp + " hp")
        else:  # damage floor by 1
            # enemy.hp -= 1
            pass


class Teleport(Skill):
    """
    Teleport to another location in your grid
    """

    def invoke(self, caller, caller_grid, grid, row_idx, col_idx,current):
        ori_row = caller.row_idx
        ori_col = caller.col_idx

        if isinstance(grid[row_idx][col_idx], Human):
            raise Exception(f"{grid[row_idx][col_idx]} is already there")
        else:
            caller_grid[row_idx][col_idx] = caller
            caller.row_idx = row_idx
            caller.col_idx = col_idx
            caller_grid[ori_row][ori_col] = Building("Floor", visible=False)


class Fuckteam(Skill):
    """
    Fuck your team to give everyone +HP
    """

    def invoke(self, caller, caller_grid, grid, row_idx, col_idx,current):
        for teammate in caller.team.members:
            if teammate is not caller:
                teammate.hp += self.damage


class FloorBreak(Skill):
    # target area to destroy + sign 5 squares of floor. if directly target at human, nothing happens
    pass


class RevealingLight(Skill):
    # reveals whole grid for 1 turn
    def invoke(self, caller, caller_grid, grid, row_idx, col_idx, current):
        x_axis = [0, 0, -1, 1, -1, 1, -1, 1,0]
        y_axis = [-1, 1, 0, 0, -1, 1, 1, -1,0]
        enemy = grid[row_idx][col_idx]

        for x, y in zip(x_axis, y_axis):
            try:
                adj = grid[row_idx + x][col_idx + y]
                #if isinstance(adj, Human):
                adj.visible.set_value(True, False, current, expiry=1)
            except IndexError:
                continue


class SuperPunch(Skill):
    # does damage to all enemies in + sign shld have a long cd
    pass


class Fuckery(Skill):
    # gain control of 1 square of enemy if got  no one there
    pass
