import time
import os

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
    print(f"[{timestamp} {type.upper()}] {message}".rjust(2))


def clientEvent(message: str, type: str = "EVENT"):
    '''
    takes in a message and optionally its type,
    logs it to the server returns bytes to be sent to the client
    '''
    serverLog(message, type)
    return bytes(f"[{type}]:{message}", "UTF-8")


def parsePath(request):
    try:
        path = "./public/" + request.split("-")[1][:-1]
    except (IndexError):
        clientEvent(
            "Invalid input please use structure <COMMAND-PATH>", "Error"
        )

    exists = os.path.exists(path)

    if not exists:
        clientEvent(f"Path '{path}' does not exist", "Error")

    return (exists, path)
