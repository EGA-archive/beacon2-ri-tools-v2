FROM python:3.11-bullseye

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    openssl \
    curl \
    pkg-config \
    make \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    vim \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

RUN sed -i 's/\r$//' /usr/local/bin/docker-entrypoint.sh && \
    chmod +x /usr/local/bin/docker-entrypoint.sh


RUN mkdir -p /opt/refgen-data && \
    rm -rf /usr/local/lib/python3.11/site-packages/refgenDetector/msgpacks && \
    ln -s /opt/refgen-data /usr/local/lib/python3.11/site-packages/refgenDetector/msgpacks

ENV REFGEN_DATA_DIR=/opt/refgen-data

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

CMD ["tail", "-f", "/dev/null"]