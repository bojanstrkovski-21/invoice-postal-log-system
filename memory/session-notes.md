# Session Notes

## 2026-10-02 — Session 1 (office-log-system)

### What was done
- Read `references/invoices+postal_system_BUILD_PLAN.md` and the old postal app in `D:\My Backups\Bojan\postal-log-system`
- Moved the source papers, spreadsheets, and build plan into `references/`
- Phase 1: Flask app, SQLite tables, login/logout/session, landing page with two buttons
- Phase 2: postal log migrated — manual ref number, package types, search, year and date filters, table and group views, CSV/Excel export, optional partner link
- Added даночен број on partners, packages, and invoices. Package value is a snapshot copied from the partner
- User confirmed the app starts and login works
- Wrote this memory folder so the next session does not depend on chat history
- Git repo: https://github.com/bojanstrkovski-21/invoice-postal-log-system
- Default branch is `main`. `master` only had the GitHub MIT `LICENSE`, so the site looked empty until the default was switched and `master` was deleted
- `office.db` is tracked, same as `pratki.db` in the old postal repo. Root and app `.gitignore` files do not ignore `*.db`
- MIT `LICENSE` is on `main`, copyright 2026 bojanstrkovski-21

### Next
- Phase 3: invoice CRUD, auto `05-X` with yearly reset, received date defaults to today, bank account, payment status, export, and tax number on the form
- Do not import the old `pratki.db` unless asked
- Restart the server before testing backend changes

## 2026-10-02 — Session 2 (invoice book)

### What was done
- Installed Flask and openpyxl in `office-log-system/.venv`. System Python refused a global install.
- Phase 3: invoice add, edit, delete, search, year/date/status filters, table and grouped view, CSV/Excel export
- New invoices suggest `05-1`, `05-2`, … from the received-date year. The number can be edited. A duplicate in the same year is rejected.
- Received date starts as today. Choosing a partner copies the name and tax number; later partner edits do not rewrite the invoice.
- Added `supplier_name` so the paper-book назив is stored on the invoice, not only through the partner link.
- API check passed against a temporary database: numbering, yearly reset, filters, snapshot, user/admin rights, CSV, and Excel.

### Next
- Phase 4: polish, Windows test, backup notes. Partners UI is already in place.
- Restart the server before testing. Do not import `pratki.db` unless asked.

### Follow-up the same day
- User signed in and confirmed the app runs.
- Removed CSV export buttons. Both books export Excel only.
- Removed the navbar password button for every role.
- Admin can edit any user from Корисници: username, role, and password. Blank password keeps the old one. The last admin cannot be deleted or demoted.
- Added root `README.md`, `push.sh`, and `set-git-cred.sh`. The scripts were not run.
- A commit and push was requested, then the command was denied. Nothing from this session is on GitHub. `origin/main` is still `9e0d977`.
- Remote is still HTTPS. Do not switch it to SSH unless the user runs `set-git-cred.sh`.

### Left uncommitted
- Invoice book, user editing, Excel-only export, README, and the two Git scripts
- `office.db` has the new empty `supplier_name` column. No invoice rows were added.
- `office-log-system/.venv` is local and ignored

### Next
- User can push with `./push.sh "commit message"` when they want. Do not change the remote first.
- Phase 4: polish, Windows test, backup notes. Do not import `pratki.db` unless asked.
