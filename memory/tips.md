# Tips

- Keep project memory in this folder. `project_office-log-system.md` is the durable context. `session-notes.md` is what happened each day. Do not put session notes back in the project root.
- The old postal app is a reference. Do not edit `D:\My Backups\Bojan\postal-log-system` unless the user asks. Build changes in `office-log-system/`.
- Stop the old postal app before starting this one. Both use port 5000.
- After changing Python files, restart `python app.py` or `start.bat`. A server that is already running will keep the old code.
- Store dates as `yyyy-mm-dd` and show them as `dd.mm.yyyy`. Package types stay in Macedonian even when the UI language is English.
- Даночен број on a package or invoice is a copy made at entry time. Editing the partner later must not silently change old rows.
- `CREATE TABLE IF NOT EXISTS` does not add columns to an existing `office.db`. New columns need `_add_column()` in `db.py`.
