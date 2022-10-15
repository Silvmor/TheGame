class Game_World:
    '''Class that simulates the characters in the game world'''
    def __init__(self, ID, w, h):
        self.w, self.h = w, h
        self.data = {
            "ID": ID,
            "player": [],
            "opponent": [],
            "matrix": [[[] for i in range(self.w)] for i in range(self.h)],
            "frame": 0,
            "HP": 0,
            "took": 0,
            "opponent_HP": 0,
            "opponent_took": 0,
        }

    def move(self, x, y, entry):
        '''Moves the player to the specified position'''
        if self.data["opponent"] == [x,y]:
            raise Exception("Conflict for same position.")
            return
        temp = self.data["matrix"][self.data["player"][1]][self.data["player"][0]].pop()
        self.data["player"] = [x,y]
        self.data["matrix"][self.data["player"][1]][self.data["player"][0]].append(temp)

    def remove(self):
        '''Removes the player from the game world'''
        self.data["matrix"][self.data["player"][1]][self.data["player"][0]].pop(0)

    def took(self):
        '''Called when the player takes an item'''
        self.data["took"] = 1

    def take_damage(self, amount):
        '''Called when the player takes damage'''
        self.data["HP"] -= amount

    def opponent_move(self, x, y, entry):
        '''Moves the opponent to the specified position'''
        if self.data["player"] == [self.w - x - 1, self.h - y - 1]:
            raise Exception("Conflict for same position.")
            return
        temp = self.data["matrix"][self.data["opponent"][1]][
            self.data["opponent"][0]
        ].pop()
        new_x = self.w - x - 1
        new_y = self.h - y - 1
        self.data["opponent"] = [new_x, new_y]
        self.data["matrix"][self.data["opponent"][1]][self.data["opponent"][0]].append(
            temp
        )

    def opponent_remove(self):
        '''Removes the opponent from the game world'''
        self.data["matrix"][self.data["opponent"][1]][self.data["opponent"][0]].pop(0)

    def opponent_took(self):
        '''Called when the opponent takes an item'''
        self.data["opponent_took"] = 1

    def opponent_take_damage(self, amount):
        '''Called when the opponent takes damage'''
        self.data["opponent_HP"] -= amount

    def fake_move(self):
        return 1

    def opponent_fake_move(self):
        return 1

    def win(self):
        pass

    def opponent_win(self):
        pass

    def death(self):
        pass

    def opponent_death(self):
        pass
