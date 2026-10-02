# Office Log System

One local web app, one login, two modules:

- **Книга за пошта / Postal Log** — outgoing packages
- **Влезни фактури / Incoming Invoices** — received invoices

Postal log is working: add, edit, delete, search, year and date filters, table and grouped view, CSV/Excel export. Incoming invoices are next.

Даночен број is stored on partners, on each package, and on invoices.

## Tech stack

- Python 3 + Flask
- SQLite (`office.db`, created on first run)
- Single-page HTML / CSS / JS — no build step

## Run

```bash
pip install -r requirements.txt
python app.py
```

Then open [http://localhost:5000](http://localhost:5000).

**Windows:** double-click `start.bat`.

Default admin on first run: `admin` / `admin123`. Change it after login.

The older postal app also uses port 5000. Stop that one before starting this app.

## Layout

```text
office-log-system/
├── app.py                 Auth and shared routes
├── db.py                  SQLite schema
├── auth.py                Login / admin checks
├── postal/routes.py       Postal API
├── invoices/routes.py     Invoice API
├── static/index.html      Landing page and both module shells
├── requirements.txt
└── start.bat
```

Source papers and the build plan are in `../references/`.
