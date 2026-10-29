FROM python:3.13.18-bookworm

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /usr/src/app

# Install system dependencies and refresh the Debian CA certificates.
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
    && update-ca-certificates -f \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and certifi to the security-fixed minimum versions.
RUN python -m pip install --no-cache-dir --upgrade \
    "pip>=26.2.2" \
    "certifi>=2026.10.19" \
    setuptools \
    wheel

# Copy and install project dependencies.
COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt

# Verify security-critical versions and dependency compatibility.
RUN python -c "import pip, certifi; \
    from packaging.version import Version; \
    print('Python CA bundle:', certifi.where()); \
    print('pip version:', pip.__version__); \
    print('certifi version:', certifi.__version__); \
    assert Version(pip.__version__) >= Version('26.2.2'), \
        f'pip version too old: {pip.__version__}'; \
    assert Version(certifi.__version__) >= Version('2026.10.19'), \
        f'certifi version too old: {certifi.__version__}'" \
    && python -m pip check

# Copy application source.
COPY . .

# Configure the container entrypoint.
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

RUN sed -i 's/\r$//' /usr/local/bin/docker-entrypoint.sh && \
    chmod +x /usr/local/bin/docker-entrypoint.sh

# Store RefgenDetector data outside the Python package directory.
RUN mkdir -p /opt/refgen-data && \
    rm -rf /usr/local/lib/python3.13/site-packages/refgenDetector/msgpacks && \
    ln -s /opt/refgen-data /usr/local/lib/python3.13/site-packages/refgenDetector/msgpacks

ENV REFGEN_DATA_DIR=/opt/refgen-data

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

CMD ["tail", "-f", "/dev/null"]
