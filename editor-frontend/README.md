# editor-frontend

The QUBeditotron3000 user interface. Provides a text area and buttons for each counting operation, sends requests to the backend services through the reverse proxy, and saves/loads text using Google Firestore.

Static HTML and JavaScript, served on port 80.

## Files

- `src/index.html` — The full UI: text area, operation buttons, the JavaScript that calls each counting service via the proxy, and the Firebase/Firestore save and load logic.
- `src/config.json` — Maps service names to their base URLs.
- `src/firebase-config.example.js` — Template for the Firebase web config.
- `Dockerfile` — Serves the static frontend.

## Firebase configuration

`index.html` loads the Firebase web config from `src/firebase-config.js`, which
is **git-ignored** so credentials are never committed. Before building, create it
from the template:

```bash
cp src/firebase-config.example.js src/firebase-config.js
# then edit src/firebase-config.js with your Firebase project's values
```

Find the values in the Firebase console: *Project settings > Your apps > SDK
setup and configuration*.

## Run

```bash
docker build -t frontend .
docker run -p 3000:80 frontend
```

Then open http://localhost:3000.
