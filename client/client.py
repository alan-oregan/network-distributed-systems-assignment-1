import socket
import utility

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((utility.HOST, utility.PORT))

while True:
    text = input("Command>")

    s.sendall((text).encode())

    # receives 80KB
    if len(text) > 0:
        data = s.recv(utility.MAX_RECEIVE_BYTES)

    # handle response

    # handle exit
    if text == "<EXIT>":
        break

    # if error then parse error text
    try:
        if "[ERROR]" in data.decode(utility.ENCODING):
            try:
                print(data.decode(utility.ENCODING).split(":")[1][:-1])
            except (IndexError):
                print(data.decode(utility.ENCODING))
            finally:
                continue

    # if exception then not an error response
    except (UnicodeDecodeError):
        pass

    # handling successful response depending on request
    if "<GET-" in text:
        filename = text.split("-")[1][:-1]

        with open(filename, "wb+") as f:
            f.write(data)
        print(f"added data to {filename}")
        continue

    if "<HASH-" in text:
        print(data.hex())
        continue

    if "<LIST-" in text:
        print(data.decode(utility.ENCODING))
        continue

s.close()

input("Connection closed...")
