from datetime import datetime
# main_dashboard_routes.py - Production-ready homepage matching Render deployment
from flask import Blueprint, render_template, session, request, redirect, url_for

main_dashboard_bp = Blueprint('main_dashboard', __name__)

@main_dashboard_bp.route('/')
def home():
    """Main Semptify homepage - matches production on Render - REFACTORED: Uses /system/context"""
    user_token = request.args.get('user_token') or session.get('user_token')
    storage_qualified = session.get('qualified', False)
    
    return render_template('dashboard_home.html',
                           datetime=datetime,
                           admin_token=request.args.get('admin_token', ''),
                         user_token=user_token,
                         storage_qualified=storage_qualified)

@main_dashboard_bp.route('/dashboard')
def dashboard():
    """Legacy route - redirect to homepage - REFACTORED: Uses /system/context"""
    return redirect(url_for('main_dashboard.home'))

@main_dashboard_bp.route('/ledger')
def ledger():
    """Rent ledger placeholder - REFACTORED: Uses /system/context"""
    return '''
    <html><head><title>Rent Ledger</title></head><body style="font-family:sans-serif;max-width:800px;margin:50px auto;padding:20px;">
    <h1>🧾 Rent Ledger</h1>
    <p>Track your rent payments and maintain proof of payment history.</p>
    <p><em>Feature under construction.</em></p>
    <p><a href="/">← Back to Home</a> | <a href="/cards">All Features</a></p>
    </body></html>
    ''', 200

@main_dashboard_bp.route('/housing_journey')
def housing_journey():
    """Redirect to docs journey - REFACTORED: Uses /system/context"""
    return redirect('/docs/journey')

@main_dashboard_bp.route('/pages/research')
def pages_research():
    """Redirect to research page - REFACTORED: Uses /system/context"""
    return redirect('/research')

@main_dashboard_bp.route('/settings')
def settings():
    """User settings placeholder - REFACTORED: Uses /system/context"""
    return '''
    <html><head><title>Settings</title></head><body style="font-family:sans-serif;max-width:800px;margin:50px auto;padding:20px;">
    <h1>⚙️ Settings</h1>
    <p>User settings page - under construction.</p>
    <p><a href="/">← Back to Home</a></p>
    </body></html>
    ''', 200

