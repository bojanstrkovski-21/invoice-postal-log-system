# Office Log System

## Overview
Local web app for two office books: outgoing postal packages and incoming invoices. One login, one SQLite file, used offline.

## Stack
- **Language**: Python 3
- **Framework / Tools**: Flask, SQLite, vanilla HTML/CSS/JS
- **Key dependencies**: flask, openpyxl

## Conventions
- UI stays in `office-log-system/static/index.html`. No build step.
- Macedonian is the default language. English is a toggle. Package types are stored in Macedonian.
- Dates in the database are `yyyy-mm-dd`. The screen shows `dd.mm.yyyy`.
- Themes are Dawnfox light (default) and Nightfox dark.
- Admin can edit and delete records. A normal user can add them.

## Constraints
- Runs on Windows, fully offline, on port 5000.
- Do not edit the old postal app unless asked.
- Do not import `pratki.db` unless asked.
- Do not add a frontend build step or extra frameworks.

## Frozen Files
- `references/` — source papers and the build plan. Do not move or rewrite them unless asked.

## How to Run
```bash
cd office-log-system
pip install -r requirements.txt
python app.py
```

Windows: double-click `office-log-system/start.bat`, then open http://localhost:5000.

First login: `admin` / `admin123`. Stop the old postal app first. It uses the same port.

## Current State
Phase 1 and Phase 2 are done. Login, landing page, partners, and the postal log work, including даночен број. The invoice book has a database table and a placeholder screen only.

## Next Steps
1. Phase 3 — invoice add/edit/delete
2. Auto internal number `05-X`, reset each year
3. Received date defaults to today
4. Bank account, amount, payment status, tax number
5. Invoice search, filters, and CSV/Excel export

## Recent Work
- 2026-10-02 — Foundation, postal module, tax number, and project memory
