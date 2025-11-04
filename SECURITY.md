# Security Policy & Best Practices for Semptify

## Overview

Semptify is a Flask-based legal/tenancy application handling sensitive user data and administrative functions. This document outlines security practices, token management, and remediation guidelines.

---

## 1. Secrets Management

### ✅ What is NOT stored in git

- API keys (Render, GitHub, etc.)
- CSRF tokens (`security/csrf.token`)
- Admin tokens (`security/admin_tokens.json` — runtime-generated)
- User tokens (`security/users.json` — runtime-generated)
- Private keys and certificates
- Database credentials
- All files under `security/` directory (see `.gitignore`)

### ✅ How to configure secrets locally & in production

#### Local Development

1. Copy the example file:
   ```bash
   cp security/render.env.example security/render.env
   ```
2. Fill in your development values:
   ```
   RENDER_API_KEY=dev_key_here (or leave blank if not needed)
   FLASK_SECRET=your-dev-secret
   ADMIN_TOKEN=your-dev-admin-token
   GITHUB_OWNER=YourGitHubUsername
   GITHUB_REPO=YourRepoName
   ```
3. Never commit `security/render.env` (it's in `.gitignore`).

#### Production (Render or other hosting)

- Use the hosting provider's **Secrets/Environment panel** (not `.env` files).
- For **Render**: Go to Dashboard → Service → Environment → Add secret variables.
- Example production vars:
  ```
  FLASK_SECRET=<long-random-string>
  ADMIN_TOKEN=<strong-random-token>
  GITHUB_TOKEN=<personal-access-token>
  RENDER_API_KEY=<render-api-key>
  ```
- Do **not** use `.env` files in production; use provider-native secrets.

---

## 2. Admin Token Management

### Token Storage & Validation

- **File**: `security/admin_tokens.json` (created at runtime, not in git).
- **Format**: JSON dict of token → metadata (hash, created_ts, breakglass flag).
- **Validation logic** (`security/__init__.py`):
  - Checks token against `admin_tokens.json` (hashed or plaintext).
  - Falls back to legacy `ADMIN_TOKEN` env var (if explicitly provided).
  - Supports breakglass one-shot tokens (consume immediately after use).
  - Rate-limits admin requests via sliding window (`ADMIN_RATE_WINDOW`, `ADMIN_RATE_MAX`).

### Creating Admin Tokens

Use the helper script:
```bash
python tools/create_admin_token.py
```
This generates a new token and stores its hash in `security/admin_tokens.json`.

For breakglass (emergency access):
```bash
python tools/create_admin_token.py --breakglass
```
Breakglass tokens can only be used once, then the flag is consumed.

### Token Rotation

1. Generate a new token (see above).
2. Update your deployment secrets to use the new token.
3. Remove old tokens from `security/admin_tokens.json` (or mark as `enabled: false`).
4. Monitor `logs/events.log` for `token_rotation` events.

### Breakglass Protocol

- **Create**: Run `create_admin_token.py --breakglass` (generates a one-shot token).
- **Use**: Pass token via `?token=<token>` or `X-Admin-Token` header.
- **Result**: Token is consumed (breakglass flag set to false), and `logs/events.log` logs `breakglass_used`.
- **Policy**: Limit who can generate breakglass tokens; log and review all uses.

---

## 3. CSRF Protection

### How it works

- **Token file**: `security/csrf.token` (created at startup, not in git).
- **Per-request**: Flask session stores a copy (in-memory or cookie-based).
- **Enforcement**: In `SECURITY_MODE=enforced`, all state-changing POSTs (forms) require a matching CSRF token.
- **Bypass**: In `SECURITY_MODE=open`, CSRF is not enforced (for testing).

### Implementing CSRF in forms
```html
<form method="POST" action="/some-endpoint">
  <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
  <!-- form fields -->
  <button type="submit">Submit</button>
</form>
```

### Modes

- `SECURITY_MODE=open` (default in dev): CSRF not enforced; useful for testing.
- `SECURITY_MODE=enforced` (production): CSRF enforced on state-changing routes.

---

## 4. User Token Flow

### Registration (Sign-up)

1. User visits `/register` → gets a form with CSRF token.
2. User submits → new anonymous token is generated and hashed.
3. Token hash stored in `security/users.json`.
4. User shown one-time token and link: `/vault?user_token=<token>`.
5. User bookmarks link or saves token for later access.

### Vault Access
- User can authenticate via:
  - `?user_token=<token>` (URL param)
  - `X-User-Token: <token>` (header)
  - Form field `user_token`
- Token is validated against `security/users.json` (hashed comparison).

### Token Disablement
- If a user's account needs to be revoked, set `enabled: false` in their entry in `security/users.json`.
- Tokens can also be time-limited (add `expires_ts` field).

---

## 5. Logging & Monitoring

### Events Log

- **File**: `logs/events.log` (JSON Lines format, rotated).
- **Contents**: All security events (token usage, breakglass, rate limits, errors).
- **Example entry**:
  ```json
  {"ts": 1699123456.789, "event": "breakglass_used", "payload": {"ip": "192.168.1.1"}}
  ```

### Metrics
- **Endpoint**: `/metrics` (Prometheus format).
- **Key metrics**:
  - `requests_total` — total HTTP requests.
  - `admin_requests_total` — admin endpoint hits.
  - `breakglass_used_total` — breakglass token uses.
  - `rate_limited_total` — rate-limit denials.
  - `errors_total` — application errors.

### Alerting
- Monitor `logs/events.log` for repeated `rate_limited` events (DDoS or brute-force attempt).
- Alert if `breakglass_used_total` increases unexpectedly (emergency access was triggered).
- Monitor `/readyz` endpoint; if it returns `degraded`, investigate token/user file I/O issues.

---

## 6. Pre-commit & CI Checks

### Pre-commit Hooks
The repo uses `.pre-commit-config.yaml` to automatically check for:
- **Secrets**: `detect-secrets` scans for leaked API keys, tokens, private keys.
- **Bandit**: Python security linter (detects unsafe code patterns).
- **Ruff**: Fast Python linter & formatter.
- **Private keys**: Detects private key files accidentally staged.

### Setup pre-commit (local)
```bash
pip install pre-commit
pre-commit install
```

### Run manually (before committing)
```bash
pre-commit run --all-files
```

### CI Workflow
- GitHub Actions (if configured) runs the same checks on PRs.
- Any new secrets or security issues block the merge.

---

## 7. Incident Response

### If a secret is accidentally committed (locally)

1. **Do not push**. Immediately:
   ```bash
   git reset HEAD <file>
   git checkout -- <file>
   ```
2. Add to `.gitignore` if not already there.
3. Rotate the secret.
4. Proceed with normal development.

### If a secret is pushed to a remote branch (GitHub)

1. **Immediately rotate the secret** (in your provider's dashboard).
2. Remove the file from the branch:
   ```bash
   git rm --cached <file>
   git commit -m "Remove leaked secret"
   git push
   ```
3. (Optional) Purge from history using `git filter-repo` or BFG (destructive; requires force-push coordination).
4. Add audit log entry and notify infra team.

### If breakglass tokens are overused

1. Review `logs/events.log` for `breakglass_used` entries.
2. Identify who triggered them (check `request_id`, IP).
3. Audit admin activity during those windows.
4. Rotate breakglass tokens and all admin tokens.
5. Update access control / RBAC to prevent future abuse.

---

## 8. Best Practices Checklist

- [ ] Never commit secrets to git (use `.gitignore`, pre-commit hooks).
- [ ] Use `security/render.env.example` as a template; fill in locally, never commit the actual file.
- [ ] In production, use the hosting provider's secrets panel (not `.env`).
- [ ] Rotate admin tokens at least quarterly or after any suspected compromise.
- [ ] Test breakglass flow in staging before relying on it in production.
- [ ] Monitor `/metrics` and `logs/events.log` for anomalies (rate limits, breakglass use, errors).
- [ ] Enforce CSRF on all state-changing endpoints (`SECURITY_MODE=enforced` in prod).
- [ ] Use strong, random tokens (generate with `secrets.token_urlsafe(32)` or use tool).
- [ ] Document token rotation steps and communicate them to ops/security teams.
- [ ] Review pre-commit configuration and CI workflows regularly.

---

## 9. References

- **Admin token creation**: `tools/create_admin_token.py`
- **Security module**: `security/__init__.py` (validate_admin_token, is_breakglass_active, etc.)
- **Config file**: `.pre-commit-config.yaml` (secret detection, bandit, ruff)
- **Example env**: `security/render.env.example`
- **Logs**: `logs/events.log` (JSON events), `logs/init.log` (startup)
- **Metrics**: `/metrics` endpoint (Prometheus format)

---

## Questions or Security Issues?

If you discover a security vulnerability:
1. **Do not** open a public issue on GitHub.
2. Contact the maintainer privately (see `README.md` for contact).
3. Provide details: what was found, where, potential impact, reproduction steps.

---

**Last Updated**: 2025-11-03
**Status**: Active & Enforced
