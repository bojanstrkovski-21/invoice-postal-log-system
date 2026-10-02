---
name: project-office-log-system
description: "Combined office log — postal packages and incoming invoices. Flask + SQLite, bilingual MK/EN UI"
metadata:
  type: project
---

One local web app, one login, two books. Replaces the paper invoice book and the separate postal app.

**Location:** `d:\My Backups\kniga na vlezni fakturi\office-log-system\`

**Source papers and build plan:** `d:\My Backups\kniga na vlezni fakturi\references\`

**Old postal app (reference only, do not edit unless asked):** `d:\My Backups\Bojan\postal-log-system\kniga-za-posta\`

**Stack:** Python Flask + SQLite (`office.db`), single-page vanilla HTML/CSS/JS. No build step. Runs offline at `http://localhost:5000`.

**Files:**
- `app.py` — auth, users, shared partners API
- `db.py` — schema and column migration
- `auth.py` — `@login_required`, `@admin_required`
- `postal/routes.py` — package CRUD, years, CSV/Excel export
- `invoices/routes.py` — status only; invoice CRUD is not built yet
- `static/index.html` — login, landing, both module shells, postal UI, partners modal
- `requirements.txt` — flask, openpyxl
- `start.bat` — installs deps, starts the server, opens the browser after 10 seconds

**DB tables:** `users`, `partners`, `packages`, `invoices`

**Partners:** id, name, address, city, tax_number, notes, created_at. Shared by both modules.

**Packages:** id, ref_number, send_date, partner_id, recipient_name, recipient_address, city, tax_number, package_type, year, notes, created_at

**Invoices (schema only):** id, internal_number, invoice_number, invoice_date, received_date, due_date, partner_id, tax_number, bank_account, amount, currency, payment_status, notes, year, created_at. Unique `(year, internal_number)`.

**Package types (stored in Macedonian):** обична, препорачана, препорачана со повратница, брза пошта, брза пошта препорачана со повратница

**API:**
- `POST /api/login`, `POST /api/logout`, `GET /api/me`, `PUT /api/me/password`
- `GET/POST /api/users`, `DELETE /api/users/<id>`, `PUT /api/users/<id>/password`
- `GET/POST /api/partners`, `PUT/DELETE /api/partners/<id>`
- `GET/POST /api/postal/packages` — list supports `search`, `year`, `date_from`, `date_to`
- `PUT/DELETE /api/postal/packages/<id>`
- `GET /api/postal/years`
- `GET /api/postal/export?format=csv|xlsx` — same filters as the list
- `GET /api/invoices/status` — placeholder

**Roles:** `admin` can edit/delete packages, delete partners, and manage users. `user` can add packages and add/edit partners. Edit/delete buttons are hidden for `user`.

**GitHub:** https://github.com/bojanstrkovski-21/invoice-postal-log-system — branch `main`. `office.db` is committed. MIT license is in the repo root.

**Current status (2026-10-02):** Phase 1 and Phase 2 done. User tested login. Postal log is usable. Invoice entry is not built. No import from the old `pratki.db`. Repo is pushed.

**Decisions:**
- Даночен број is on partners, packages, and invoices. The user asked for it on both books.
- Choosing a partner copies name, address, city, and tax number onto the package. Later partner edits do not rewrite old packages.
- Postal `ref_number` stays manual and is required. Common prefixes: `03-`, `08-`, `01-`, `02-`, `04-`.
- Invoice internal number will be `05-1`, `05-2`, … and resets each year. `received_date` starts as today. Not built yet.
- Paper invoice book columns also include реден број, број, датум, назив на седиште, даночен број, износ, сметка, забелешка.
- Light theme is default (Dawnfox, `--bg: #b8cece`). Dark theme is Nightfox. Preference is in `localStorage`.
- Dates display as `dd.mm.yyyy`. The database stores `yyyy-mm-dd`. Date fields are a text input with auto-inserted dots plus a calendar button. `lang="mk"` alone was not reliable.
- Package types stay Macedonian even when the UI is English.
- All UI stays in `static/index.html`. No build step.
- Default admin on first run: `admin` / `admin123`. Change it after login.
- The old postal app also binds to port 5000. Stop it before starting this one.
- Restart the server after Python changes. The running process does not reload them.
- Existing databases get new columns through `_add_column()` in `db.py`. Do not rely on `CREATE TABLE IF NOT EXISTS` to alter an old `office.db`.
- `office.db` stays in git. Match the postal project: do not ignore database files.
- GitHub default branch is `main`. Do not recreate `master`.

**Why:** One login and one database for both paper books, without changing the postal workflow people already know.

**How to apply:** Keep new invoice UI in the same page and the same theme. Store invoice status values as `pending`, `paid`, or `cancelled`. Suggest the next `05-X` for the current year, but let the user edit `received_date`. Do not auto-import `pratki.db` unless asked.
