# editor-vowelcount

Counts the number of vowels in the provided text.

Written in Python (Flask), listens on port 80.

## Endpoint

`GET /?text=<string>` returns JSON with the vowel count.

## Files

- `src/app.py` — Flask app; reads the `text` parameter, validates it, and returns the count.
- `src/vowelCount.py` — `count_vowels()`; counts vowels and returns per-vowel totals.
- `src/test.py` — Unit tests for the counting function.
- `src/integrationTest.py` — Integration tests against the running endpoint.
- `Dockerfile` — Builds the service image.
- `.gitlab-ci.yml` — Build and test pipeline.

## Run

```bash
docker build -t vowelcount .
docker run -p 8007:80 vowelcount
```
