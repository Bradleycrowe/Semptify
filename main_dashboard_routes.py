# main_dashboard_routes.py - Production-ready homepage matching Render deployment
from flask import Blueprint, render_template, session, request

main_dashboard_bp = Blueprint('main_dashboard', __name__)

@main_dashboard_bp.route('/')
def home():
    """Main Semptify homepage - matches production on Render"""
    user_token = request.args.get('user_token') or session.get('user_token')
    storage_qualified = session.get('qualified', False)
    
    return render_template('main_dashboard/home.html',
                         user_token=user_token,
                         storage_qualified=storage_qualified)

@main_dashboard_bp.route('/dashboard')
def dashboard():
    """Legacy route - redirect to homepage"""
    from flask import redirect, url_for
    return redirect(url_for('main_dashboard.home'))
