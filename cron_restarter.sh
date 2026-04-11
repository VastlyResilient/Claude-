#!/bin/bash
# Cron-based auto-restarter for the image collector.
# Runs every minute via cron. If the collector isn't running, starts it.

LOGFILE="/home/user/Claude-/watchdog.log"
PIDFILE="/home/user/Claude-/collector.pid"
WORKDIR="/home/user/Claude-"
TARGET=544

cd "$WORKDIR" || exit 1

# Count current images
CURRENT=$(find outputs -name "*.jpg" 2>/dev/null | wc -l)

# Already done?
if [ "$CURRENT" -ge "$TARGET" ]; then
    echo "[$(date '+%H:%M:%S')] DONE - $CURRENT/$TARGET images" >> "$LOGFILE"
    exit 0
fi

# Is collector already running?
if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    if kill -0 "$PID" 2>/dev/null; then
        # Still running, do nothing
        exit 0
    fi
fi

# Not running — start it
echo "[$(date '+%H:%M:%S')] Cron restart: $CURRENT/$TARGET images. Starting collector..." >> "$LOGFILE"
nohup python3 collect_images.py --csv players.csv --output outputs --skip-existing --delay 1.5 >> "$LOGFILE" 2>&1 &
echo $! > "$PIDFILE"
