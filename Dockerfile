FROM python:3
WORKDIR /plaid_two
#before we can run pip install we need to get our requirements.txt file into our image
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
#At this point, we have an image that is based on Python version 3.8 and we have installed our dependencies.
#The next step is to add our source code into the image.
COPY . .
CMD ["python", "plaid_service/plaid_dashboard.py"]
