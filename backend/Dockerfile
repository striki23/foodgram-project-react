FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY foodgram/ .

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0.0.0.0:8000" ]
