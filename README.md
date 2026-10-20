# Swimart Bli Bli pool guides

Static site of customer guides, served at https://swimartblibli-guides.hinterlandweb.com

- `/` index of guides
- `/plunge-pool`, `/green-pool`, `/heat-pump` guide pages (print to A4 cleanly)
- `/pdf/` downloadable A4 PDFs

No build step. Vercel deploys on every push to `main`.

## Repo layout

- `source/` — master guide files (standalone HTML), the index page, and the scripts used to build the site and render the A4 PDFs
- `qr/` — print-ready QR codes for the index and each guide
- `pdf/` — the published PDFs
