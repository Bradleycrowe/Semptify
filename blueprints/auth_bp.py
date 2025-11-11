"""Authentication Blueprint unified on SQLite-backed user_database."""

from flask import Blueprint, render_template, request, redirect, url_for, session
from user_database import (
    create_pending_user,
    get_pending_user,
    verify_code,
    resend_verification_code,
    mask_contact,
    check_existing_user,
    get_user_by_email,
    update_user_login,
    create_login_pending_entry,
)
from security import _get_or_create_csrf_token, log_event

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            form_data = {
                'first_name': request.form.get('first_name', ''),
                'last_name': request.form.get('last_name', ''),
                'email': request.form.get('email', ''),
                'phone': request.form.get('phone', ''),
                'address': request.form.get('address', ''),
                'city': request.form.get('city', ''),
                'county': request.form.get('county', ''),
                'state': request.form.get('state', ''),
                'zip': request.form.get('zip', ''),
            }

            verification_method = request.form.get('verify_method') or 'email'

            if not all(form_data.values()) or verification_method not in ('email', 'both', 'email'):
                return render_template(
                    'register_simple.html',
                    csrf_token=_get_or_create_csrf_token(),
                    error="All fields are required"
                )

            if check_existing_user(form_data['email'], form_data['phone']):
                return render_template(
                    'register_simple.html',
                    csrf_token=_get_or_create_csrf_token(),
                    error="Email or phone already registered. Please sign in.",
                    show_signin=True
                )

            user_id, code = create_pending_user(form_data, 'email')

            from email_service import send_verification_email
            success = send_verification_email(form_data['email'], code, form_data['first_name'])
            if not success:
                print(f"[WARN] Failed to send email to {form_data['email']} (code: {code})")

            log_event("user_registration_started", {
                "user_id": user_id,
                "method": 'email',
                "email": form_data['email']
            })

            return redirect(url_for('auth.verify', user_id=user_id))

        except Exception as e:
            log_event("user_registration_error", {"error": str(e)})
            return render_template('register_simple.html', csrf_token=_get_or_create_csrf_token(), error=str(e))

    return render_template('register_simple.html', csrf_token=_get_or_create_csrf_token())


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        if not email:
            return render_template('login.html', csrf_token=_get_or_create_csrf_token(), error="Please enter your email")

        user = get_user_by_email(email)
        if not user:
            return render_template('login.html', csrf_token=_get_or_create_csrf_token(), error="Account not found. Please register first.")

        # Create pending entry for this existing user_id
        user_id, code = create_login_pending_entry(user)

        from email_service import send_verification_email
        send_verification_email(user['email'], code, user.get('first_name', ''))
        log_event("login_code_sent", {"user_id": user_id, "email": user['email']})

        return redirect(url_for('auth.verify', user_id=user_id))

    return render_template('login.html', csrf_token=_get_or_create_csrf_token())


@auth_bp.route('/verify')
def verify():
    user_id = request.args.get('user_id')
    if not user_id:
        return redirect(url_for('auth.register'))

    user_data = get_pending_user(user_id)
    if not user_data:
        return render_template('register_simple.html', csrf_token=_get_or_create_csrf_token(), error="Verification session expired. Please register again.")

    contact = mask_contact(user_data['email'], 'email')
    return render_template('verify_code.html', method="email", masked_contact=contact, user_id=user_id, csrf_token=_get_or_create_csrf_token())


@auth_bp.route('/verify', methods=['POST'])
def verify_post():
    user_id = request.form.get('user_id')
    code = request.form.get('full_code')
    if not user_id or not code:
        return redirect(url_for('auth.register'))

    success, error = verify_code(user_id, code)
    if success:
        # For registration, pending contains first/last; for login, it's okay if missing
        user_data = get_pending_user(user_id) or {}
        session['user_id'] = user_id
        session['verified'] = True
        session['user_name'] = f"{user_data.get('first_name','')} {user_data.get('last_name','')}".strip()

        try:
            update_user_login(user_id)
        except Exception as e:
            log_event("update_user_login_error", {"user_id": user_id, "error": str(e)})

        log_event("user_verified", {"user_id": user_id, "email": user_data.get('email')})
        return redirect(url_for('dashboard'))

    # failure: re-render verify page
    user_data = get_pending_user(user_id)
    if not user_data:
        return redirect(url_for('auth.register'))
    contact = mask_contact(user_data['email'], 'email')
    return render_template('verify_code.html', method="email", masked_contact=contact, user_id=user_id, error=error, csrf_token=_get_or_create_csrf_token())


@auth_bp.route('/resend-code', methods=['POST'])
def resend_code():
    user_id = request.form.get('user_id')
    if not user_id:
        return redirect(url_for('auth.register'))

    success, code, _error = resend_verification_code(user_id)
    if success:
        user_data = get_pending_user(user_id)
        if not user_data:
            return redirect(url_for('auth.register'))
        from email_service import send_verification_email
        send_verification_email(user_data['email'], code, user_data.get('first_name',''))
        log_event("verification_code_resent", {"user_id": user_id})
        contact = mask_contact(user_data['email'], 'email')
        return render_template('verify_code.html', method="email", masked_contact=contact, user_id=user_id, success="New code sent!", csrf_token=_get_or_create_csrf_token())

    return redirect(url_for('auth.register'))


@auth_bp.route('/recover')
def recover():
    return render_template('token_recovery.html')
