FROM python:3.7-slim
WORKDIR /app
COPY Dockerfile .
# COPY .env .
COPY homework.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["python3", "homework.py"]