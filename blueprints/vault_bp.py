from flask import Blueprint, render_template, request, redirect, url_for

vault_bp = Blueprint('vault', __name__, url_prefix='/vault')

@vault_bp.route('/')
def vault_home():
    """Document vault homepage"""
    user_token = request.args.get('user_token', '')
    return render_template('vault.html', user_token=user_token, documents=[])

@vault_bp.route('/upload', methods=['POST'])
def upload_document():
    """Handle document upload"""
    return redirect(url_for('vault.vault_home'))
