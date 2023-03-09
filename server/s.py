import socket
import threading
import hashlib
import os
import time

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


# ================= command functions =================

def sendFile(filename: str):
    with open(filename, "rb") as f:
        conn.send(f.read())


def splitFile(filename: str):
    filenameSplit = filename.split(".")

    with open(filename, mode="rb") as file:
        contents = file.read()
        chunkSize = 80000
        numOfSegments = int(len(contents)/chunkSize)

        os.makedirs(os.path.dirname(f"{filenameSplit[0]}/"), exist_ok=True)
        for i in range(1, numOfSegments+1):
            f = open(f"{filenameSplit[0]}/{i}.{filenameSplit[1]}", 'wb+')

            if (i != numOfSegments):
                f.write(contents[chunkSize*i - chunkSize: chunkSize*i])
            else:
                f.write(contents[chunkSize*i - chunkSize:])
            f.close()


def sendHash(filename: str):
    with open(filename, 'rb') as f:
        content = f.read()

    m = hashlib.sha256()
    m.update(content)
    conn.send(m.digest())
    return m.hexdigest()

# ================= util functions =================


def logEvent(message: str, type: str = "EVENT"):
    timestamp = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime())
    print(f"[{timestamp} {type.upper()}] {message}".rjust(2))


def raiseError(message: str, type: str = "ERROR"):
    logEvent(message, type)
    conn.send(bytes(f"[{type}]:{message}", "UTF-8"))


def parseFilename(data):
    try:
        filename = data.split("-")[1][:-1]
        return (True, filename)
    except (IndexError):
        raiseError(
            "Invalid filename please use structure <COMMAND-FILENAME.EXTENSION>"
        )
        return (False, "")


# sample parser function. The job of this function is to take some input
# data and search to see if a command is present in the text. If it finds a
# command it will then need to extract the command.
def parseInput(data, conn):
    data = data

    # Checking for commands
    if "<GET-" in data:
        is_success, filename = parseFilename(data)
        if is_success:
            try:
                sendFile(filename)
                logEvent(f"Sent {filename} to client")
            except (FileNotFoundError):
                raiseError(f"File '{filename}'does not exist")

    if "<SPLIT-" in data:
        is_success, filename = parseFilename(data)

        if is_success:
            splitFile(filename)

    if "<DELETE-" in data:
        is_success, filename = parseFilename(data)

        if is_success:
            filenameSplit = filename.split(".")
            for i in range(1, 11):
                try:
                    os.remove(f"{filenameSplit[0]}/{i}.{filenameSplit[1]}")
                except (FileNotFoundError):
                    pass
            try:
                os.rmdir(f"{filenameSplit[0]}/")
            except (FileExistsError, FileNotFoundError):
                pass

    if "<HASH-" in data:
        is_success, filename = parseFilename(data)

        if is_success:
            hash = sendHash(filename)
            logEvent(f"Sent the file hash for {filename}:{hash}")

    if "<LIST-" in data:
        is_success, directory = parseFilename(data)
        directory = "./" + directory + "/"
        dir = os.scandir(directory)
        conn.send(
            bytes(
                " ".join([entry.name for entry in dir if entry.is_file()]),
                "UTF-8"
            )
        )

        logEvent(f"sent the directory list for {directory}")


# we a new thread is started from an incoming connection
# the manageConnection function is used to take the input
# and print it out on the server
# the data that came in from a client is added to the buffer.

def manageConnection(conn, addr):
    logEvent(f"Client Connected on port {addr[1]}", "connected")

    data = ""
    while "<EXIT>" not in data:
        data = conn.recv(1024).decode("UTF-8")

        logEvent(data, "RECEIVED")

        parseInput(data, conn)

        conn.send(b' ')

        if "<EXIT>" in data:
            conn.send(b'[END]')
            conn.close()

    logEvent(f"Client disconnected from port {addr[1]}", "disconnected")
    exit(1)


logEvent("Hi!, This is the server :)", "started")
while True:
    s.listen(1)
    conn, addr = s.accept()
    # after we have listened and accepted a connection coming in,
    # we will then create a thread for that incoming connection.
    # this will prevent us from blocking the listening process
    # which would prevent further incoming connections
    t = threading.Thread(target=manageConnection, args=(conn, addr))

    t.start()
