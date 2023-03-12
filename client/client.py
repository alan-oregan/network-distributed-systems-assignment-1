import socket
import utility

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((utility.HOST, utility.PORT))

while True:
    text = input("Command>")

    s.sendall((text).encode())

    # handle exit
    if text == "<EXIT>":
        break

    # receives 80KB
    if len(text) > 0:
        data = s.recv(utility.MAX_RECEIVE_BYTES)

    # handle response

    # if error then parse error text
    try:
        if "[ERROR]" in data.decode(utility.ENCODING):
            print(data.decode(utility.ENCODING))
            continue

    # ignore if data is not in text encoding
    except (UnicodeDecodeError):
        pass

    # handling successful response depending on request
    if "<GET-" in text:
        filename = text.split("-")[1][:-1]

        with open(filename, "wb+") as f:
            f.write(data)
        print(f"added data to {filename}")
        continue

    # if unknown format try to parse data as text
    try:
        print(data.decode(utility.ENCODING))

    # ignore if data is not in text encoding
    except (UnicodeDecodeError):
        pass

s.close()

input("Connection closed...")
