import sys
import ast
import pygame
import socket
import threading
import screeninfo
from fonts import *
from colors import *
from fps import FPS
from gameworld import Game_World


""" initialize """
pygame.init()
screen = screeninfo.get_monitors()[0]
clock = pygame.time.Clock()
display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Server")
"""initialization end"""


"""network operations"""


def accept_connections():
    global index, threads, running
    index = 0
    while index < 2:
        running[index] = 1
        connectionSocket, address = serverSocket.accept()
        RML((f"Client_{index} {address} is connected."))
        connections.append(connectionSocket)
        threads.append(
            threading.Thread(target=connection, args=(connectionSocket, index))
        )
        threads[index].start()
        index += 1


def connection(sock, ID):
    global running
    sock.setblocking(False)
    receiver_thread = threading.Thread(target=receiver, args=(sock, ID))
    receiver_thread.start()
    while running[ID]:
        update(sock, ID)


def sender(msg, sock, ID):
    totalsent = 0
    while totalsent < len(msg):
        sent = sock.send(msg[totalsent:].encode())
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent
    RML(f"Sent_{int(ID)} : {msg}")


def receiver(sock, ID):
    result = []
    msg_sofar = ""
    semaphor =0
    while True:
        try:
            chunk = sock.recv(64).decode("utf-8")
            RML('Chunk : '+chunk)
            while '$' in chunk:
                index = chunk.find('$')
                msg_sofar += chunk[:index]
                result.append(msg_sofar)
                semaphor+=1
                msg_sofar=''
                if(index == len(chunk)-1):
                    chunk=''
                    msg_sofar = ''
                else:
                    chunk = chunk[index+1:]
                RML('Dollar Found : ')
            msg_sofar += chunk
        except Exception as e:
            if str(e)[1:9]=='WinError':
                pass
            else:
                RML(str(e))
        while semaphor>0:
            authority(result.pop(0), sock, ID)
            semaphor-=1
            continue


def authority(message, sock, ID):
    global State_ADVANCE, mess
    RML(f"Client_{ID} : {message}")
    split = message.split(";")
    temp = split.pop(0)
    if temp == "MS":
        players[ID].data["HP"] = int(message[6])
        players[not ID].data["opponent_HP"] = int(message[6])
        players[ID].data["matrix"] = ast.literal_eval(message[7:])
        set_player(ID)
        if players[not ID].data["player"] != []:
            set_opponents()
            State_ADVANCE = [1, 1]
    elif temp == "OK":
        State_ADVANCE[ID] += 1
    elif temp == "GO":
        State_ADVANCE[ID] += 1
    elif temp == "RR":
        """
        here you receive effects in split
        [f_no,self.move(...),...]
        """
        if messageCache[ID] == []:
            messageCache[ID].append(split)
            check(ID)
        else:
            messageCache[ID].append(split)


"""END"""


"""move validation"""
under_checking = 0
messageCache = [[], []]


def check(ID):
    global under_checking
    RML(f"\n{ID}_myCache : {messageCache[ID]}")
    RML(f"{ID}_opCache : {messageCache[not ID]}")
    if messageCache[not ID] == [] or under_checking:
        sender("request_frame", connections[not ID], not ID)
    else:
        check_move(ID)


def check_move(ID):
    global under_checking
    under_checking = 1
    """perform all moves in cache until not possible then done"""
    global w, h
    temp_player = Game_World(ID, w, h)
    temp_player.data = ast.literal_eval(str(players[ID].data))

    x_temp_moves = [[f"temp_player.{y[5:]}" for y in x[1:]] for x in messageCache[ID]]
    x_temp_opponent_moves = [
        [f"temp_player.opponent_{y[5:]}" for y in x[1:]] for x in messageCache[not ID]
    ]
    RML(f"{ID}_xTmp_moves : " + str(x_temp_moves))
    RML(f"{ID}_xop_Tmp_moves : " + str(x_temp_opponent_moves))
    while messageCache[ID] and messageCache[not ID]:
        temp_moves = [[f"temp_player.{y[5:]}" for y in messageCache[ID][0][1:]]]
        temp_opponent_moves = [
            [f"temp_player.opponent_{y[5:]}" for y in messageCache[not ID][0][1:]]
        ]
        RML(f"{ID}_single_Tmp_moves : " + str(temp_moves))
        RML(f"{ID}_single_op_Tmp_moves : " + str(temp_opponent_moves))
        if int(messageCache[ID][0][0]) <= int(messageCache[not ID][0][0]):
            if validate(temp_moves.pop(0), temp_player):
                forward(messageCache[ID].pop(0), ID)
            else:
                rollback(messageCache[ID].pop(0), ID)
                messageCache[ID].clear()
        elif int(messageCache[ID][0][0]) > int(messageCache[not ID][0][0]):
            if validate(temp_opponent_moves.pop(0), temp_player):
                forward(messageCache[not ID].pop(0), not ID)
            else:
                rollback(messageCache[not ID].pop(0), not ID)
                messageCache[not ID].clear()

    while messageCache[ID]:
        if messageCache[ID][0][1] == "self.fake_move()":
            messageCache[ID].pop(0)
        else:
            sender("request_frame", connections[not ID], not ID)
            break
    while messageCache[not ID]:
        if messageCache[not ID][0][1] == "self.fake_move()":
            messageCache[not ID].pop(0)
        else:
            sender("request_frame", connections[ID], ID)
            break
    under_checking = 0


