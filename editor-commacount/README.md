# editor-commacount

Counts the number of commas in the provided text.

Written in Python (Flask), listens on port 80.

## Endpoint

`GET /?text=<string>` returns JSON with the comma count.

## Files

- `src/app.py` — Flask app; reads the `text` parameter, validates it, and returns the count.
- `src/commaCount.py` — `comma_counting()`; counts commas in the input.
- `src/test.py` — Unit tests for the counting function.
- `src/integrationTest.py` — Integration tests against the running endpoint.
- `Dockerfile` — Builds the service image.
- `.gitlab-ci.yml` — Build and test pipeline.

## Run

```bash
docker build -t commacount .
docker run -p 8005:80 commacount
```
