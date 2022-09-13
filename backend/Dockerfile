# syntax=docker/dockerfile:1
FROM python:3.10
COPY .. ./personal_finance_tracker
WORKDIR /personal_finance_tracker
RUN pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:."
CMD ["python3","database/mongoDB/MongoDB_service.py"]