def validate(effects, temp_player):
    up, down, left, right = "up", "down", "left", "right"
    for effect in effects:
        try:
            exec(effect)
        except Exception as e:
            RML("could not execute")
            RML(effect + " ON : ")
            RML(str(temp_player.data["matrix"]))
            RML(f"Beacuse : {e}")
            return 0
    return 1


def forward(message, ID):
    """ message = [frame_no, self.move(x,y,direction), ... self.effects ...]"""
    print("forward_start :")
    global player_0, player_1, players
    up, down, left, right = "up", "down", "left", "right"
    frame_number = message.pop(0)
    if message != []:
        if message[0] != "self.fake_move()":
            fw_msg = f"make_opponent_move;{frame_number};" + str(
                ";".join(
                    [
                        f"{x[:5]}opponent_{x[5:]}"
                        for x in message
                        if (x != "" and x != "self.fake_move()")
                    ]
                )
            )  # rajan
            sender(fw_msg, connections[not ID], not ID)
            temp_moves = [f"players[int(ID)].{x[5:]}" for x in message]
            temp_opponent_moves = [
                f"players[int(not ID)].opponent_{x[5:]}" for x in message
            ]
            RML(f"{int(ID)}_perform" + str(temp_moves))
            RML(f"{int(not ID)}_perform" + str(temp_opponent_moves))
            for move_player in temp_moves:
                RML("Move : " + move_player)
                try:
                    eval(move_player)
                except Exception as e:
                    RML(f"NOT PERFORMED AS : {e}")
            for move_op in temp_opponent_moves:
                RML("op_Move : " + move_op)
                try:
                    eval(move_op)
                except Exception as e:
                    RML(f"NOT PERFORMED AS : {e}")
    else:
        RML("Error_forwarding_empty")
    print("forward_End :")


def rollback(split, ID):
    frame_number = split[0]
    sender(f"rollback;{frame_number};" + str(players[ID].data), connections[ID], ID)


"""END"""


"""Player data Initialization"""


def set_player(ID):
    for y, row in enumerate(players[ID].data["matrix"]):
        for x, cell in enumerate(row):
            if cell != []:
                if cell[0] in ["P1", "P2"]:
                    players[ID].data["player"] = [x, y]
                    players[not ID].data["opponent"] = [w - x - 1, h - y - 1]


def set_opponents():
    global w, h
    for y, row in enumerate(players[1].data["matrix"]):
        for x, cell in enumerate(row):
            if cell != []:
                if cell[0] in ["P1", "P2"]:
                    players[0].data["matrix"][h - y - 1][w - x - 1] = ["X" + cell[0][1]]
                else:
                    players[0].data["matrix"][h - y - 1][w - x - 1] = ast.literal_eval(
                        str(cell)
                    )

    for y, row in enumerate(players[0].data["matrix"]):
        for x, cell in enumerate(row):
            if cell != []:
                if cell[0] in ["P1", "P2"]:
                    players[1].data["matrix"][h - y - 1][w - x - 1] = ["X" + cell[0][1]]
                elif cell[0] in ["X1", "X2"]:
                    players[1].data["matrix"][h - y - 1][w - x - 1] = ["P" + cell[0][1]]

                else:
                    players[1].data["matrix"][h - y - 1][w - x - 1] = ast.literal_eval(
                        str(cell)
                    )

    players[0].data["matrix"][int(h / 2)][0] = ["CB"]
    players[0].data["matrix"][int(h / 2) - 1][0] = ["Gp"]
    players[0].data["matrix"][int(h / 2)][w - 1] = ["CR"]
    players[0].data["matrix"][int(h / 2) + 1][w - 1] = ["Gx"]
    players[1].data["matrix"][int(h / 2)][0] = ["CB"]
    players[1].data["matrix"][int(h / 2) - 1][0] = ["Gp"]
    players[1].data["matrix"][int(h / 2)][w - 1] = ["CR"]
    players[1].data["matrix"][int(h / 2) + 1][w - 1] = ["Gx"]


