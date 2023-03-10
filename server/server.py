import socket
import threading

import command
import utility

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((utility.HOST, utility.PORT))

# This is the buffer string
# when input comes in from a client it is added
# into the buffer string to be relayed later
# to different clients that have connected
# Each message in the buffer is separated by a colon :
buffer = ""


def parseInput(request: str, conn: socket):

    # Checking for commands

    if "<GET-" in request:
        is_success, filename = utility.parseFilePath(conn, request)
        if is_success:
            fileBytes = command.get(filename)
            conn.send(fileBytes)
            utility.serverLog(f"Sent {filename} to Client")
        return

    if "<SPLIT-" in request:
        is_success, filename = utility.parseFilePath(conn, request)
        if is_success:
            splitFiles = command.split(filename)
            utility.clientEvent(conn,
                                f"Split {filename} into {splitFiles}"
                                )
        return

    if "<DELETE-" in request:
        is_success, filename = utility.parseFilePath(conn, request)

        if is_success:
            deletedFiles = command.delete(filename)
            utility.clientEvent(conn,
                                f"Deleted {deletedFiles}",
                                "Response"
                                )
        return

    if "<HASH-" in request:
        is_success, filename = utility.parseFilePath(conn, request)

        if is_success:
            hash = command.hash(filename)
            utility.clientEvent(conn,
                                f"The hash for {filename} is {hash}",
                                "Response"
                                )
        return

    if "<LIST-" in request:
        is_success, directory = utility.parseDirectoryPath(conn, request)
        if is_success:
            response = command.list(directory)
            utility.clientEvent(conn,
                                f"Files in directory {directory} are: \n{response}",
                                "Response"
                                )
        return

    # default response
    utility.clientEvent(conn, f"Unknown command {request}", "ERROR")


def manageConnection(conn: socket, addr):
    '''main function that runs on the thread and manages each connection'''

    utility.serverLog(f"Client Connected on port {addr[1]}", "connected")

    # continues the connection while client does not send <EXIT>
    request = ""
    while "<EXIT>" not in request:
        # receives the request and decodes it from bytes
        # to a UTF-8 string
        request = conn.recv(utility.MAX_RECEIVE_BYTES).decode("UTF-8")

        utility.serverLog(
            f"{request} from client on port {addr[1]}", "RECEIVED")

        parseInput(request, conn)

        if "<EXIT>" in request:
            conn.send(b'[END]')
            conn.close()

    # handles when a client disconnects
    utility.serverLog(
        f"Client disconnected from port {addr[1]}",
        "disconnected"
    )
    exit(1)


# log starting event message to server
utility.serverLog(
    f"Hi!, This is the server:) I'm listening on port {utility.PORT}",
    "started"
)

while True:
    # continuously listens for client connections
    s.listen(1)

    # accepts any connection and starts a thread to manage that connection
    conn, addr = s.accept()
    threading.Thread(target=manageConnection, args=(conn, addr)).start()
