# Echo client program
import socket

HOST = '127.0.0.1'    # The remote host
PORT = 50007          # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    text = input("Command>")

    s.sendall((text).encode())

    # receives 80KB
    if len(text) > 0:
        data = s.recv(80000)

    # handle response

    # handle exit
    if text == "<EXIT>":
        break

    # if error then parse error text
    if "[ERROR]" in data.decode("UTF-8"):
        try:
            print(data.decode("UTF-8").split(":")[1][:-1])
        except (IndexError):
            print(data.decode("UTF-8"))
        finally:
            continue

    # handling successful response depending on request
    if "<GET-" in text:
        filename = text.split("-")[1][:-1]

        with open(filename, "wb+") as f:
            f.write(data)
        print(f"added data to {filename}")

    if "<HASH-" in text:
        print(data.hex())

    if "<LIST-" in text:
        print(data.decode("UTF-8"))

    if data == "<EXIT>":
        break

s.close()

input("Connection closed...")