def update(sock, ID):
    global State_ADVANCE
    if State_ADVANCE == [1, 1] or (
        State_ADVANCE[not ID] == 2 and State_ADVANCE[ID] == 1
    ):
        """send matrix"""
        msg = (
            "set_matrix;HP_"
            + str(players[ID].data["opponent_HP"])
            + str(players[ID].data["matrix"])
        )
        sender(msg, sock, ID)
        State_ADVANCE[ID] += 1
    elif State_ADVANCE == [3, 3] or (
        State_ADVANCE[not ID] == 4 and State_ADVANCE[ID] == 3
    ):
        """send KO = begin run_phase"""
        State_ADVANCE[ID] += 1
        sender("KO", sock, ID)
    elif State_ADVANCE == [5, 5] or (
        State_ADVANCE[not ID] == 6 and State_ADVANCE[ID] == 5
    ):
        """a player want to go to next level"""
        State_ADVANCE[ID] += 1
        sender("OG", sock, ID)

    elif State_ADVANCE == [6, 6]:
        State_ADVANCE = [0, 0]
        RML("Call to next Level")
        next_level()


"""End"""


"""Simulation Operations"""


def Event_handler():
    global user_text
    events = pygame.event.get()
    if events:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Quit()
                    serverSocket.shutdown(socket.SHUT_RDWR)
                    serverSocket.close()
                elif event.key == pygame.K_RETURN:
                    try:
                        exec(user_text)
                        user_text = ""
                    except:
                        pass
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.unicode == "`":
                    exec('log_surface.fill(white);global y;y=50;RML("Server Logs :")')
                elif event.unicode == "~":
                    restart()

                else:
                    user_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONUP:
                pass
            elif event.type == pygame.QUIT:
                Quit()
        del events
    pygame.draw.rect(display_surface, black, (50, 1010, 1820, 60), 4)
    User_surface = NixieOne.render(user_text, True, red)
    display_surface.blit(User_surface, (70, 1020))


def restart():
    global index, threads, connections, level_number, running
    for connection in connections:
        connection.shutdown(socket.SHUT_RDWR)
        connection.close()
    running = [0, 0]
    threads.clear()
    connections.clear()
    level_number = 0
    next_level()
    connection_accept_thread = threading.Thread(target=accept_connections)
    connection_accept_thread.start()


def Quit():
    pygame.quit()
    sys.exit()


def set_matrix(x, y, w, h, matrix, color=(0, 255, 255, 100)):
    size = 50
    for i in range(h):
        for j in range(w):
            matrix[i][j] = pygame.Rect((x + j) * size, (y + i) * size, size, size)
            pygame.draw.rect(
                cell_surface,
                color,
                ((x + j) * size, (y + i) * size, size - 3, size - 3),
                border_radius=10,
            )


def writer(matrix, matrix_pos):
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            text = Courier_xsmall.render(str(cell), True, black)
            text_rect = text.get_rect()
            text_rect.center = matrix_pos[i][j].center
            display_surface.blit(text, text_rect)


