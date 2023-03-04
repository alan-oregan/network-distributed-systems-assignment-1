# Echo client program
import socket

HOST = '127.0.0.1'    # The remote host
PORT = 50007          # The same port as used by the server


while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    text = input("Command>")

    s.sendall((text).encode())

    # receives 80000
    data = s.recv(80000)

    if text == "<EXIT>":
        s.close()
        break

    if "<GET-" in text:
        filename = text.split("-")[1][:-1]
        filenameSplit = filename.split(".")

        with open(f"{filenameSplit[0]}.rec.{filenameSplit[1]}", "wb+") as f:
            f.write(data)
        print(f"added data to {filenameSplit[0]}.rec.{filenameSplit[1]}")

    if "<HASH-" in text:
        print(data.hex())

    s.close()
