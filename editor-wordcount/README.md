# editor-wordcount

Counts the number of words in the provided text.

Written in PHP (Apache), listens on port 80.

## Endpoint

`GET /?text=<string>` returns JSON:

```json
{ "error": false, "string": "Contains 5 words", "answer": 5, "message": "" }
```

## Files

- `src/index.php` — HTTP entry point; reads the `text` parameter, validates it, and returns the word count.
- `src/functions.inc.php` — `wordcount()` and `validate_input()`; normalises whitespace and counts words.
- `src/test.php` — Unit tests for the counting function.
- `src/integrationTest.php` — Integration tests against the running endpoint.
- `Dockerfile` — Builds the service image (PHP on Apache).
- `.gitlab-ci.yml` — Build and test pipeline.

## Run

```bash
docker build -t wordcount .
docker run -p 8008:80 wordcount
```
