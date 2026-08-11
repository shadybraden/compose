FROM python:3.14.7-alpine3.23

ENV TZ="America/New_York"

WORKDIR /app

COPY skywatch/. /app

RUN pip install --no-cache-dir -r skywatch/requirements.txt

CMD ["python3", "skywatch/skywatch.py"]
