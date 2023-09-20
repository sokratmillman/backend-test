FROM python:3.10

WORKDIR /controller

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY utils.py .

COPY controller.py .

RUN mkdir volume && \
    touch volume/history.txt

CMD ["python", "-u", "./controller.py"]

EXPOSE 5000