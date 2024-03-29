import pygame
from levels import Level
from characters import Character
from weapons import Weapon
from colors import *
from fonts import *
from animations import Still
from animations import Animation
from clients import Client
import ast
import threading
import sys
from gameworld import Game_World
from sounds import Sound


class TheGame:
    def __init__(self, IP=0):
        self.state = ["character_choose", "free"]
        self.state_change = 0
        self.player = None
        self.opponent = None
        self.buffer = []
        self.opponent_buffer = []

        self.weapons = []
        self.characters = []

        self.matrix = []
        self.weapon_pos = []
        self.character_pos = []

        self.overlay = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        self.overlay_fixed = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        self.stills = []
        self.map = ["abstract matrix"]

        # self.console = pygame.Surface((1920,1080),pygame.SRCALPHA)
        # self.con_font=pygame.font.Font("assets/Fonts/NixieOne.otf",30)
        self.effect = ""
        self.score = 0
        self.current_frame = 0
        self.credit_count=0
        self.last_update = 0
        self.explosions = []
        self.client = Client(IP)
        self.DJ = Sound()

    def state_manager(self):
        '''Handles different states of a character'''
        if self.state[0] == "run_phase":
            self.DJ.play_Run()
            pass
        elif self.state[0] == "character_choose":
            self.state = ["object_place", "free"]
            self.character_choose()
            self.level = Level()
            self.game_world = Game_World("Z", self.level.w, self.level.h)
            self.state_change = 1
        elif self.state[0] == "object_place":
            self.set_matrix()
            self.set_inventory()
            self.character_assign()
            self.weapon_assign()
            self.goal_set()
            self.start()
            self.legend()
            self.level.surface.blit(self.overlay_fixed, (0, 0))
        elif self.state[0] == "send_map":
            self.client.sender("MS;HP_" + str(self.player.HP) + str(self.map))
        elif self.state[0] == "pause":
            self.client.sender("GO")
        elif self.state[0] == "win":
            self.state = ["object_place", "free"]
            if self.level.next() == "credits":
                self.state = ["credits"]
                print("Thank You For Playing.")
            self.stills.clear()
            self.weapons.clear()
            self.player = None
            self.opponent = None
            self.state_change = 1
            self.DJ.play_transition()
            self.DJ.stop_Run()

    def game_update(self, surface):
        '''Updates the game according to its state'''
        if self.state[0] in ["object_place", "send_map", "ready", "run_phase", "pause"]:
            surface.blit(self.level.surface, (0, 0))
            if self.state[0] == "object_place":
                cell = None
                temp = [
                    self.mouse_check(self.matrix)
                    or self.mouse_check(self.character_pos)
                    or self.mouse_check(self.weapon_pos)
                ]
                if self.state[1] != "free":
                    cell = eval(
                        f"self.{self.state[1]}[{self.state[2][0]}][{self.state[2][1]}]"
                    )
                    self.draw_select(surface, (200, 0, 0, 50), cell)
                if temp[0]:
                    if temp[0][0] != cell:
                        self.draw_select(surface, (0, 200, 200, 50), temp[0][0])
                    else:
                        self.draw_select(surface, (100, 0, 0, 255), cell, 0)
            if self.state[0] == "run_phase":
                self.current_frame += 1
                if self.player.state == "walk":
                    if self.player.wait > 0:
                        self.player.walk()
                        self.player.wait -= 1
                        if self.player.wait == 0:
                            self.use_effect()
                            self.set_wait()
                if self.opponent.state == "walk":
                    if self.opponent.wait > 0:
                        self.opponent.walk()
                        self.opponent.wait -= 1
                        if self.opponent.wait == 0:
                            self.opponent_use_effect()
                            self.opponent_set_wait()
            if self.state[0] == "pause":
                self.current_frame += 1
            if self.client.authority_advance:
                message = self.client.authority_messages.pop(0)
                self.network_manage(message)
                if self.client.authority_messages == []:
                    self.client.authority_advance = 0

            for image in self.stills:
                image.draw(surface)
            surface.blit(
                Courier.render("Wins    : " + str(self.score), True, black), (30, 960)
            )
            T_sec=int(self.current_frame/60)
            T_min=int(T_sec/60)
            T_hrs=int(T_min/60)

            surface.blit(
                Courier.render(f"Time    : {T_hrs}::{T_min:02d}::{T_sec:02d}", True, black),
                (1430, 960),
            )
            if self.explosions != []:
                fake_exp = self.explosions.copy()
                for i in fake_exp:
                    i.explode()
                    surface.blit(i.image, i.rect)
                    if i.current_sprite == 0:
                        self.explosions.remove(i)
            if self.player:
                self.player.SG.draw(surface)
                surface.blit(
                    Courier.render("Hp      : " + str(self.player.HP), True, black),
                    (30, 990),
                )
                surface.blit(
                    Courier.render(
                        "Reveals : " + str(self.player.reveals), True, black
                    ),
                    (30, 1020),
                )
                surface.blit(
                    Courier.render(
                        "Position: " + str(self.player.position), True, black
                    ),
                    (30, 1050),
                )
            if self.opponent:
                self.opponent.SG.draw(surface)
                surface.blit(
                    Courier.render("Hp      : " + str(self.opponent.HP), True, black),
                    (1430, 990),
                )
                surface.blit(
                    Courier.render(
                        "Reveals : " + str(self.opponent.reveals), True, black
                    ),
                    (1430, 1020),
                )
                surface.blit(
                    Courier.render(
                        "Position: " + str(self.opponent.position), True, black
                    ),
                    (1430, 1050),
                )
        elif self.state[0] == "Halt":
            if self.client.authority_advance:
                message = self.client.authority_messages.pop(0)
                self.network_manage(message)
                if self.client.authority_messages == []:
                    self.client.authority_advance = 0
            for i, col in enumerate(self.level.occupants):
                for j, cell in enumerate(col):
                    if cell == []:
                        temp = []
                    elif cell[0][0] == "block":
                        temp = cell[0][1]
                    elif cell[0][0] == "weapon":
                        temp = cell[0][1].id
                        temp = str(temp) + str(cell[0][1].activated)
                        if len(cell) > 1:
                            temp = temp + cell[1][1]
                    surface.blit(
                        Courier.render(str(temp), True, black),
                        (100 + 50 * i, 100 + 50 * j),
                    )
        
        elif self.state[0] == "credits":
            credit = pygame.image.load('assets/0x464F5220444F45').convert_alpha()
            while self.credit_count<1870:
                surface.fill(white)
                self.credit_count+=1
                surface.blit(credit,(0,-self.credit_count))
                pygame.display.update()
            surface.blit(credit,(0,-1870))

    # initial phase

    def character_choose(self):
        '''Allows the player to choose a character'''
        # after finished
        self.characters = [
            Character("Captain"),
            Character("Spy"),
            Character("Spy"),
            Character("Captain"),
            Character("Captain"),
            Character("Spy"),
        ]

    ##phase 'object_place'
    # 1.level initialize
    def set_matrix(self):
        '''Sets the matrix of the level'''
        size = 60
        self.matrix.clear()
        x, y, w, h = self.level.x, self.level.y, self.level.w, self.level.h
        for i in range(h):
            temp = []
            for j in range(w):
                temp.append(pygame.Rect((x + j) * size, (y + i) * size, size, size))
                pygame.draw.rect(
                    self.overlay_fixed,
                    (255, 255, 255, 20),
                    ((x + j) * size, (y + i) * size, size - 3, size - 3),
                    border_radius=20,
                )
            self.matrix.append(temp)
        self.map = [[[] for i in range(w)] for i in range(h)]

    def set_inventory(self):
        '''Sets the inventory of the player'''
        self.character_pos.clear()
        self.weapon_pos.clear()
        for i in range(6):
            temp = []
            for j in range(1):
                temp.append(
                    pygame.Rect(60 + (90 + 30) * j, 150 + (90 + 30) * i, 90, 90)
                )
                pygame.draw.rect(
                    self.overlay_fixed, (50, 50, 50, 100), temp[-1], border_radius=20
                )
                pygame.draw.rect(
                    self.overlay_fixed,
                    (0, 0, 0, 100),
                    temp[-1],
                    width=5,
                    border_radius=20,
                )
            self.character_pos.append(temp)
        for i in range(int(len(self.level.allowed_weapon) / 3)):
            temp = []
            for j in range(3):
                temp.append(
                    pygame.Rect(1560 + 30 + (90 + 15) * j, 150 + (90 + 15) * i, 90, 90)
                )
                pygame.draw.rect(
                    self.overlay_fixed, (50, 50, 50, 100), temp[-1], border_radius=20
                )
                pygame.draw.rect(
                    self.overlay_fixed,
                    (0, 0, 0, 100),
                    temp[-1],
                    width=5,
                    border_radius=20,
                )
            self.weapon_pos.append(temp)

    # 2.level screen setup
    def character_assign(self):
        '''Assigns the characters to the player'''
        for index, character in enumerate(self.characters):
            temp = Still("assets/character/" + character.name + ".png")
            temp.zoom(1.2)
            cell = self.character_pos[index][0]
            temp.place(cell.center[0], cell.center[1] - 10, wrt="c")
            temp.draw(self.overlay_fixed)
            if character.HP <= 0:
                No = Still("assets/NO.png")
                # No.resize(70,70)
                No.place(cell.center[0], cell.center[1], wrt="c")
                No.draw(self.overlay_fixed)

    def weapon_assign(self):
        '''Assigns the weapons to the player'''
        # to be chnged to support numbers
        for index, name in enumerate(self.level.allowed_weapon):
            temp = Still("assets/Weapon/" + name + ".png")
            temp.resize(70, 70)
            cell = self.weapon_pos[int(index / 3)][index % 3]
            temp.place(cell.center[0], cell.center[1], wrt="c")
            temp.draw(self.overlay_fixed)
            self.weapons.append([name, self.level.weapon_counts[index]])

    def goal_set(self):
        '''Sets the goal of the level'''
        temp = Weapon("crystal_blue")
        temp.image.rect.center = self.matrix[int(self.level.h / 2)][0].center
        self.stills.append(temp.image)
        self.level.occupants[0][int(self.level.h / 2)] = [["weapon", temp]]

        temp = Weapon("goal")
        temp.image.rect.center = self.matrix[int(self.level.h / 2) - 1][0].center
        self.stills.append(temp.image)
        self.level.occupants[0][int(self.level.h / 2) - 1] = [["weapon", temp]]

        temp = Weapon("crystal_red")
        temp.image.rect.center = self.matrix[int(self.level.h / 2)][
            self.level.w - 1
        ].center
        self.stills.append(temp.image)
        self.level.occupants[self.level.w - 1][int(self.level.h / 2)] = [
            ["weapon", temp]
        ]

        temp = Weapon("no_goal")
        temp.image.rect.center = self.matrix[int(self.level.h / 2) + 1][
            self.level.w - 1
        ].center
        self.stills.append(temp.image)
        self.level.occupants[self.level.w - 1][int(self.level.h / 2) + 1] = [
            ["weapon", temp]
        ]

    # 3.receive input
    def mouse_click(self):
        '''Handles the mouse click event'''
        # code in character,initial phase
        if self.state[0] == "object_place":
            if self.start_rect.collidepoint(pygame.mouse.get_pos()):
                if self.player:
                    self.state = ["send_map", "free"]
                    self.state_change = 1
            else:
                temp = self.mouse_check(self.matrix)
                if temp:
                    if temp[2] < self.level.w / 2 and temp[1] < self.level.h:
                        if self.state[1] in ["free", "matrix"]:
                            self.state = ["object_place", "matrix", [temp[1], temp[2]]]
                        else:
                            if self.state[1] == "weapon_pos":
                                self.weapon_place(
                                    self.state[2][0], self.state[2][1], temp[1], temp[2]
                                )
                            elif self.state[1] == "character_pos":
                                self.character_place(
                                    self.state[2][0], self.state[2][1], temp[1], temp[2]
                                )
                            self.state = ["object_place", "free"]

                else:
                    temp = self.mouse_check(self.weapon_pos)
                    if temp:
                        # check for validity
                        if self.level.weapon_counts[temp[1] * 3 + temp[2]] > 0:
                            if self.state[1] in ["free", "weapon_pos", "character_pos"]:
                                self.state = [
                                    "object_place",
                                    "weapon_pos",
                                    [temp[1], temp[2]],
                                ]
                            elif self.state[1] == "matrix":
                                self.weapon_place(
                                    temp[1], temp[2], self.state[2][0], self.state[2][1]
                                )
                                self.state = ["object_place", "free"]
                        else:
                            self.state = ["object_place", "free"]

                    else:
                        temp = self.mouse_check(self.character_pos)
                        if temp:
                            if self.characters[temp[1]].HP > 0:
                                if self.state[1] in [
                                    "free",
                                    "weapon_pos",
                                    "character_pos",
                                ]:
                                    self.state = [
                                        "object_place",
                                        "character_pos",
                                        [temp[1], temp[2]],
                                    ]
                                elif self.state[1] == "matrix":
                                    self.character_place(
                                        temp[1],
                                        temp[2],
                                        self.state[2][0],
                                        self.state[2][1],
                                    )
                                    self.state = ["object_place", "free"]
                            else:
                                self.state = ["object_place", "free"]
                        else:
                            self.state = ["object_place", "free"]

    def mouse_check(self, matrix):
        '''Checks if the mouse is on the matrix'''
        pos = pygame.mouse.get_pos()
        for i, row in enumerate(matrix):
            for j, cell in enumerate(row):
                if cell.collidepoint(pos):
                    return [cell, i, j]
        return None

    def draw_select(self, screen, color, rect, fill=1):
        '''Draws the selection rectangle'''
        Surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        if fill:
            pygame.draw.rect(
                Surface,
                (255, 255, 255, 100),
                (0, 0, rect.width, rect.height),
                border_radius=20,
            )
        pygame.draw.rect(
            Surface, color, (0, 0, rect.width, rect.height), width=5, border_radius=20
        )
        screen.blit(Surface, rect.topleft)
        del Surface

    # 4.placement of objects
    def character_place(self, from_x, from_y, to_x, to_y):
        '''Places the character on the map'''
        representation = {"Captain": "P1", "Spy": "P2"}
        if self.level.occupants[to_y][to_x] == []:
            if self.player:
                self.level.occupants[self.player.position[0]][
                    self.player.position[1]
                ] = []
                self.map[self.player.position[1]][self.player.position[0]] = []
            self.player = self.characters[from_x]
            self.player.position = [to_y, to_x]
            self.level.occupants[to_y][to_x] = [["block", "P"]]
            self.map[to_x][to_y] = [representation[self.player.name]]
            self.player.animation.rect.center = (
                (self.level.x + to_y) * 60 + 30,
                (self.level.y + to_x) * 60 - 10,
            )

    def weapon_place(self, from_x, from_y, to_x, to_y):
        '''Places the weapon on the map'''
        if self.level.occupants[to_y][to_x] == []:
            temp = Weapon(self.weapons[from_x * 3 + from_y][0])
            self.level.weapon_counts[from_x * 3 + from_y] -= 1
            if self.level.weapon_counts[from_x * 3 + from_y] == 0:
                No = Still("assets/NO.png")
                # No.resize(70,70)
                cell = self.weapon_pos[from_x][from_y]
                No.place(cell.center[0], cell.center[1], wrt="c")
                No.draw(self.level.surface)

            temp.image.rect.center = self.matrix[to_x][to_y].center
            self.level.occupants[to_y][to_x] = [["weapon", temp]]
            self.map[to_x][to_y] = [temp.id]
            self.stills.append(temp.image)

    # phase 'run phase'
    def input_receive(self, direction, state):
        '''Receives the input from the player'''
        # code in run phase
        if self.state[0] == "run_phase":
            if direction != "yes" and direction != "no":
                if state == "remove":
                    if direction in self.buffer:
                        self.buffer.remove(direction)
                elif state == "walk":
                    self.buffer.append(direction)
                    if self.player.wait == 0:
                        self.set_wait()
                        self.player.direction = direction
                        self.player.idle(change=True)
            elif direction == "yes":
                pass

    def set_wait(self):
        '''Sets the wait time for the player'''
        if self.buffer:
            while self.buffer:
                entry = self.buffer[-1]
                if self.validate_move(entry):
                    self.client.sender(
                        "RR;" + str(self.current_frame) + ";" + self.effect
                    )
                    if self.player.direction != entry:
                        self.player.direction = entry
                        self.player.idle(change=True)
                    else:
                        self.player.idle()
                    self.player.wait = 60
                    self.player.state = "walk"
                    return
                else:
                    self.buffer.remove(entry)
        if not self.buffer:
            self.player.wait = 0
            self.player.state = "idle"

    def opponent_set_wait(self):
        '''Sets the wait time for the opponent'''
        if self.opponent.wait != 0 or self.opponent_buffer == []:
            return
        received_move =self.opponent_buffer.pop(0)
        msg,frame_number = received_move[0],received_move[1]
        swap = {"up": "down", "down": "up", "left": "right", "right": "left"}
        up, down, left, right = "up", "down", "left", "right"
        split = msg.split(";")
        x, y, entry = eval(split[0])
        if self.opponent.direction != swap[entry]:
            self.opponent.direction = swap[entry]
            self.opponent.idle(change=True)
        else:
            self.opponent.idle()
        delta = self.current_frame - frame_number
        '''
        if delta > 60 or delta <0:
            self.opponent.wait=1
        else:
            self.opponent.wait = delta
        '''
        self.opponent.wait=60
        self.opponent.state = "walk"

        new_x = self.level.w - x - 1
        new_y = self.level.h - y - 1
        effect = f"self.do_opponent_move({new_x},{new_y},{swap[entry]})"
        for i, char in enumerate(msg):
            if char == ";":
                effect += msg[i:]
                break
        self.opponent_effect = effect

    def opponent_move(self, x, y, entry):
        '''Moves the opponent'''
        return (x, y, entry)

    def validate_move(self, entry):
        '''Validates the move'''
        move = {"up": [0, -1], "down": [0, 1], "left": [-1, 0], "right": [1, 0]}
        new_x = self.player.position[0] + move[entry][0]
        new_y = self.player.position[1] + move[entry][1]
        if new_x in range(self.level.w):
            if new_y in range(self.level.h):
                occupant = self.level.occupants[new_x][new_y]
                if occupant == []:
                    self.effect = f"self.move({new_x},{new_y},{entry})"
                    return 1
                elif occupant[0][0] == "weapon":
                    if occupant[0][1].activated:
                        if occupant[0][1].id == "CB":
                            print(f"In front : {occupant} at {new_x} , {new_y}")
                            return 0
                        if occupant[0][1].effect == "empty":
                            self.effect = f"self.move({new_x},{new_y},{entry})"

                        else:
                            self.effect = f"self.move({new_x},{new_y},{entry});{occupant[0][1].effect}"
                    else:
                        self.effect = f"self.move({new_x},{new_y},{entry})"
                    return 1
                else:
                    print(f"In front : {occupant} at {new_x} , {new_y}")
                    return 0

    def move(self, x, y, entry):
        '''Moves the player'''
        self.level.occupants[self.player.position[0]][self.player.position[1]].remove(
            ["block", "P"]
        )
        self.level.occupants[x][y].append(["block", "P"])
        self.player.position = [x, y]
        self.player.animation.rect.center = (
            (self.level.x + x) * 60 + 30,
            (self.level.y + y) * 60 - 10,
        )

    def undo_move(self, x, y):
        '''Undoes the move'''
        self.level.occupants[self.player.position[0]][self.player.position[1]].remove(
            ["block", "P"]
        )
        self.level.occupants[x][y].append(["block", "P"])
        self.player.position = [x, y]

    def do_opponent_move(self, x, y, entry):
        '''Moves the opponent'''
        self.level.occupants[self.opponent.position[0]][
            self.opponent.position[1]
        ].remove(["block", "X"])
        self.level.occupants[x][y].append(["block", "X"])
        self.opponent.position = [x, y]
        self.opponent.animation.rect.center = (
            (self.level.x + x) * 60 + 30,
            (self.level.y + y) * 60 - 10,
        )

    def take_damage(self, amount):
        '''Takes amount damage and modify player health'''
        self.player.HP -= amount
        temp = self.level.occupants[self.player.position[0]][self.player.position[1]][0]
        temp[1].expl.rect.center = self.matrix[self.player.position[1]][
            self.player.position[0]
        ].center
        self.explosions.append(temp[1].expl)
        self.DJ.play_blast()
        # could be in negative
        if self.player.HP <= 0:
            self.death()

    def undo_take_damage(self, amount):
        '''Undoes the damage and increases player health'''
        self.player.HP += amount

    def opponent_take_damage(self, amount):
        '''Takes amount damage and modify opponent health'''
        self.opponent.HP -= amount
        temp = self.level.occupants[self.opponent.position[0]][
            self.opponent.position[1]
        ][0]
        temp[1].expl.rect.center = self.matrix[self.opponent.position[1]][
            self.opponent.position[0]
        ].center
        self.explosions.append(temp[1].expl)
        if self.opponent.HP <= 0:
            self.opponent_death()

    def remove(self):
        '''Removes the block'''
        temp = self.level.occupants[self.player.position[0]][self.player.position[1]][0]
        temp[1].activated = 0
        try:
            self.stills.remove(temp[1].image)
        except:
            pass

    def opponent_remove(self):
        '''Removes the block'''
        temp = self.level.occupants[self.opponent.position[0]][
            self.opponent.position[1]
        ][0]
        temp[1].activated = 0
        try:
            self.stills.remove(temp[1].image)
        except:
            pass

    def undo_remove(self):
        '''Undoes the removal of the block'''
        temp = self.level.occupants[self.player.position[0]][self.player.position[1]][0]
        temp[1].activated = 1
        self.stills.append(temp[1].image)

    def took(self):
        '''Player takes the crystal'''
        self.player.took = "took"

    def opponent_took(self):
        '''Opponent takes the crystal'''
        self.opponent.took = "took"

    def undo_took(self):
        '''Undoes the taking of the crystal'''
        self.player.took = "free"

    def win(self):
        '''Player wins'''
        if self.player.took == "took":
            # here first resolve all conflicts
            self.score += 1
            self.state = ["pause"]
            self.state_change = 1

    def opponent_win(self):
        '''Opponent wins'''
        if self.opponent.took == "took":
            self.state = ["pause"]
            self.state_change = 1

    def death(self):
        '''Player dies'''
        # resolve all conflicts first
        self.state = ["pause"]
        self.state_change = 1

    def opponent_death(self):
        '''Opponent dies'''
        self.score += 1
        self.state = ["pause"]
        self.state_change = 1

    def use_effect(self):
        '''Uses the effect of the block'''
        up, down, left, right = "up", "down", "left", "right"
        exec(self.effect)
        self.effect = ""

    def opponent_use_effect(self):
        '''Uses the effect of the block'''
        up, down, left, right = "up", "down", "left", "right"
        exec(self.opponent_effect)
        self.opponent_effect = ""

    def legend(self):
        '''Displays the legend'''
        character_word = Goldie.render("Character", True, black)
        weapon_word = Goldie.render("Weapon", True, black)
        self.overlay_fixed.blit(character_word, (60, 60))
        self.overlay_fixed.blit(weapon_word, (1590, 60))

    def start(self):
        '''Starts the game'''
        self.start_rect = pygame.Rect(840, 960, 240, 90)
        pygame.draw.rect(
            self.overlay_fixed, (50, 50, 50, 100), self.start_rect, border_radius=20
        )
        pygame.draw.rect(
            self.overlay_fixed,
            (0, 0, 0, 100),
            self.start_rect,
            width=5,
            border_radius=20,
        )

    def set_opponent(self, message):
        '''Sets the opponent'''
        represent = {
            "M": "mine",
            "B": "bomb",
            "P1": "Captain",
            "P2": "Spy",
            "X1": "Captain",
            "X2": "Spy",
        }
        temp_message = message
        HP = temp_message[3]
        temp_matrix = ast.literal_eval(temp_message[4:])
        self.game_world.data["matrix"] = temp_matrix
        for x, row in enumerate(temp_matrix):
            for y, cell in enumerate(row):
                if y < self.level.w / 2:
                    continue
                elif cell:
                    if cell[0] in ["X1", "X2"]:
                        self.opponent = Character(represent[cell[0]])
                        self.opponent.direction = "left"
                        self.opponent.idle(change=True)
                        self.opponent.position = [y, x]
                        self.level.occupants[y][x] = [["block", "X"]]
                        self.opponent.animation.rect.center = (
                            (self.level.x + y) * 60 + 30,
                            (self.level.y + x) * 60 - 10,
                        )
                    elif cell[0] in ["M", "B"]:
                        temp = Weapon(represent[cell[0]])
                        temp.image.rect.center = self.matrix[x][y].center
                        self.level.occupants[y][x] = [["weapon", temp]]
                        # self.stills.append(temp.image)

        self.opponent.HP = int(HP)
        self.state[0] = "ready"
        self.client.sender("OK")

    def network_manage(self, message):
        '''Manages the network'''
        """handling messages recieve in the run phase from the server"""
        split = message.split(";")
        code = split.pop(0)
        if code == "make_opponent_move":
            """received when opponent move is allowed"""
            frame_number = split.pop(0)
            perform = str(";".join([x for x in split if x != ""]))
            self.opponent_buffer.append([perform,int(frame_number)])
            self.opponent_set_wait()
            """make change to oswait as effect should be list"""
        elif code == "set_matrix":
            self.state[0] = "receive_map"
            self.set_opponent(split[0])
            self.state_change = 1
        elif code == "request_frame":
            self.client.sender(f"RR;{self.current_frame};self.fake_move()")
        elif code == "KO":
            self.state[0] = "run_phase"
            self.current_frame = 0
            self.state_change = 1
        elif code == "OG":
            self.state = ["win"]
            self.state_change = 1
        elif code == "rollback":
            print("Rollback Recv")
            self.rollback(split)

    def rollback(self, split):
        '''Rolls back the game'''
        frame_number = int(split.pop(0))
        self.current_frame = frame_number
        temp_player = ast.literal_eval(split[0])
        matrix = temp_player["matrix"]
        self.player.HP=int(temp_player["HP"])
        self.opponent.HP=int(temp_player["opponent_HP"])
        self.player.took=int(temp_player["took"])
        self.opponent.took=int(temp_player["opponent_took"])
        print("Before : ")
        self.print_lo()
        for row in self.level.occupants:
            for cell in row:
                if ["block", "P"] in cell:
                    cell.remove(["block", "P"])
                if ["block", "X"] in cell:
                    cell.remove(["block", "X"])
        print("Remove Player : ")
        self.print_lo()
        for y, row in enumerate(matrix):    
            for x, cell in enumerate(row):
                if cell == []:
                    self.level.occupants[x][y] = []
                    continue
                else:
                    if cell[0] in ["M", "B", "CR", "CB"]:
                        if not self.level.occupants[x][y][0][1].activated:
                            self.level.occupants[x][y][0][1].activated = 1
                            if x < self.level.w / 2:
                                self.stills.append(
                                    self.level.occupants[x][y][0][1].image
                                )
                    if cell[-1] in ["P1", "P2"]:
                        self.player.position = [x, y]
                        self.player.animation.rect.center = ((self.level.x + x) * 60 + 30,(self.level.y + y) * 60 - 10)
                        self.level.occupants[x][y].append(["block", "P"])
                    if cell[-1] in ["X1", "X2"]:
                        self.opponent.position = [x, y]
                        self.opponent.animation.rect.center = ((self.level.x + x) * 60 + 30,(self.level.y + y) * 60 - 10)

                        self.level.occupants[x][y].append(["block", "X"])
        print("After : ")
        self.print_lo()
        self.state[0]='run_phase'

    def print_lo(self):
        '''Prints the level occupants'''
        for i in range(self.level.h):
            for j in range(self.level.w):
                print(self.level.occupants[j][i],end='##')
            print('\n')