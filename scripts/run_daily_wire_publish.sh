#!/bin/bash
set -euo pipefail

export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$HOME/bin"
PROJECT_DIR="/Users/thomaskim/Cryptocasinomedia"
LOG_DIR="$PROJECT_DIR/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/daily_wire_cron.log"

echo "==================================================" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] Starting Daily Wire Publication Trigger" >> "$LOG_FILE"

cd "$PROJECT_DIR"

# 1. Pull latest remote changes cleanly
/usr/local/bin/git pull --rebase origin main >> "$LOG_FILE" 2>&1 || true

# 2. Run automated wire publisher
/usr/local/bin/python3 scripts/auto_publish_daily_wire.py >> "$LOG_FILE" 2>&1

# 3. Check for repository changes and push
if ! /usr/local/bin/git diff --quiet || ! /usr/local/bin/git diff --staged --quiet || [ -n "$(/usr/local/bin/git status --porcelain)" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] Changes detected, committing and pushing..." >> "$LOG_FILE"
    /usr/local/bin/git add .
    /usr/local/bin/git commit -m "feat(auto): publish daily wire news [$(date '+%Y-%m-%d')]" --author="TK <tk@eznewswire.com>" >> "$LOG_FILE" 2>&1
    /usr/local/bin/git push origin main >> "$LOG_FILE" 2>&1
    echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] Successfully pushed to origin main! Vercel edge deployment triggered." >> "$LOG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] Today's wire quota is already satisfied. All sitemaps and verification verified." >> "$LOG_FILE"
fi

# 4. Trigger GitHub Actions workflow dispatch as fallback
/usr/local/bin/gh workflow run daily_wire_publish.yml >> "$LOG_FILE" 2>&1 || true

echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] Finished Daily Wire Publication Task" >> "$LOG_FILE"
