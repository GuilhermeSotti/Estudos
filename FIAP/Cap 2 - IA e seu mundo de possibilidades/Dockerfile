FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=src/deploy_model.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]
