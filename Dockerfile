FROM python:3-alpine3.15
WORKDIR /demo-docker
COPY . /demo-docker
EXPOSE 5000 
CMD python3 ./backend.py
