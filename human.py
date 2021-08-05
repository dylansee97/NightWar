from time_variable import TimeVariable



class Human:
    def __init__(self, app, name, hp, speed, defense, type, skills, row_idx, col_idx):
        self.name = name
        self.hp = hp
        self.speed = speed
        self.skills = skills

        self.defense = defense  # between 0 and 10
        self.type = type
        self.row_idx = row_idx
        self.col_idx = col_idx
        self.team = None
        self.app = app

        self.visible = TimeVariable(
            app=self.app, value=False, default=True, created=1, expiry=999
        )

    def __repr__(self) -> str:
        return self.name if self.visible.get_value() else ""

    def choose_move(self):
        print(f"[{self.name} - {self.app.turn}] choose your move!", end=" ")
        [
            print(f"{idx}. {skill.get_name()}", end="    ")
            for idx, skill in enumerate(self.skills)
        ]
        skill = int(input().strip())
        chosen = self.skills[skill]
        print(f"You chose {chosen.get_name()}")
        return chosen

    def is_effective_against(self, human):
        if self.type == human.type:
            return 1
        if self.type == "fire" and human.type == "grass":
            return 2
        if self.type == "grass" and human.type == "water":
            return 2
        if self.type == "water" and human.type == "fire":
            return 2

        if self.type == "grass" and human.type == "fire":
            return 0.5
        if self.type == "water" and human.type == "grass":
            return 0.5
        if self.type == "fire" and human.type == "water":
            return 0.5

    def is_alive(self):
        if self.hp <= 0:
            return False
        else:
            return True

    def reset(self):
        self.hp = 100


"""
    def attack(self,human):
        attack_damage = random.randint(self.damage -3,self.damage +3) / human.defense
        attack_damage *= self.is_effective_against(human)
        human.hp -= attack_damage

        print(str(self.name) + " attacks " + str(human.name) + " for " + str(attack_damage) + " damage " )
        print(str(self.name) + " HP Remaining: " + str(self.hp) + " "+ str(human.name) + " HP Remaining: " + str(human.hp))
        print("\n")
"""
