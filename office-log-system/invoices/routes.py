from flask import Blueprint, jsonify

from auth import login_required

invoices_bp = Blueprint('invoices', __name__, url_prefix='/api/invoices')


@invoices_bp.route('/status')
@login_required
def status():
    return jsonify({'module': 'invoices', 'ready': True})
