# syntax=docker/dockerfile:1
FROM python:3.10
COPY . .
RUN pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:."
CMD ["python3","database/mongoDB/MongoDB_service.py"]