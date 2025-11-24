# 🚀 PRODUCTION DEPLOYMENT CHECKLIST

## Pre-Deployment (Complete Before Deploy)

### 1. Environment Configuration ✓
- [x] Review .env.production.template
- [ ] Create actual .env file with secrets
- [ ] Generate FLASK_SECRET_KEY (32+ random chars)
- [ ] Set SECURITY_MODE=enforced
- [ ] Configure ADMIN_RATE_WINDOW and ADMIN_RATE_MAX

### 2. Admin Tokens ✓
- [ ] Run: `python create_admin_token.py`
- [ ] Save token securely (1Password, secrets manager)
- [ ] Verify security/admin_tokens.json created
- [ ] Test token validation with test request

### 3. Database Setup ✓
- [x] users.db exists with schema
- [ ] Create database backup script
- [ ] Set up automated backups (daily)
- [ ] Test database migrations (if any)

### 4. Security Audit ✓
- [x] CSRF protection enabled (enforced mode)
- [x] Rate limiting configured
- [x] File upload restrictions in place
- [ ] Review security/users.json permissions
- [ ] Verify no secrets in code

### 5. File Permissions ✓
- [ ] uploads/ directory writable
- [ ] logs/ directory writable
- [ ] security/ directory read-only (except admin_tokens.json)
- [ ] data/ directory writable (for learning patterns)

### 6. Testing ✓
- [x] All pytest tests passing
- [x] Context API operational
- [x] Complaint filing integration working
- [ ] Load testing (100 concurrent users)
- [ ] Edge case testing (large files, malformed data)

## Render.com Deployment

### 7. Render Configuration
- [ ] Create new Web Service on Render.com
- [ ] Set Build Command: `pip install -r requirements.txt`
- [ ] Set Start Command: `python run_prod.py`
- [ ] Set Environment: Python 3.14
- [ ] Configure environment variables from .env.production.template

### 8. Environment Variables (Set in Render Dashboard)
Critical:
- [ ] FLASK_SECRET_KEY
- [ ] SECURITY_MODE=enforced
- [ ] DATABASE_URL (if using Postgres instead of SQLite)

Optional:
- [ ] AI_PROVIDER + API keys (for Copilot features)
- [ ] CF_ACCOUNT_ID + CF_API_TOKEN (for R2 storage)
- [ ] SMTP credentials (for email notifications)

### 9. Domain & SSL
- [ ] Add custom domain (if available)
- [ ] SSL certificate auto-provisioned by Render
- [ ] Test HTTPS redirect
- [ ] Update TOS_URL and PRIVACY_URL

### 10. Monitoring Setup
- [ ] Enable Render health checks (/readyz endpoint)
- [ ] Set up uptime monitoring (UptimeRobot, Pingdom)
- [ ] Configure error alerting
- [ ] Set up log aggregation (optional)

## Post-Deployment Verification

### 11. Smoke Tests
- [ ] Homepage loads: GET /
- [ ] Registration works: GET /register
- [ ] Vault accessible: GET /vault (with token)
- [ ] Context API: GET /api/context/1
- [ ] Complaint API: GET /api/complaint/1/auto-fill
- [ ] Health check: GET /readyz returns 200

### 12. User Acceptance Testing
- [ ] Create test user account
- [ ] Upload sample lease document
- [ ] Verify document intelligence extraction
- [ ] Check perspective analysis
- [ ] Test auto-fill complaint form
- [ ] Generate court packet
- [ ] Verify timeline tracking

### 13. Performance Validation
- [ ] Page load time < 2 seconds
- [ ] API response time < 500ms
- [ ] Document upload < 5 seconds
- [ ] Perspective analysis < 3 seconds
- [ ] No memory leaks (monitor for 24 hours)

### 14. Security Validation
- [ ] Test rate limiting (10+ requests in 1 hour)
- [ ] Verify CSRF protection on POST routes
- [ ] Test file upload restrictions (try .exe, .sh)
- [ ] Verify admin token required for /admin/*
- [ ] Check user token isolation (user 1 can't access user 2 data)

## Ongoing Maintenance

### 15. Backup Strategy
- [ ] Daily database backups to S3/R2
- [ ] Weekly full system backup
- [ ] Test restore procedure
- [ ] Retention: 30 days daily, 12 months weekly

### 16. Monitoring
- [ ] Daily health check review
- [ ] Weekly error log review
- [ ] Monthly performance analysis
- [ ] User feedback collection

### 17. Updates
- [ ] Security patches: Apply within 7 days
- [ ] Dependency updates: Monthly review
- [ ] Feature releases: Every 2 weeks
- [ ] Documentation updates: With each release

## Rollback Plan

If deployment fails:
1. Revert to previous Render deployment (1-click)
2. Restore database from last backup
3. Verify rollback with smoke tests
4. Investigate issue in staging environment
5. Document root cause

## Success Metrics (Week 1)

- [ ] 0 critical bugs
- [ ] 99% uptime
- [ ] < 1 second median API response time
- [ ] 10+ user registrations
- [ ] 50+ documents analyzed
- [ ] 20+ complaints filed

## Next Steps After Launch

1. Monitor for 48 hours continuously
2. Gather user feedback
3. Fix any critical bugs immediately
4. Plan Sprint 2 features (attorney directory, calendar sync)
5. Celebrate! 🎉

---

**Estimated Total Time:** 2-3 hours
**Current Progress:** Pre-deployment checks in progress
**Blocker Status:** None
**Ready to Deploy:** Pending checklist completion
