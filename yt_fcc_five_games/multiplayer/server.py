# https://youtu.be/XGf2GcyHPhc?t=19616
import socket
from _thread import *
import sys

server = "192.168.0.12"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# initialize server
try:
    s.bind((server, port))
except socket.error as e:
    print(e)

# open the port and expect connections
s.listen(2)
print("Waiting for a connection, Server Started")


def read_pos(str):
    # "decode" position string into tupple
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    # "enconde" position tupple into string
    return str(tup[0]) + "," + str(tup[1])


# starting positions
pos = [(0, 0), (150, 150)]


def threaded_client(conn, player):
    reply = ""
    # something like "async":
    # function runs in the background + don't need to wait for it to finish executing before running again

    # send the current player's position first time
    conn.send(str.encode(make_pos(pos[player])))

    while True:
        # continuously try to get information from the client
        try:
            # update the stored position for the player when they send it
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                # send the other player's position to the client so they can update their UI
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                print("Received: ", data)
                print("Sending: ", reply)

            conn.sendall(str.encode(make_pos(reply)))
        except:
            break

    print("Lost connection")
    conn.close()


current_player = 0

while True:
    # continuously wait for connections
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1
