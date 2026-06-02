# QUBeditotron3000 — Cloud Microservices Text Editor

CSC3065 — Cloud Computing Assignment (40412457)

A containerised, microservices-based web text editor. A browser frontend sends text to a set of independent counting services through a custom reverse-proxy / API gateway. A monitoring service polls each backend for health and accuracy, and document persistence is handled by Google Firestore.

## Architecture

```
                          +-----------------------------+
   Browser  ----------->  |  editor-frontend  (:3000)   |  -- Firestore (save/load text)
                          +--------------+--------------+
                                         |  HTTP /<service>?text=...
                                         v
                          +-----------------------------+
                          | reverse-proxy / API gateway |
                          |   customproxyrouter (:8000) |
                          +--------------+--------------+
            +--------------+-------------+-------------+--------------+
            v              v             v             v              v
        wordcount     charcount     andcount     commacount    palindrome / vowel
         (PHP)        (Node.js)     (Python)      (Python)        (Python)

                          +-----------------------------+
                          |   monitoring  (:8009)       |  polls each service + email alerts
                          +-----------------------------+

   All services share the editor-network Docker bridge network.
```

## Services

| Service                     | Directory                  | Stack             | Host Port |
| --------------------------- | -------------------------- | ----------------- | --------- |
| Frontend                    | `editor-frontend`          | Static HTML + JS  | 3000      |
| Reverse Proxy / API Gateway | `editor-customproxyrouter` | Python / Flask    | 8000      |
| Word Count                  | `editor-wordcount`         | PHP 7.2 / Apache  | 8008      |
| Character Count             | `editor-charcount`         | Node.js / Express | 8004      |
| And Count                   | `editor-andcount`          | Python / Flask    | 8003      |
| Comma Count                 | `editor-commacount`        | Python / Flask    | 8005      |
| Palindrome Count            | `editor-palindrome`        | Python / Flask    | 8006      |
| Vowel Count                 | `editor-vowelcount`        | Python / Flask    | 8007      |
| Monitoring                  | `editor-monitoring`        | Python / Flask    | 8009      |

## What Each File Does

### Top level

- **docker-compose.yml** — Orchestrates all nine containers, assigns host ports, and connects every service to the shared `editor-network` bridge network.

### editor-frontend

- **src/index.html** — The QUBeditotron3000 user interface. Provides the text area and buttons, calls each counting service through the reverse proxy, and saves/loads text to Google Firestore using the embedded Firebase config.
- **src/config.json** — Maps service names to their base URLs.
- **Dockerfile** — Serves the static frontend.

### editor-customproxyrouter (Reverse Proxy / API Gateway)

- **src/app.py** — Flask reverse proxy. Forwards `/<service>` requests to the matching backend, exposes a health check, and provides admin routes to list, register, remove, and redeploy service endpoints.
- **src/config.json** — The initial routing table mapping each service name to its internal URL.
- **requirements.txt** — Python dependencies (Flask, requests, Werkzeug, docker).
- **Dockerfile** — Builds the proxy image and installs the Docker CLI.

### editor-wordcount (PHP)

- **src/index.php** — HTTP entry point. Reads the `text` parameter, validates it, and returns the word count as JSON.
- **src/functions.inc.php** — `wordcount()` and `validate_input()` helpers that normalise whitespace and count words.
- **src/test.php** / **src/integrationTest.php** — Unit and integration tests.
- **Dockerfile** — Serves the PHP app on Apache.

### editor-charcount (Node.js)

- **server.js** — Express server exposing `GET /?text=...`; validates input and returns the character count.
- **charcount.js** — `counter()` and `validate()` functions; strips whitespace and counts the remaining characters.
- **package.json** — Dependencies and test scripts.
- **test/test-charcount.js** / **test/integrationTest.js** — Mocha/Chai unit and integration tests.
- **Dockerfile** — Builds the Node.js service.

### editor-andcount (Python)

- **src/app.py** — Flask app exposing `GET/POST /`; returns the number of occurrences of the word "and".
- **src/andCount.py** — `count_and_occurrences()`; sanitises text and counts whole-word "and" matches.
- **src/test.py** / **src/integrationTest.py** — Unit and integration tests.
- **Dockerfile** — Builds the Python service.

### editor-commacount (Python)

- **src/app.py** — Flask app exposing the comma-count endpoint.
- **src/commaCount.py** — `comma_counting()`; counts commas in the input.
- **src/test.py** / **src/integrationTest.py** — Unit and integration tests.
- **Dockerfile** — Builds the Python service.

### editor-palindrome (Python)

- **src/app.py** — Flask app exposing the palindrome-count endpoint.
- **src/palindromeCount.py** — `count_palindromes()`; splits text into words and counts word-palindromes.
- **src/test.py** / **src/integrationTest.py** — Unit and integration tests.
- **Dockerfile** — Builds the Python service.

### editor-vowelcount (Python)

- **src/app.py** — Flask app exposing the vowel-count endpoint.
- **src/vowelCount.py** — `count_vowels()`; counts vowels and returns per-vowel totals.
- **src/test.py** / **src/integrationTest.py** — Unit and integration tests.
- **Dockerfile** — Builds the Python service.

### editor-monitoring (Python)

- **src/app.py** — Flask monitoring service. Periodically calls each backend with generated test text, compares results against expected values, records status and response times, sends email alerts on failure, and serves a dashboard.
- **src/config.json** — Maps each service name to the URL the monitor should poll.
- **src/templates/index.html** — The monitoring dashboard, showing per-service status cards and a response-time chart.
- **Dockerfile** — Builds the monitoring service.

## API

Each counting service exposes a single `GET /?text=<string>` endpoint that returns JSON, for example:

```json
{ "error": false, "string": "Contains 5 words", "answer": 5, "message": "" }
```

The reverse proxy routes requests as follows:

| Method   | Path                    | Description                              |
| -------- | ----------------------- | ---------------------------------------- |
| GET      | `/`                     | Health check                             |
| GET/POST | `/<service>`            | Proxy to a registered backend            |
| GET      | `/admin/endpoints`      | List registered endpoints                |
| POST     | `/admin/register`       | Register `{name, url}`                   |
| POST     | `/admin/remove`         | Remove `{name}`                          |
| POST     | `/admin/update-service` | Pull an image and (re)deploy a container |

## Prerequisites

- Docker and Docker Compose
- (Optional) a Google Firebase project with Firestore enabled, for the save/load feature

## Running

```bash
# from the repository root
docker compose up --build
```

Open the editor at http://localhost:3000. The proxy is reachable at http://localhost:8000 and the monitoring dashboard at http://localhost:8009.

To stop and clean up:

```bash
docker compose down
```

## Testing

Python services use `unittest`, charcount uses Mocha/Chai, and wordcount uses PHP test scripts. Each service also has a `.gitlab-ci.yml` pipeline that builds the image, runs unit and integration tests, then tears down.

```bash
# Python services
python3 -m unittest test.py
python3 -m unittest integrationTest.py

# charcount
npm test
```

## Repository Layout

```
.
├── docker-compose.yml          # Orchestrates all services on editor-network
├── editor-frontend/            # Browser UI + Firebase Firestore integration
├── editor-customproxyrouter/   # Flask reverse proxy / API gateway
├── editor-monitoring/          # Flask health + accuracy monitor
├── editor-wordcount/           # PHP word counter
├── editor-charcount/           # Node.js character counter
├── editor-andcount/            # Python "and" counter
├── editor-commacount/          # Python comma counter
├── editor-palindrome/          # Python palindrome counter
└── editor-vowelcount/          # Python vowel counter
```