def show_stats():
    temp = []
    temp.append(
        Courier_small.render(
            "position : " + str(players[0].data["player"]), True, black
        )
    )
    temp.append(Courier_small.render("HP : " + str(players[0].data["HP"]), True, black))
    temp.append(
        Courier_small.render("Took : " + str(players[0].data["took"]), True, black)
    )
    temp.append(
        Courier_small.render(
            "OP_position : " + str(players[0].data["opponent"]), True, black
        )
    )
    temp.append(
        Courier_small.render(
            "OP_HP : " + str(players[0].data["opponent_HP"]), True, black
        )
    )
    temp.append(
        Courier_small.render(
            "OP_Took : " + str(players[0].data["opponent_took"]), True, black
        )
    )
    for i, word in enumerate(temp):
        display_surface.blit(word, (300 * i + 200, 5))

    temp.clear()
    temp.append(
        Courier_small.render(
            "position : " + str(players[1].data["player"]), True, (150, 10, 10)
        )
    )
    temp.append(
        Courier_small.render("HP : " + str(players[1].data["HP"]), True, (150, 10, 10))
    )
    temp.append(
        Courier_small.render(
            "Took : " + str(players[1].data["took"]), True, (150, 10, 10)
        )
    )
    temp.append(
        Courier_small.render(
            "OP_position : " + str(players[1].data["opponent"]), True, (150, 10, 10)
        )
    )
    temp.append(
        Courier_small.render(
            "OP_HP : " + str(players[1].data["opponent_HP"]), True, (150, 10, 10)
        )
    )
    temp.append(
        Courier_small.render(
            "OP_Took : " + str(players[1].data["opponent_took"]), True, (150, 10, 10)
        )
    )
    for i, word in enumerate(temp):
        display_surface.blit(word, (300 * i + 200, 20))


def RML(text, fsize=25, font=NixieOne_small, color=(40, 0, 40, 255)):
    global x, y, level_number
    with open(f"log_file_{level_number}.txt", "a") as log_file:
        log_file.write(text + "\n")
    lines = text.splitlines()
    for i, l in enumerate(lines):
        # print(l)
        y += fsize * i
        log_surface.blit(font.render(l, True, color), (x, y))
    y += fsize


def next_level():
    global server_1_pos, server_2_pos, w, h, level_number, players, player_0, player_1, on_hold
    on_hold = 1
    if level_number == 5:
        level_number = 0
    level_size = [(10, 5), (12, 7), (16, 7), (18, 7), (18, 9)]
    w, h = level_size[level_number]
    players.clear()
    players = [Game_World("A", w, h), Game_World("B", w, h)]
    server_1_pos.clear()
    server_2_pos.clear()
    server_1_pos = [[[] for i in range(w)] for i in range(h)]
    server_2_pos = [[[] for i in range(w)] for i in range(h)]
    surface.fill(white)
    cell_surface.fill(white)
    set_matrix(1, 1, w, h, server_1_pos)
    set_matrix(1, 11, w, h, server_2_pos, (255, 20, 20, 100))
    surface.blit(cell_surface, (0, 0))
    surface.blit(Goldie_small.render("Player_1", True, black), (50, 10))
    surface.blit(Goldie_small.render("Player_2", True, black), (50, 510))
    level_number += 1
    exec("log_surface.fill(white);global y;y=50")
    with open(f"log_file_{level_number}.txt", "w"):
        pass
    RML(f"Level : {level_number}\n\n")
    RML(
        "Server Logs:\n"
        + socket.gethostname()
        + " is now running as "
        + socket.gethostbyname(socket.gethostname())
        + " on port "
        + str(port)
    )
    on_hold = 0


"""END"""


"""connection assignment"""
index = 0
port = 2300
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((socket.gethostname(), port))
serverSocket.listen(2)
connections = []
threads = []
running = [0, 0]
connection_accept_thread = threading.Thread(target=accept_connections)
connection_accept_thread.start()
"""END"""

"""game variable assignment"""
fps = FPS()
w, h = 10, 5
x, y = 10, 50
user_text = ""
players = []
player_0 = None
player_1 = None
move = {"up": [-1, 0], "down": [1, 0], "left": [0, -1], "right": [0, 1]}
State_ADVANCE = [0, 0]
level_number = 0
"""END"""

""" To display level cell on server screen """
cell_surface = pygame.Surface((1920, 1080), pygame.SRCALPHA)
surface = pygame.Surface((1920, 1080))
server_1_pos = []
server_2_pos = []
surface.fill(white)
log_surface = pygame.Surface((920, 1080))
log_surface.fill(white)
next_level()
"""END"""


on_hold = 0
while True:
    """ To run server display,show matrices and logs"""
    display_surface.fill(white)
    display_surface.blit(surface, (0, 0))
    display_surface.blit(log_surface, (1000, 0))
    if not on_hold:
        show_stats()
        writer(players[0].data["matrix"], server_1_pos)
        writer(players[1].data["matrix"], server_2_pos)
    """END"""

    fps.show(display_surface)
    Event_handler()
    pygame.display.update()
    # clock.tick(60)
