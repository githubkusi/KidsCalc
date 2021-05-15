#FROM python:3.8-slim-buster
FROM python:buster
WORKDIR /src
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./src/calc.py .

CMD ["python3", "./calc.py"]
