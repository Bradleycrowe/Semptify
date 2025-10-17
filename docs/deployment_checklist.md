# Deployment Checklist for SemptifyGUI

This checklist helps ensure SemptifyGUI is configured correctly for Render (or similar) deployments.

## 1. Environment variables (required)
- SECURITY_MODE (open|enforced)
- FLASK_SECRET
- ADMIN_TOKEN (legacy bootstrap)
- GITHUB_TOKEN (optional - for release/tagging)
- AI_PROVIDER (openai|azure|ollama) and provider keys (e.g., OPENAI_API_KEY, AZURE_API_KEY)
- RON_WEBHOOK_SECRET, BLUENOTARY_API_KEY, BLUENOTARY_BASE_URL
- SEMPTIFY_PORT or PORT
- SEMPTIFY_HOST (optional)
- DEV_SSL_CERT, DEV_SSL_KEY (for dev SSL)
- TESTING (use `1` to enable test/mocked behavior)
- ADMIN_RATE_WINDOW, ADMIN_RATE_MAX, ADMIN_RATE_STATUS, ADMIN_RATE_RETRY_AFTER
- LOG_MAX_BYTES
- SEMPTIFY_DATA_ROOT (optional)

## 2. Files & writable paths
- Ensure the following directories exist and are writable by the app at runtime:
  - `uploads/`
  - `logs/`
  - `copilot_sync/`
  - `final_notices/`
  - `security/` (do not commit secrets inside; use Render secrets)

Note: On Render, the repository directory is generally writable for short term but use persistent storage or object storage for long-term file retention.

## 3. Secrets and Tokens
- Use Render's Secrets/Environment features to store tokens and API keys.
- Never commit secrets into `security/` or the repo.

## 4. Service integrations
- If you enable GitHub release functionality, set `GITHUB_TOKEN` with repo scope for tags.
- For Copilot/AI, set `AI_PROVIDER` plus provider-specific keys.
- For RON/Notary provider, ensure `BLUENOTARY_API_KEY` and `BLUENOTARY_BASE_URL` are configured.

## 5. Pre-deploy checklist
1. Add all required env vars to Render (see section 1).
2. Ensure runtime dirs exist and are writable; app will create them on startup but verify.
3. Verify `FLASK_SECRET` is set for session security.
4. If using forced HTTPS in-app redirects, ensure SSL cert/key are provided or disable for Render-managed TLS.
5. Run tests locally with `TESTING=1` and confirm behavior.

## 6. Post-deploy verification
- Hit `/readyz` and `/healthz` to confirm readiness and health.
- Check logs for any warnings about missing env vars or non-writable directories.
- Verify admin pages if `SECURITY_MODE=enforced` by testing an admin token.

## 7. Rollback & Upgrade notes
- Keep a backup of `security/admin_tokens.json` if rotating tokens (but do NOT commit it).
- When changing AI or external providers, add new env vars and ensure backward compatibility by keeping mock/testing fallbacks.

## 8. Contact & Documentation
- Update this file when adding new external integrations.
