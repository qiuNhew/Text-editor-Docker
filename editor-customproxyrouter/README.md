# editor-customproxyrouter

The reverse proxy / API gateway for the editor. Routes incoming `/<service>` requests to the matching backend container and provides admin routes to manage the routing table at runtime.

Written in Python (Flask), listens on port 80.

## Endpoints

| Method   | Path                    | Description                              |
| -------- | ----------------------- | ---------------------------------------- |
| GET      | `/`                     | Health check                             |
| GET/POST | `/<service>`            | Forward the request to a registered backend |
| GET      | `/admin/endpoints`      | List registered endpoints                |
| POST     | `/admin/register`       | Register `{name, url}`                   |
| POST     | `/admin/remove`         | Remove `{name}`                          |
| POST     | `/admin/update-service` | Pull an image and (re)deploy a container |

## Files

- `src/app.py` — Flask reverse proxy. Loads the routing table, forwards requests (method, headers, query string, body) to the target service, and exposes the health check and admin routes.
- `src/config.json` — The initial routing table mapping each service name to its internal URL.
- `requirements.txt` — Python dependencies (Flask, requests, Werkzeug, docker).
- `Dockerfile` — Builds the proxy image and installs the Docker CLI.

## Run

```bash
docker build -t customproxyrouter .
docker run -p 8000:80 customproxyrouter
```
