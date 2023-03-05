FROM python:3.7-slim
WORKDIR /app
# for local uncomment below )))
# COPY .env . 
COPY homework.py .
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
CMD ["python3", "homework.py"]