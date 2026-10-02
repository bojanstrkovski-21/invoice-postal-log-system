import os
import sqlite3

from flask import Flask, jsonify, request, send_from_directory, session
from werkzeug.security import check_password_hash, generate_password_hash

from auth import admin_required, login_required
from db import close_connection, get_db, init_db
from invoices.routes import invoices_bp
from postal.routes import postal_bp

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'office-log-secret-2026')
app.register_blueprint(postal_bp)
app.register_blueprint(invoices_bp)


@app.teardown_appcontext
def _close_connection(exception):
    close_connection(exception)


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    db = get_db()
    user = db.execute(
        'SELECT * FROM users WHERE username = ?',
        (data.get('username', '').strip(),)
    ).fetchone()
    if not user or not check_password_hash(user['password_hash'], data.get('password', '')):
        return jsonify({'error': 'Invalid username or password'}), 401
    session['user_id'] = user['id']
    session['username'] = user['username']
    session['role'] = user['role']
    return jsonify({'id': user['id'], 'username': user['username'], 'role': user['role']})


@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'ok': True})


@app.route('/api/me')
def me():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    return jsonify({
        'id': session['user_id'],
        'username': session['username'],
        'role': session['role']
    })


@app.route('/api/me/password', methods=['PUT'])
@login_required
def change_own_password():
    data = request.get_json(silent=True) or {}
    current = data.get('current_password', '')
    new_pw = data.get('password', '').strip()
    if not new_pw:
        return jsonify({'error': 'Password is required'}), 400
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    if not user or not check_password_hash(user['password_hash'], current):
        return jsonify({'error': 'Current password is incorrect'}), 400
    db.execute(
        'UPDATE users SET password_hash = ? WHERE id = ?',
        (generate_password_hash(new_pw), session['user_id'])
    )
    db.commit()
    return jsonify({'ok': True})


@app.route('/api/users', methods=['GET'])
@admin_required
def get_users():
    db = get_db()
    rows = db.execute(
        'SELECT id, username, role, created_at FROM users ORDER BY id'
    ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route('/api/users', methods=['POST'])
@admin_required
def create_user():
    data = request.get_json(silent=True) or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    role = data.get('role', 'user')
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    if role not in ('admin', 'user'):
        return jsonify({'error': 'Invalid role'}), 400
    db = get_db()
    try:
        cur = db.execute(
            'INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
            (username, generate_password_hash(password), role)
        )
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 409
    row = db.execute(
        'SELECT id, username, role, created_at FROM users WHERE id = ?',
        (cur.lastrowid,)
    ).fetchone()
    return jsonify(dict(row)), 201


@app.route('/api/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    data = request.get_json(silent=True) or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    role = data.get('role', 'user')
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    if role not in ('admin', 'user'):
        return jsonify({'error': 'Invalid role'}), 400
    db = get_db()
    existing = db.execute('SELECT id, role FROM users WHERE id = ?', (user_id,)).fetchone()
    if not existing:
        return jsonify({'error': 'Not found'}), 404
    if existing['role'] == 'admin' and role != 'admin':
        admins = db.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'").fetchone()[0]
        if admins <= 1:
            return jsonify({'error': 'The last admin cannot be changed to a normal user'}), 400
    try:
        if password:
            db.execute(
                'UPDATE users SET username = ?, password_hash = ?, role = ? WHERE id = ?',
                (username, generate_password_hash(password), role, user_id)
            )
        else:
            db.execute(
                'UPDATE users SET username = ?, role = ? WHERE id = ?',
                (username, role, user_id)
            )
        db.commit()
    except sqlite3.IntegrityError:
        db.rollback()
        return jsonify({'error': 'Username already exists'}), 409
    if user_id == session['user_id']:
        session['username'] = username
        session['role'] = role
    row = db.execute(
        'SELECT id, username, role, created_at FROM users WHERE id = ?',
        (user_id,)
    ).fetchone()
    return jsonify(dict(row))


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    if user_id == session['user_id']:
        return jsonify({'error': 'Cannot delete your own account'}), 400
    db = get_db()
    target = db.execute('SELECT role FROM users WHERE id = ?', (user_id,)).fetchone()
    if target and target['role'] == 'admin':
        admins = db.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'").fetchone()[0]
        if admins <= 1:
            return jsonify({'error': 'The last admin cannot be deleted'}), 400
    db.execute('DELETE FROM users WHERE id = ?', (user_id,))
    db.commit()
    return jsonify({'ok': True})


def _clean(value):
    if value is None:
        return ''
    return str(value).strip()


@app.route('/api/partners', methods=['GET'])
@login_required
def get_partners():
    db = get_db()
    rows = db.execute(
        'SELECT * FROM partners ORDER BY name COLLATE NOCASE, id'
    ).fetchall()
    return jsonify([dict(row) for row in rows])


@app.route('/api/partners', methods=['POST'])
@login_required
def create_partner():
    data = request.get_json(silent=True) or {}
    name = _clean(data.get('name'))
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    db = get_db()
    cur = db.execute(
        'INSERT INTO partners (name, address, city, tax_number, notes) VALUES (?,?,?,?,?)',
        (name, _clean(data.get('address')) or None, _clean(data.get('city')) or None,
         _clean(data.get('tax_number')) or None, _clean(data.get('notes')) or None)
    )
    db.commit()
    row = db.execute('SELECT * FROM partners WHERE id = ?', (cur.lastrowid,)).fetchone()
    return jsonify(dict(row)), 201


@app.route('/api/partners/<int:partner_id>', methods=['PUT'])
@login_required
def update_partner(partner_id):
    data = request.get_json(silent=True) or {}
    name = _clean(data.get('name'))
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    db = get_db()
    existing = db.execute('SELECT id FROM partners WHERE id = ?', (partner_id,)).fetchone()
    if not existing:
        return jsonify({'error': 'Not found'}), 404
    db.execute(
        'UPDATE partners SET name=?, address=?, city=?, tax_number=?, notes=? WHERE id=?',
        (name, _clean(data.get('address')) or None, _clean(data.get('city')) or None,
         _clean(data.get('tax_number')) or None, _clean(data.get('notes')) or None, partner_id)
    )
    db.commit()
    row = db.execute('SELECT * FROM partners WHERE id = ?', (partner_id,)).fetchone()
    return jsonify(dict(row))


@app.route('/api/partners/<int:partner_id>', methods=['DELETE'])
@admin_required
def delete_partner(partner_id):
    db = get_db()
    db.execute('DELETE FROM partners WHERE id = ?', (partner_id,))
    db.commit()
    return jsonify({'ok': True})


if __name__ == '__main__':
    init_db()
    print()
    print('  Office Log System — стартуван!')
    print('  Отворете: http://localhost:5000')
    print()
    app.run(host='0.0.0.0', port=5000, debug=False)
