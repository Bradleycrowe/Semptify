"""
Authentication Blueprint
Handles user registration, login, verification, and session management
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from user_registration import create_pending_user, get_pending_user
from user_registration import verify_code, resend_verification_code
from user_registration import generate_verification_code, mask_contact
from user_database import check_existing_user, get_user_by_email
from security import _get_or_create_csrf_token, log_event
import os

# Create blueprint
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration with verification"""
    if request.method == 'POST':
        try:
            # Get all form fields
            form_data = {
                'first_name': request.form.get('first_name'),
                'last_name': request.form.get('last_name'),
                'email': request.form.get('email'),
                'phone': request.form.get('phone'),
                'address': request.form.get('address'),
                'city': request.form.get('city'),
                'county': request.form.get('county'),
                'state': request.form.get('state'),
                'zip': request.form.get('zip'),
            }

            verification_method = request.form.get('verify_method')

            # Validate all fields
            if not all(form_data.values()) or not verification_method:
                return render_template('register_simple.html',
                                     csrf_token=_get_or_create_csrf_token(),
                                     error="All fields are required")

            # Check if email or phone already registered
            if check_existing_user(form_data['email'], form_data['phone']):
                return render_template('register_simple.html',
                                     csrf_token=_get_or_create_csrf_token(),
                                     error="Email or phone already registered. Please sign in.",
                                     show_signin=True)

            # Create pending user and generate code
            user_id, code = create_pending_user(form_data, verification_method)

            # Send verification code via email
            from email_service import send_verification_email

            if verification_method in ['email', 'both']:
                success = send_verification_email(
                    form_data['email'],
                    code,
                    form_data['first_name']
                )
                if not success:
                    print(f"⚠️ Failed to send email to {form_data['email']}, code: {code}")

            # Log for debugging
            print(f"Verification code for {user_id}: {code}")
            log_event("user_registration_started", {
                "user_id": user_id,
                "method": verification_method,
                "email": form_data['email']
            })

            # Redirect to verification page
            return redirect(url_for('auth.verify', user_id=user_id))

        except Exception as e:
            log_event("user_registration_error", {"error": str(e)})
            return render_template('register_simple.html',
                                 csrf_token=_get_or_create_csrf_token(),
                                 error=str(e))

    return render_template('register_simple.html',
                         csrf_token=_get_or_create_csrf_token())


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login for returning users"""
    if request.method == 'POST':
        email_or_phone = request.form.get('email')

        if not email_or_phone:
            return render_template('login.html',
                                 csrf_token=_get_or_create_csrf_token(),
                                 error="Please enter your email or phone")

        # Check if user exists (try email first)
        user = get_user_by_email(email_or_phone)
        
        if not user:
            return render_template('login.html',
                                 csrf_token=_get_or_create_csrf_token(),
                                 error="Account not found. Please register first.")

        # Generate verification code
        code = generate_verification_code()

        # Store in pending_users for verification
        user_id = user['user_id']
        
        # Send verification email
        from email_service import send_verification_email
        send_verification_email(user['email'], code, user.get('first_name', ''))
        
        # Redirect to verify page where user enters code
        return redirect(url_for('auth.verify', user_id=user_id))

    return render_template('login.html', csrf_token=_get_or_create_csrf_token())


@auth_bp.route('/verify')
def verify():
    """Verification code entry page"""
    user_id = request.args.get('user_id')

    if not user_id:
        return redirect(url_for('auth.register'))

    user_data = get_pending_user(user_id)
    if not user_data:
        return render_template('register_simple.html',
                             csrf_token=_get_or_create_csrf_token(),
                             error="Verification session expired. Please register again.")

    # Display email contact (SMS no longer supported)
    contact = mask_contact(user_data['email'], 'email')

    return render_template('verify_code.html',
                         method="email",
                         masked_contact=contact,
                         user_id=user_id,
                         csrf_token=_get_or_create_csrf_token())


@auth_bp.route('/verify', methods=['POST'])
def verify_post():
    """Process verification code"""
    user_id = request.form.get('user_id')
    code = request.form.get('full_code')

    if not user_id or not code:
        return redirect(url_for('auth.register'))

    # Verify the code
    success, error = verify_code(user_id, code)

    if success:
        # Code verified - create session
        user_data = get_pending_user(user_id)
        
        session['user_id'] = user_id
        session['verified'] = True
        session['user_name'] = f"{user_data['first_name']} {user_data['last_name']}"

        log_event("user_verified", {
            "user_id": user_id,
            "email": user_data['email']
        })

        # Redirect to dashboard
        return redirect(url_for('dashboard'))
    else:
        # Show error on verification page
        user_data = get_pending_user(user_id)
        if not user_data:
            return redirect(url_for('auth.register'))

        # Display email contact (SMS no longer supported)
        contact = mask_contact(user_data['email'], 'email')

        return render_template('verify_code.html',
                             method="email",
                             masked_contact=contact,
                             user_id=user_id,
                             error=error,
                             csrf_token=_get_or_create_csrf_token())


@auth_bp.route('/resend-code', methods=['POST'])
def resend_code():
    """Resend verification code"""
    user_id = request.form.get('user_id')

    if not user_id:
        return redirect(url_for('auth.register'))

    success, code, _error = resend_verification_code(user_id)

    if success:
        # Send new verification code via email
        user_data = get_pending_user(user_id)
        from email_service import send_verification_email
        send_verification_email(user_data['email'], code, user_data['first_name'])
        
        print(f"Resent verification code for {user_id}: {code}")
        log_event("verification_code_resent", {"user_id": user_id})

        # Show success message on verify page
        method = user_data.get('verification_method', 'email')
        contact = mask_contact(user_data['email'], 'email')

        return render_template('verify_code.html',
                             method="email",
                             masked_contact=contact,
                             user_id=user_id,
                             success="New code sent!",
                             csrf_token=_get_or_create_csrf_token())
    else:
        return redirect(url_for('auth.register'))


@auth_bp.route('/recover')
def recover():
    """Token recovery page"""
    return render_template('token_recovery.html')
