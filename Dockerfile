FROM python:3.10-alpine

WORKDIR /usr/src/app

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN apk add --no-cache gcc musl-dev linux-headers
COPY . .
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["tail", "-f", "/dev/null"]