FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends cron \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# config.yaml and evidence/ should be mounted at runtime
RUN mkdir -p evidence/screenshots output/campaign

COPY deploy/cron-entry /etc/cron.d/stop-assholes
RUN chmod 0644 /etc/cron.d/stop-assholes && crontab /etc/cron.d/stop-assholes

CMD ["cron", "-f"]
