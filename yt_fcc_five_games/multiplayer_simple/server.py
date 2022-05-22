import pickle
import socket
from _thread import *
import sys
from player import Player

GREEN = (0, 255, 0)
GREY = (128, 128, 128)

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


# keep players on the server
players = [Player(0, 0, 50, 50, GREY), Player(150, 0, 50, 50, GREEN)]


def threaded_client(conn, player):
    # something like "async":
    # function runs in the background + don't need to wait for it to finish executing before running again

    # send the current player first time
    conn.send(pickle.dumps(players[player]))

    reply = ""

    while True:
        # continuously try to get information from the client
        try:
            # update the stored player obj for the player when they send it
            data = pickle.loads(conn.recv(2048*4))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                # send the other player's position to the client so they can update their UI
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print("Received: ", data)
                print("Sending: ", reply)

            conn.sendall(pickle.dumps(reply))
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
