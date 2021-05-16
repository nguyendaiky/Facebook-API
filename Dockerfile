# Dockerfile, Image, Container

FROM python:3.8

ADD main.py .

COPY requirements.txt .
COPY main.py . 

RUN pip install --no-cache-dir -r requirements.txt 

CMD ["python","./main.py"]