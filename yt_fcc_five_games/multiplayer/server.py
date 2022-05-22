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

# something like "async":
# runs in the background + don't need to wait for it to finish executing before running again


def threaded_client(conn):
    conn.send(str.encode("√ Connected"))
    reply = ""
    while True:
        try:
            # continuously try to get information from the client
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", reply)
                print("Sending: ", reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()


while True:
    # continuously wait for connections
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,))
