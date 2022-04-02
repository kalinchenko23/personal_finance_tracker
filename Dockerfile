# syntax=docker/dockerfile:1
FROM python:3.10
WORKDIR /personal_finanse_tracker
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
#At this point, we have an image that is based on Python version 3.8 and we have installed our dependencies.
#The next step is to add our source code into the image.
COPY . ../new_app
CMD ["python3","time.slee(100000)"]