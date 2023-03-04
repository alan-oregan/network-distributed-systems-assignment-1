import socket
import threading
import hashlib
import os

print("Hi!, This is the server :)")

# from time import gmtime, strftime
# import time

HOST = '0.0.0.0'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

# This is the buffer string
# when input comes in from a client it is added
# into the buffer string to be relayed later
# to different clients that have connected
# Each message in the buffer is separated by a colon :
buffer = ""


# custom say hello command

def sayHello():
    print("----> The hello function was called")


# sample parser function. The job of this function is to take some input
# data and search to see if a command is present in the text. If it finds a
# command it will then need to extract the command.

def parseInput(data, conn):
    global exit

    data = str(data)

    if "<EXIT>" in data:
        conn.close()
        exit(1)

    # Checking for commands
    if "<GET-" in data:
        filename = data.split("-")[1][:-2]
        with open(filename, "rb") as f:
            conn.send(f.read())

        print("sent the file")

    if "<SPLIT-" in data:
        filename = data.split("-")[1][:-2]
        filenameSplit = filename.split(".")

        with open(filename, mode="rb") as file:
            contents = file.read()
            chunkSize = 100000
            numOfSegments = int(contents/chunkSize)

            os.makedirs(os.path.dirname(f"{filenameSplit[0]}/"), exist_ok=True)
            for i in range(1, numOfSegments+1):
                f = open(f"{filenameSplit[0]}/{i}.{filenameSplit[1]}", 'wb+')
                if (i != numOfSegments):
                    f.write(contents[chunkSize*i - chunkSize: chunkSize*i])
                else:
                    f.write(contents[chunkSize*i - chunkSize:])
                f.close()

    if "<DEL-" in data:
        filename = data.split("-")[1][:-2]
        filenameSplit = filename.split(".")
        for i in range(1, 11):
            try:
                os.remove(f"{filenameSplit[0]}/{i}.{filenameSplit[1]}")
            except (FileNotFoundError):
                pass
        try:
            os.rmdir(f"{filenameSplit[0]}/")
        except (FileExistsError):
            pass

    if "<HASH-" in data:
        filename = data.split("-")[1][:-2]

        with open(filename, 'rb') as f:
            content = f.read()

        m = hashlib.sha256()

        # get the hash

        m.update(content)
        res = m.digest()

        print(res)
        conn.send(res)

        print("sent the hash for '"+filename+"' :" + m.hexdigest())


# we a new thread is started from an incoming connection
# the manageConnection funnction is used to take the input
# and print it out on the server
# the data that came in from a client is added to the buffer.

def manageConnection(conn, addr):
    global buffer
    print('Connected by', addr)

    data = conn.recv(1024)

    parseInput(str(data), conn)  # Calling the parser, passing the connection

    print("rec:" + str(data))
    buffer += str(data)


while True:
    s.listen(1)
    conn, addr = s.accept()
    # after we have listened and accepted a connection coming in,
    # we will then create a thread for that incoming connection.
    # this will prevent us from blocking the listening process
    # which would prevent further incoming connections
    t = threading.Thread(target=manageConnection, args=(conn, addr))

    t.start()
