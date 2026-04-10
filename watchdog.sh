#!/bin/bash
# Watchdog script: runs the image collector in a loop until all 544 players are done.
# Runs inside tmux so it survives session disconnects.

CSV="players.csv"
OUTPUT="outputs"
TARGET=544
DELAY=1.5

echo "=================================================="
echo "  Image Collector Watchdog"
echo "  Target: $TARGET images"
echo "  Auto-restarts on failure or timeout"
echo "=================================================="
echo ""

while true; do
    # Count current images
    CURRENT=$(find "$OUTPUT" -name "*.jpg" 2>/dev/null | wc -l)
    echo "[$(date '+%H:%M:%S')] Current images: $CURRENT / $TARGET"

    if [ "$CURRENT" -ge "$TARGET" ]; then
        echo ""
        echo "ALL $TARGET IMAGES DOWNLOADED!"
        echo "Collection complete at $(date)"
        echo ""
        # Show summary
        if [ -f "collection_summary.txt" ]; then
            cat collection_summary.txt
        fi
        break
    fi

    echo "[$(date '+%H:%M:%S')] Starting collection run..."
    python collect_images.py --csv "$CSV" --output "$OUTPUT" --skip-existing --delay "$DELAY"
    EXIT_CODE=$?

    # Count again after run
    NEW_COUNT=$(find "$OUTPUT" -name "*.jpg" 2>/dev/null | wc -l)
    echo "[$(date '+%H:%M:%S')] Run finished (exit $EXIT_CODE). Images: $NEW_COUNT / $TARGET"

    if [ "$NEW_COUNT" -ge "$TARGET" ]; then
        echo ""
        echo "ALL $TARGET IMAGES DOWNLOADED!"
        echo "Collection complete at $(date)"
        break
    fi

    if [ "$NEW_COUNT" -eq "$CURRENT" ]; then
        echo "[$(date '+%H:%M:%S')] No new images this run. Waiting 30s before retry..."
        sleep 30
    else
        echo "[$(date '+%H:%M:%S')] Got $((NEW_COUNT - CURRENT)) new images. Restarting immediately..."
        sleep 2
    fi
done
