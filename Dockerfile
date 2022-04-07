# syntax=docker/dockerfile:1
FROM python:3.10
COPY . .
RUN pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:."
CMD ["python3","plaid_service/plaid_dashboard.py"]