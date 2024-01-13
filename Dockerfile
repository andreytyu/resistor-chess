FROM python:3.12.1
LABEL maintainer="Andrey Tyukavin <tyukavin.andreyy@gmail.com>"

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]