FROM python:3.14.6-alpine3.23

ENV TZ="America/New_York"

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "skywatch.py"]
