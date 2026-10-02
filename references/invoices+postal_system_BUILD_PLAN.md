# Office Log System — Build Plan

## Overview

One local web application with a single login and two modules:

1. **Postal Log** (Книга за пошта) — outgoing packages
2. **Incoming Invoices** (Книга за влезни фактури) — received invoices

After login the user sees two big buttons and chooses which system to use.

---

## Goals

- Keep the same simple tech stack as the current postal system
- One login for both modules
- Shared partners list
- Clean separation of data (packages vs invoices)
- Match real paper workflow as closely as possible

---

## Tech Stack

- **Backend:** Python 3 + Flask
- **Database:** SQLite (single file)
- **Frontend:** Vanilla HTML / CSS / JS (single page or multi-view SPA)
- **No build step**, runs fully offline
- Bilingual (Macedonian / English)
- Dual theme (light / dark)

---

## High-level Structure

```
office-log-system/
├── app.py                  # Main Flask app + auth + shared routes
├── postal/
│   └── routes.py           # Postal-specific API
├── invoices/
│   └── routes.py           # Invoice-specific API
├── static/
│   └── index.html          # Frontend (landing + both modules)
├── requirements.txt
├── start.bat
└── office.db               # SQLite database
```

Alternative simpler structure (acceptable for v1):
```
office-log-system/
├── app.py
├── static/index.html
├── requirements.txt
└── office.db
```

---

## Database Design

### 1. users
```sql
id              INTEGER PRIMARY KEY
username        TEXT UNIQUE NOT NULL
password_hash   TEXT NOT NULL
role            TEXT NOT NULL DEFAULT 'user'   -- 'admin' | 'user'
created_at      TEXT DEFAULT CURRENT_TIMESTAMP
```

### 2. partners (shared)
```sql
id              INTEGER PRIMARY KEY
name            TEXT NOT NULL
address         TEXT
city            TEXT
tax_number      TEXT                   -- даночен број, shared
notes           TEXT
created_at      TEXT DEFAULT CURRENT_TIMESTAMP
```

### 3. packages (Postal module)
```sql
id                  INTEGER PRIMARY KEY
ref_number          TEXT NOT NULL          -- manual: 03-145, 08-12, etc.
send_date           TEXT NOT NULL
partner_id          INTEGER                -- optional FK → partners
recipient_name      TEXT NOT NULL
recipient_address   TEXT
city                TEXT
tax_number          TEXT               -- copied from partner, can be edited
package_type        TEXT NOT NULL
year                INTEGER NOT NULL
notes               TEXT
created_at          TEXT DEFAULT CURRENT_TIMESTAMP
```

### 4. invoices (Invoices module)
```sql
id                  INTEGER PRIMARY KEY
internal_number     TEXT NOT NULL          -- auto: 05-1, 05-2, ... (resets yearly)
invoice_number      TEXT                   -- supplier's number (optional)
invoice_date        TEXT                   -- date written on the invoice
received_date       TEXT NOT NULL          -- auto-filled with today
due_date            TEXT
partner_id          INTEGER                -- FK → partners
tax_number          TEXT                   -- даночен број
bank_account        TEXT                   -- 903, 787, 785M6, 785L1, etc.
amount              REAL
currency            TEXT DEFAULT 'MKD'
payment_status      TEXT DEFAULT 'pending' -- pending / paid / cancelled
notes               TEXT
year                INTEGER NOT NULL
created_at          TEXT DEFAULT CURRENT_TIMESTAMP
```

---

## Numbering Rules

### Invoices
- Format: `05-1`, `05-2`, `05-3`...
- Resets every year on 1 January → starts again at `05-1`
- System automatically suggests the next number for the current year
- `received_date` is automatically set to today when creating a new entry

### Postal Packages
- `ref_number` stays **manual**
- User types the full number (examples: `03-145`, `08-12`, `01-3`, `04-7`...)
- Common prefixes: `03-` (most used), `08-`, `01-`, `02-`, `04-`

---

## User Interface Flow

1. **Login screen**
2. **Landing page** — two big buttons:
   - Книга за пошта / Postal Log
   - Влезни фактури / Incoming Invoices
3. Each module has its own:
   - List / Table view
   - Add / Edit modal
   - Search + filters (year, date range)
   - Export (CSV / Excel)
4. Shared elements:
   - Language switcher
   - Theme switcher
   - User menu (logout, change password, manage users for admin)

---

## Main Features by Module

### Postal Log
- Add / Edit / Delete packages
- Manual `ref_number` (Деловоден број)
- Search by recipient
- Filter by year or date range
- Table view + Group by recipient view
- Export CSV / Excel
- Package types (same as current system)

### Incoming Invoices
- Add / Edit / Delete invoices
- Auto `internal_number` (`05-X`) with yearly reset
- Auto `received_date` = today
- Fields: invoice date, due date, partner, bank account, amount, status
- Search + filters
- Export CSV / Excel
- Simple payment status (pending / paid)

### Shared
- Partners management (simple list: add / edit partners)
- User management (admin only)
- Bilingual UI
- Light / Dark theme

---

## Implementation Phases

### Phase 1 — Foundation
- [x] Project structure
- [x] Database tables (users, partners, packages, invoices)
- [x] Login / logout / session
- [x] Landing page with two big buttons
- [x] Basic routing between modules

### Phase 2 — Postal Module
- [x] Migrate existing postal functionality
- [x] Keep current package types and manual ref_number
- [x] Link to partners (optional)
- [x] Export
- [x] Даночен број on partners, packages, and invoices

### Phase 3 — Invoices Module
- [ ] Invoice CRUD
- [ ] Auto internal_number (`05-X`) with yearly reset
- [ ] Auto received_date
- [ ] Bank account field
- [ ] Basic payment status
- [ ] Export

### Phase 4 — Shared & Polish
- [ ] Partners management UI
- [ ] Consistent design between both modules
- [ ] Yearly reset logic tested
- [ ] Backup / restore notes
- [ ] Final testing

---

## Notes & Decisions

- One SQLite database file for simplicity
- `created_at` is kept as automatic timestamp
- `received_date` on invoices is auto-filled (can be edited if needed)
- Postal `ref_number` remains fully manual
- Partners are shared between both modules
- System runs locally (and can be accessed on LAN)

---

## Future Ideas (not in v1)

- Automatic next-number suggestion also for postal prefixes
- Dashboard with counts / pending invoices
- Attachments (scan of invoice)
- Better reporting

---

*Plan created: 2026-10-02*
