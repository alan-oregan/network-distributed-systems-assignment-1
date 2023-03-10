#publicly available docker image "python" on docker hub will be pulled
FROM python

# Open the port for access
EXPOSE 50007

#copying server from local directory to container's folder
COPY server/server.py /home/server.py

#copying the file over
COPY server/public/britney.mp3 /home/public/britney.mp3

# set working directory
WORKDIR /home

#running s.py in container
CMD python server.py