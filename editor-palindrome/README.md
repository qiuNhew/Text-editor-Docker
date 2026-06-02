# editor-palindrome

Counts the number of word-palindromes in the provided text.

Written in Python (Flask), listens on port 80.

## Endpoint

`GET /?text=<string>` returns JSON with the palindrome count.

## Files

- `src/app.py` — Flask app; reads the `text` parameter, validates it, and returns the count.
- `src/palindromeCount.py` — `count_palindromes()`; splits the text into words and counts those that read the same backwards.
- `src/test.py` — Unit tests for the counting function.
- `src/integrationTest.py` — Integration tests against the running endpoint.
- `Dockerfile` — Builds the service image.
- `.gitlab-ci.yml` — Build and test pipeline.

## Run

```bash
docker build -t palindromecount .
docker run -p 8006:80 palindromecount
```
