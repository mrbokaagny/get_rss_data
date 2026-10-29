FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir \
    requests \
    beautifulsoup4 \
    lxml \
    pandas \
    psycopg2-binary \
    "psycopg[binary]" \
    sqlalchemy

RUN mkdir -p /data

COPY . /app/

CMD ["python", "main.py"]
