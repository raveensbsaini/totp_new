FROM  python:latest
WORKDIR /usr/src/app 
COPY server/ /usr/src/app 
RUN apt update &&  pip3 install -r requirements.txt
CMD [ "fastapi","run","main.py" ]
