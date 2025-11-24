# Remove sensitive files from git tracking (keeps local files)
git rm --cached users.db
git rm --cached logs/events.log
git rm --cached -r security/
git rm --cached data/learning_patterns.json
git rm --cached data/admin_config.json

# Add the production template
git add .env.production.template

# Verify what will be committed
git status --short
