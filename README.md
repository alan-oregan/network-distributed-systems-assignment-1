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
