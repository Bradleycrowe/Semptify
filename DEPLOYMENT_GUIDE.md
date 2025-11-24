# 🚀 DEPLOYMENT GUIDE - Semptify Production

## Quick Deploy to Render.com

### Prerequisites
- GitHub account (to link repository)
- Render.com account (free tier works)
- Admin tokens generated

### Step-by-Step Deployment

#### 1. Prepare Repository
`powershell
# Initialize Git (if not already)
git init
git add .
git commit -m "Initial production deployment"

# Push to GitHub
git remote add origin https://github.com/yourusername/semptify.git
git push -u origin main
`

#### 2. Configure Render.com
1. Go to https://render.com/dashboard
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Render will auto-detect ender.yaml

#### 3. Set Environment Variables (Render Dashboard)
**Required:**
- FLASK_SECRET_KEY - Generate with: python -c "import secrets; print(secrets.token_hex(32))"
- SECURITY_MODE - Set to nforced for production
- ADMIN_TOKEN - Your admin token hash (from security/admin_tokens.json)

**Optional:**
- DATABASE_URL - If using Postgres instead of SQLite
- AI_PROVIDER - Set to openai, zure, or ollama
- OPENAI_API_KEY - If using OpenAI for AI features
- AZURE_OPENAI_KEY - If using Azure OpenAI
- GITHUB_TOKEN - For release management features

#### 4. Deploy
- Click "Create Web Service"
- Render will:
  1. Install dependencies from equirements.txt
  2. Run python run_prod.py (waitress server)
  3. Expose service at https://semptify-prod.onrender.com

#### 5. Verify Deployment
`ash
# Check health endpoint
curl https://semptify-prod.onrender.com/readyz

# Test Context API
curl https://semptify-prod.onrender.com/api/context/1

# Test Complaint API
curl https://semptify-prod.onrender.com/api/complaint/1/auto-fill
`

---

## Manual Deployment (VPS / Cloud Server)

### Ubuntu/Debian Server

#### 1. Install Dependencies
`ash
sudo apt update
sudo apt install python3.14 python3-pip git -y
`

#### 2. Clone Repository
`ash
git clone https://github.com/yourusername/semptify.git
cd semptify
`

#### 3. Set Up Python Environment
`ash
python3.14 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
`

#### 4. Configure Environment
`ash
cp config.env.template .env
nano .env  # Edit with your production values
`

#### 5. Initialize Database
`ash
python -c "from user_database import init_database, init_remember_tokens_table; init_database(); init_remember_tokens_table()"
`

#### 6. Start Production Server
`ash
python run_prod.py
`

#### 7. Set Up as System Service (systemd)
`ash
sudo nano /etc/systemd/system/semptify.service
`

`ini
[Unit]
Description=Semptify Production Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/semptify
Environment="PATH=/path/to/semptify/.venv/bin"
ExecStart=/path/to/semptify/.venv/bin/python run_prod.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
`

`ash
sudo systemctl daemon-reload
sudo systemctl enable semptify
sudo systemctl start semptify
sudo systemctl status semptify
`

#### 8. Configure Nginx (Reverse Proxy)
`ash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/semptify
`

`
ginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host \System.Management.Automation.Internal.Host.InternalHost;
        proxy_set_header X-Real-IP \;
        proxy_set_header X-Forwarded-For \;
        proxy_set_header X-Forwarded-Proto \;
    }

    client_max_body_size 100M;
}
`

`ash
sudo ln -s /etc/nginx/sites-available/semptify /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
`

#### 9. Set Up SSL (Let's Encrypt)
`ash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
`

---

## Post-Deployment Tasks

### 1. Database Backup (Automated)
`ash
# Add to crontab for daily backups at 2 AM
crontab -e
`

Add line:
`
0 2 * * * cd /path/to/semptify && /path/to/semptify/.venv/bin/python database_backup.py scheduled
`

### 2. Monitor Logs
`ash
# Application logs
tail -f logs/application.log

# Error logs
tail -f logs/errors.log

# Security logs
tail -f logs/security.log
`

### 3. Test All Features
- [ ] User registration
- [ ] Document upload
- [ ] Context API
- [ ] Perspective analysis
- [ ] Complaint auto-fill
- [ ] Evidence ranking
- [ ] Court packet generation

### 4. Set Up Monitoring
- Configure uptime monitoring (e.g., UptimeRobot)
- Set up error alerting (email/Slack)
- Monitor disk space for uploads
- Monitor database size

---

## Troubleshooting

### Issue: Context API returns 404
**Solution:** Check that blueprint registration is before if __name__ == '__main__' in Semptify.py

### Issue: Database locked errors
**Solution:** Use Postgres instead of SQLite for concurrent users, or ensure only one process accesses SQLite

### Issue: Upload directory not writable
**Solution:**
`ash
chmod 755 uploads/
chown -R www-data:www-data uploads/
`

### Issue: Memory errors on Render free tier
**Solution:** Reduce SEMPTIFY_WORKERS to 2 and SEMPTIFY_THREADS to 1 in environment variables

---

## Rollback Procedure

### If Deployment Fails:
1. Check logs in Render dashboard or server logs
2. Verify environment variables are set correctly
3. Restore previous database backup:
   `ash
   python database_backup.py restore backups/database/users_backup_YYYYMMDD_HHMMSS.db
   `
4. Revert to previous Git commit:
   `ash
   git revert HEAD
   git push
   `

---

## Production Checklist

Before going live:
- [ ] All environment variables set
- [ ] SECURITY_MODE=enforced
- [ ] Admin tokens configured
- [ ] Database initialized
- [ ] Backup script scheduled
- [ ] Logs directory writable
- [ ] Health check endpoint responding
- [ ] All 8 API endpoints tested
- [ ] SSL certificate configured
- [ ] Monitoring set up
- [ ] Error alerting configured

---

## Security Hardening

### 1. Admin Token Management
- Store tokens in security/admin_tokens.json (SHA-256 hashed)
- Never commit tokens to Git
- Rotate tokens every 90 days
- Enable break-glass procedure for emergencies

### 2. Rate Limiting
- Configure ADMIN_RATE_WINDOW and ADMIN_RATE_MAX
- Monitor logs/security.log for rate limit violations
- Adjust limits based on legitimate usage patterns

### 3. CSRF Protection
- Enabled automatically in nforced mode
- Ensure all POST routes include CSRF token
- Test with real forms after deployment

### 4. File Upload Security
- Maximum upload size: 100MB (configurable)
- Allowed file types validated
- Files stored outside web root
- Virus scanning recommended for production

---

## Support

**Documentation:**
- BUILD_LOGBOOK.md - Complete project history
- MVP_COMPLETION_REPORT.md - Feature summary
- POST_MVP_FEATURES.md - Future roadmap

**Monitoring:**
- Health check: https://your-domain.com/readyz
- Metrics: https://your-domain.com/metrics

**Backup Location:**
- Local: ackups/database/
- Keep 30 days of daily backups

**Next Steps:**
1. Deploy to Render.com (5 minutes)
2. Configure domain (10 minutes)
3. Test with real users (1 hour)
4. Monitor for 24 hours
5. Iterate based on feedback

🚀 You're ready to deploy!