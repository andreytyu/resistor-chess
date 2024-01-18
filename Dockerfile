FROM python:3.12.1
LABEL maintainer="Andrey Tyukavin <tyukavin.andreyy@gmail.com>"

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -y i2c-tools lsof

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
