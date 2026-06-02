# editor-charcount

Counts the number of non-whitespace characters in the provided text.

Written in Node.js (Express), listens on port 80.

## Endpoint

`GET /?text=<string>` returns JSON:

```json
{ "error": false, "string": "Contains 12 characters", "answer": 12, "message": "" }
```

## Files

- `server.js` — Express server; reads the `text` query parameter, validates it, and returns the count.
- `charcount.js` — `counter()` and `validate()`; strips whitespace and counts the remaining characters.
- `package.json` — Dependencies and test scripts.
- `test/test-charcount.js` — Mocha/Chai unit tests.
- `test/integrationTest.js` — Mocha/Chai integration tests.
- `Dockerfile` — Builds the service image.
- `.gitlab-ci.yml` — Build and test pipeline.

## Run

```bash
docker build -t charcount .
docker run -p 8004:80 charcount
```
