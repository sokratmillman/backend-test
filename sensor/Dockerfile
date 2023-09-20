FROM python:3.10

WORKDIR /sensor

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY sensor.py .

CMD ["python", "-u", "./sensor.py"]