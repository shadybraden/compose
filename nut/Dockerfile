FROM python:3.13-slim

ENV TZ="America/New_York"

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "nut.sh"]
