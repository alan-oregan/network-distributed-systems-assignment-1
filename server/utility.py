import time
import os
import socket

# =========== define utility constants ===========


HOST = '0.0.0.0'
PORT = 50007
MAX_RECEIVE_BYTES = 1024
MAX_SEND_BYTES = 80000
ENCODING = "UTF-8"


# =========== define utility methods ===========


def serverLog(message: str, type: str = "EVENT"):
    '''
    takes in a message and optionally its type and
    logs it to the server
    '''
    timestamp = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime())
    print(f"[{timestamp}] {type.upper():9} {message}")


def clientEvent(conn: socket, message: str, type: str = "EVENT"):
    '''
    takes in a message and optionally its type,
    logs it to the server returns bytes to be sent to the client
    '''
    serverLog(message, type)
    conn.send(bytes(f"[{type.upper()}] {message}", "UTF-8"))


def parseDirectoryPath(conn: socket, request):
    try:
        directoryPath = "./public/" + request.split("-")[1][:-1]
    except (IndexError):
        clientEvent(
            conn,
            "Invalid input please use structure <COMMAND-DIRPATH>", "Error"
        )

    exists = os.path.exists(directoryPath)

    if not exists:
        clientEvent(conn, f"Path '{directoryPath}' does not exist", "Error")

    return (exists, directoryPath)


def parseFilePath(conn: socket, request):
    try:
        filePath = "./public/" + request.split("-")[1][:-1]
    except (IndexError):
        clientEvent(
            conn,
            "Invalid input please use structure <COMMAND-FILEPATH>", "Error"
        )

    exists = os.path.isfile(filePath)

    if not exists:
        clientEvent(conn, f"File '{filePath}' does not exist", "Error")

    return (exists, filePath)
