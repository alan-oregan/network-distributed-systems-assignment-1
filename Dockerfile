#publicly available docker image "python" on docker hub will be pulled
FROM python

# Open the port for access
EXPOSE 50007

#copying server python files from local directory to container's folder
COPY server/utility.py /home/utility.py
COPY server/command.py /home/command.py
COPY server/server.py /home/server.py

#copying the music file over
COPY server/public/britney.mp3 /home/public/britney.mp3

# set working directory
WORKDIR /home

#running s.py in container
CMD python server.py