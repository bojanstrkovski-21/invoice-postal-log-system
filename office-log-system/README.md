# Office Log System

One local web app, one login, two modules:

- **Книга за пошта / Postal Log** — outgoing packages
- **Влезни фактури / Incoming Invoices** — received invoices

Both books are working: add, edit, delete, search, year and date filters, table and grouped view, and Excel export.

Даночен број is stored on partners, on each package, and on each invoice. Invoice numbers use `05-1`, `05-2`, and start again each year.

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

Default admin on first run: `admin` / `admin123`. An admin changes usernames, roles, and passwords from Корисници.

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
