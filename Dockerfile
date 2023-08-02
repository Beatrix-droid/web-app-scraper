FROM python:3.8-slim-buster  
# base parent image with which we will add other layers of our appplication

COPY ./static /app/
COPY  ./templates /app/
COPY image_scraper.py  /app/
COPY main.py  /app/
COPY  requirements.txt  /app/ 
# take files from our local computer and copy them into the container. The app folder in the container MUST have a trailing slash. That way
# docker knows to create that folder in the container if it does not exist yet.

WORKDIR /app
#change directory in the container

RUN pip install -r requirements.txt
# install the requirements for this app
RUN export FLASK_APP=main

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
# start appliction  [executable, parameter1, parameter2, etc]