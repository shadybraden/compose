FROM python:3.14-slim

# apply base-image security patches (glibc CVE-2026-5450, perl-base CVEs)
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN pip install flask
COPY app.py .
COPY templates/ templates/
EXPOSE 5000
CMD ["python", "app.py"]