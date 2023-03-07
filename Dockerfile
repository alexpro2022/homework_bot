FROM python:3.7-slim
WORKDIR /app
# for local run uncomment below )))
# COPY .env . 
COPY homework.py .
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
CMD python homework.py
