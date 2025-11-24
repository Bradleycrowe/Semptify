# Add these routes to calendar_master.py before the PHASE 2 comment

@calendar_master_bp.route('/calendar/view')
def calendar_view():
    """"Open Calendar" - Interactive calendar view"""
    user_token = _get_user_token()
    return render_template('calendar_view.html', user_token=user_token)

@calendar_master_bp.route('/calendar/deadlines')
def calendar_deadlines():
    """"Track Deadlines" - Court dates, filing deadlines, important dates"""
    user_token = _get_user_token()
    return render_template('calendar_deadlines.html', user_token=user_token)

@calendar_master_bp.route('/calendar/ledger')
def calendar_ledger():
    """"View Ledger" - Rent payment ledger integrated with calendar"""
    user_token = _get_user_token()
    return render_template('calendar_ledger.html', user_token=user_token)

@calendar_master_bp.route('/calendar/rent-ledger')
def calendar_rent_ledger():
    """"View Ledger" - Alternative route for rent ledger"""
    user_token = _get_user_token()
    return render_template('calendar_ledger.html', user_token=user_token)

@calendar_master_bp.route('/calendar/payments')
def calendar_payments():
    """"Payment Schedule" - Upcoming rent payments and payment tracking"""
    user_token = _get_user_token()
    return render_template('calendar_payments.html', user_token=user_token)
