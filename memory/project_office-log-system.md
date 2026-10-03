---
name: project-office-log-system
description: "Combined office log — postal packages and incoming invoices. Flask + SQLite, bilingual MK/EN UI"
metadata:
  type: project
---

One local web app, one login, two books. Replaces the paper invoice book and the separate postal app.

**Location on this Linux machine:** `/home/bojan/Data/invoice-postal-log-system/`

**Older Windows location:** `d:\My Backups\kniga na vlezni fakturi\office-log-system\`

**Source papers and build plan:** `d:\My Backups\kniga na vlezni fakturi\references\`

**Old postal app (reference only, do not edit unless asked):** `d:\My Backups\Bojan\postal-log-system\kniga-za-posta\`

**Stack:** Python Flask + SQLite (`office.db`), single-page vanilla HTML/CSS/JS. No build step. Runs offline at `http://localhost:5000`.

**Files:**
- `app.py` — auth, users, shared partners API
- `db.py` — schema and column migration
- `auth.py` — `@login_required`, `@admin_required`
- `postal/routes.py` — package CRUD, years, Excel export
- `invoices/routes.py` — invoice CRUD, next `05-X`, years, Excel export
- `static/index.html` — login, landing, postal UI, invoice UI, partners modal
- `requirements.txt` — flask, openpyxl
- `start.bat` — installs deps, starts the server, opens the browser after 10 seconds

**DB tables:** `users`, `partners`, `packages`, `invoices`

**Partners:** id, name, address, city, tax_number, notes, created_at. Shared by both modules.

**Packages:** id, ref_number, send_date, partner_id, recipient_name, recipient_address, city, tax_number, package_type, year, notes, created_at

**Invoices:** id, internal_number, invoice_number, invoice_date, received_date, due_date, partner_id, supplier_name, tax_number, bank_account, amount, currency, payment_status, notes, year, created_at. Unique `(year, internal_number)`.

**Package types (stored in Macedonian):** обична, препорачана, препорачана со повратница, брза пошта, брза пошта препорачана со повратница

**API:**
- `POST /api/login`, `POST /api/logout`, `GET /api/me`, `PUT /api/me/password`
- `GET/POST /api/users`, `PUT/DELETE /api/users/<id>` — update changes username, role, and an optional password
- `GET/POST /api/partners`, `PUT/DELETE /api/partners/<id>`
- `GET/POST /api/postal/packages` — list supports `search`, `year`, `date_from`, `date_to`
- `PUT/DELETE /api/postal/packages/<id>`
- `GET /api/postal/years`
- `GET /api/postal/export?format=xlsx` — same filters as the list. The screen exports Excel only.
- `GET /api/invoices` — list supports `search`, `year`, `status`, `date_from`, `date_to`
- `POST /api/invoices`, `PUT/DELETE /api/invoices/<id>`
- `GET /api/invoices/next?received_date=yyyy-mm-dd` — next `05-X` for that year
- `GET /api/invoices/years`
- `GET /api/invoices/export?format=xlsx` — same filters as the list. The screen exports Excel only.
- `GET /api/invoices/status`

**Roles:** `admin` can edit/delete packages and invoices, delete partners, and manage users from Корисници. That screen can rename a user, change the role, and set a password. A blank password keeps the old one. The last admin cannot be deleted or demoted. `user` can add packages and invoices, and add/edit partners. Edit/delete buttons are hidden for `user`. There is no password button in the navbar.

**GitHub:** https://github.com/bojanstrkovski-21/invoice-postal-log-system — branch `main`. Remote is HTTPS. `office.db` is tracked. MIT license and a root `README.md` are in the repo. `push.sh` commits everything and pushes `main`. `set-git-cred.sh` would switch origin to SSH; do not run it unless asked.

**Current status (2026-10-02, session closed):** Phase 1, Phase 2, and Phase 3 are done locally. User signed in after the invoice book was added. Postal log and invoice entry are usable. Excel export only. No navbar password button. Admin user editing is in Корисници. No import from the old `pratki.db`. GitHub `main` does not yet have this session. Last pushed commit is `9e0d977`.

**Decisions:**
- Даночен број is on partners, packages, and invoices. The user asked for it on both books.
- Choosing a partner copies name, address, city, and tax number onto the package. Later partner edits do not rewrite old packages.
- Postal `ref_number` stays manual and is required. Common prefixes: `03-`, `08-`, `01-`, `02-`, `04-`.
- Invoice internal number is `05-1`, `05-2`, … and resets each year. The form suggests the next number from the received date. An empty number is filled on save. `received_date` starts as today and can be edited.
- `supplier_name` and `tax_number` are snapshots. Choosing a partner copies them. Later partner edits do not rewrite old invoices.
- Paper invoice book columns are реден број, број, датум, назив на седиште, даночен број, износ, сметка, забелешка. The app also stores due date, currency, and payment status.
- Light theme is default (Dawnfox, `--bg: #b8cece`). Dark theme is Nightfox. Preference is in `localStorage`.
- Dates display as `dd.mm.yyyy`. The database stores `yyyy-mm-dd`. Date fields are a text input with auto-inserted dots plus a calendar button. `lang="mk"` alone was not reliable.
- Package types stay Macedonian even when the UI is English.
- All UI stays in `static/index.html`. No build step.
- Default admin on first run: `admin` / `admin123`. Change the password from Корисници, not from a navbar button.
- Screen export is Excel only. Do not put the CSV button back unless asked.
- Linux installs go in `office-log-system/.venv`. Do not use system `pip`.
- The old postal app also binds to port 5000. Stop it before starting this one.
- Restart the server after Python changes. The running process does not reload them.
- Existing databases get new columns through `_add_column()` in `db.py`. Do not rely on `CREATE TABLE IF NOT EXISTS` to alter an old `office.db`.
- `office.db` stays in git. Match the postal project: do not ignore database files.
- GitHub default branch is `main`. Do not recreate `master`.

**Why:** One login and one database for both paper books, without changing the postal workflow people already know.

**How to apply:** Keep new invoice UI in the same page and the same theme. Store invoice status values as `pending`, `paid`, or `cancelled`. Suggest the next `05-X` for the current year, but let the user edit `received_date`. Do not auto-import `pratki.db` unless asked.
