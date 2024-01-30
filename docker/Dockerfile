FROM python:3.12.1-slim-bookworm

WORKDIR /mentorship_program_project

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONNUNBUFFERED=1

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y netcat-openbsd

COPY ./docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ../ .

ENTRYPOINT ["/entrypoint.sh"]
