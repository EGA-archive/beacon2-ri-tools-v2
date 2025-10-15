FROM python:3.11-bullseye AS BUILD

ENV DEBIAN_FRONTEND noninteractive

WORKDIR /usr/src/app

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN apt-get update
#RUN apt-get upgrade -y
RUN apt-get install -y --no-install-recommends \
    ca-certificates pkg-config make \
    libssl-dev libffi-dev libpq-dev
RUN apt install vim -y
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install wheel setuptools pip --upgrade
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENTRYPOINT ["tail", "-f", "/dev/null"]