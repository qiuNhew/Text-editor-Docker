# editor-monitoring

Monitors the health and accuracy of the counting services. On a fixed interval it sends generated test text to each backend, compares the returned count against the expected value, records status and response times, sends an email alert when a service is down or inaccurate, and serves a dashboard.

Written in Python (Flask), listens on port 80.

## Endpoints

| Method | Path          | Description                                  |
| ------ | ------------- | -------------------------------------------- |
| GET    | `/`           | Monitoring dashboard                         |
| GET    | `/api/status` | Current service status and performance data  |

## Files

- `src/app.py` — Flask monitoring service. Runs the periodic polling loop, calculates expected counts, stores status and response-time history, sends email alerts, and serves the dashboard and status API.
- `src/config.json` — Maps each service name to the URL the monitor should poll.
- `src/templates/index.html` — The dashboard showing per-service status cards and a response-time chart.
- `Dockerfile` — Builds the monitoring service image.

## Email alerts (configuration)

Alert credentials are read from environment variables — nothing is hardcoded.
Set these (e.g. in the root `.env`, consumed by `docker-compose`):

| Variable          | Description                                            |
| ----------------- | ------------------------------------------------------ |
| `SMTP_SERVER`     | SMTP host (default `smtp.gmail.com`)                   |
| `SMTP_PORT`       | SMTP port (default `587`)                              |
| `SENDER_EMAIL`    | Account that sends alerts                              |
| `SENDER_PASSWORD` | App password for the sender (Gmail: an *App Password*) |
| `RECIPIENT_EMAIL` | Where alerts are delivered (defaults to sender)        |

If `SENDER_EMAIL` / `SENDER_PASSWORD` / `RECIPIENT_EMAIL` are unset, email
alerts are skipped (monitoring still runs). See `.env.example` in the repo root.

## Run

```bash
docker build -t monitoring .
docker run -p 8009:80 \
  -e SENDER_EMAIL=you@example.com \
  -e SENDER_PASSWORD=your_app_password \
  -e RECIPIENT_EMAIL=you@example.com \
  monitoring
```

Or via `docker-compose` from the repo root (reads the root `.env`):

```bash
docker compose up monitor
```
