# Admin Token Manual

## Overview
This manual provides instructions for managing admin tokens, including resetting tokens and initiating break-glass procedures. Admin tokens are designed to never expire, ensuring uninterrupted access for administrators.

---

## Token Management

### Generating Tokens
- Admin tokens are generated using a secure random generator.
- Tokens are hashed before storage to ensure security.

### Token Expiry
- **Admin Tokens**: Never expire.
- **User Tokens**: Expire after 24 hours.

---

## Resetting Tokens

### Regular Reset
1. Access the admin panel.
2. Navigate to the "Token Management" section.
3. Select the token to reset.
4. Confirm the reset action.

### Break-Glass Procedure
If the admin token is lost or compromised:
1. **Initiate Break-Glass**:
   - Create a `breakglass.flag` file in the `security/` directory.
   - Use the following command:
     ```bash
     touch security/breakglass.flag
     ```
2. **Authenticate with Break-Glass Token**:
   - Use a pre-configured break-glass token to regain access.
3. **Reset Admin Token**:
   - Generate a new admin token and replace the compromised one.

---

## Security Best Practices
- Store tokens securely and avoid sharing them.
- Regularly monitor token usage for suspicious activity.
- Use the break-glass procedure only in emergencies.

---

## Contact
For further assistance, contact the system administrator.