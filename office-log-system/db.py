import os
import sqlite3

from flask import g
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), 'office.db')


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys = ON')
    return db


def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('PRAGMA foreign_keys = ON')
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id              INTEGER PRIMARY KEY,
                username        TEXT UNIQUE NOT NULL,
                password_hash   TEXT NOT NULL,
                role            TEXT NOT NULL DEFAULT 'user',
                created_at      TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS partners (
                id              INTEGER PRIMARY KEY,
                name            TEXT NOT NULL,
                address         TEXT,
                city            TEXT,
                tax_number      TEXT,
                notes           TEXT,
                created_at      TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS packages (
                id                  INTEGER PRIMARY KEY,
                ref_number          TEXT NOT NULL,
                send_date           TEXT NOT NULL,
                partner_id          INTEGER REFERENCES partners(id) ON DELETE SET NULL,
                recipient_name      TEXT NOT NULL,
                recipient_address   TEXT,
                city                TEXT,
                tax_number          TEXT,
                package_type        TEXT NOT NULL,
                year                INTEGER NOT NULL,
                notes               TEXT,
                created_at          TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS invoices (
                id                  INTEGER PRIMARY KEY,
                internal_number     TEXT NOT NULL,
                invoice_number      TEXT,
                invoice_date        TEXT,
                received_date       TEXT NOT NULL,
                due_date            TEXT,
                partner_id          INTEGER REFERENCES partners(id) ON DELETE SET NULL,
                supplier_name       TEXT,
                tax_number          TEXT,
                bank_account        TEXT,
                amount              REAL,
                currency            TEXT DEFAULT 'MKD',
                exchange_rate       REAL,
                rate_date           TEXT,
                amount_mkd          REAL,
                payment_status      TEXT NOT NULL DEFAULT 'pending'
                                    CHECK (payment_status IN ('pending', 'paid', 'cancelled')),
                notes               TEXT,
                year                INTEGER NOT NULL,
                created_at          TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (year, internal_number)
            );

            CREATE INDEX IF NOT EXISTS idx_packages_year ON packages(year);
            CREATE INDEX IF NOT EXISTS idx_packages_partner ON packages(partner_id);
            CREATE INDEX IF NOT EXISTS idx_invoices_year ON invoices(year);
            CREATE INDEX IF NOT EXISTS idx_invoices_partner ON invoices(partner_id);
        ''')
        _add_column(conn, 'partners', 'tax_number', 'TEXT')
        _add_column(conn, 'packages', 'tax_number', 'TEXT')
        _add_column(conn, 'invoices', 'tax_number', 'TEXT')
        _add_column(conn, 'invoices', 'supplier_name', 'TEXT')
        _add_column(conn, 'invoices', 'exchange_rate', 'REAL')
        _add_column(conn, 'invoices', 'rate_date', 'TEXT')
        _add_column(conn, 'invoices', 'amount_mkd', 'REAL')
        count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        if count == 0:
            conn.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, 'admin')",
                ('admin', generate_password_hash('admin123'))
            )
            print('  Default admin created — username: admin  password: admin123')
            print('  Change the password after first login.')
        conn.commit()


def _add_column(conn, table, column, definition):
    cols = {row[1] for row in conn.execute(f'PRAGMA table_info({table})')}
    if column not in cols:
        conn.execute(f'ALTER TABLE {table} ADD COLUMN {column} {definition}')
