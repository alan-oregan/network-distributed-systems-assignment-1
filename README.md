# network-distributed-systems-assignment-1

## Local

The bat file in the root directory will launch the server and a client in separate terminals

```ps
./run
```

## Docker

The docker file in the root directory will create an image that you can use to run the server

```ps
docker build -t server .
docker run --publish=50007:50007 server
```

## Server Commands

Here are the commands you can use from the client:

- <GET-{FILE PATH}>
  - This will return the file at the given filepath in bytes and save it to the clients directory
- <LIST-{DIRECTORY PATH}>
  - This will list the files inside the directory at the given directory path
- <HASH-{FILE PATH}>
  - This will return sha256 hash for the file at the given filepath
- <SPLIT-{FILE PATH}>
  - This will split the file at the given filepath by the set MAX_SEND_SIZE and return the directory of the saved files
- <DELETE-{FILE PATH}>
  - This will delete the file at the given filepath along with the directory of the split files if it exists
