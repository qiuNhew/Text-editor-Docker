# editor-andcount

Counts the occurrences of the word "and" in the provided text.

Written in Python (Flask), listens on port 80.

## Endpoint

`GET /?text=<string>` returns JSON:

```json
{ "error": false, "message": "The text contains 3 'and's", "total_ands": 3 }
```

## Files

- `src/app.py` — Flask app; reads the `text` parameter, validates it, and returns the count.
- `src/andCount.py` — `count_and_occurrences()`; sanitises the text and counts whole-word "and" matches.
- `src/test.py` — Unit tests for the counting function.
- `src/integrationTest.py` — Integration tests against the running endpoint.
- `Dockerfile` — Builds the service image.
- `.gitlab-ci.yml` — Build and test pipeline.

## Run

```bash
docker build -t andcount .
docker run -p 8003:80 andcount
```
