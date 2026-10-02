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
