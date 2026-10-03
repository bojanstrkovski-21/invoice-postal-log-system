# Office Log System

Local web app for two office books. One login, one SQLite file, works offline.

- **Книга за пошта / Postal Log** — outgoing packages
- **Влезни фактури / Incoming Invoices** — received invoices

The app is in `office-log-system/`. Source papers and the build plan are in `references/`.

## Run

**Windows:** double-click `office-log-system/start.bat`, then open [http://localhost:5000](http://localhost:5000).

**Linux:**

```bash
cd office-log-system
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app.py
```

First login: `admin` / `admin123`.

Stop the older postal app first. It uses the same port.

## What it does

Both books can add, search, filter by year and date, switch between table and grouped view, and export Excel.

An admin can edit and delete records. A normal user can add them. Edit and delete buttons stay hidden for a normal user.

**Корисници** is admin only. An admin can rename a user, make them an admin or not, and set a password. Leave the password empty to keep the old one. The last admin cannot be deleted or demoted.

**Партнери** are shared. Choosing a partner copies the name and tax number onto the package or invoice. Changing the partner later does not rewrite old rows.

Invoice numbers are suggested as `05-1`, `05-2`, and start again each year. The received date starts as today and can be changed. Payment status is pending, paid, or cancelled.

Dates are stored as `yyyy-mm-dd` and shown as `dd.mm.yyyy`. Macedonian is the default language. English is a toggle. Package types stay in Macedonian.

The database file is `office-log-system/office.db`. Copy that file to back up the books.

## Git

```bash
./push.sh "commit message"
```

`set-git-cred.sh` sets the Git name, email, and an SSH remote. The current remote is HTTPS. Run that script only if GitHub SSH already works on this computer.

## License

MIT. See [LICENSE](LICENSE).
