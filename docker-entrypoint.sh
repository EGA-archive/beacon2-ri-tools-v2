#!/bin/sh
set -e

echo "ENTRYPOINT STARTED"

MARKER=/opt/refgen-data/.initialized

if [ ! -f "$MARKER" ]; then
    echo "Downloading refgenDetector needed files..."

    mkdir -p /opt/refgen-data

    for i in 1 2 3; do
        echo "Attempt $i"
        if refgenDetector -h; then
            touch "$MARKER"
            echo "Download successful"
            break
        fi
        echo "Failed, retrying..."
        sleep 5
    done
else
    echo "Already initialized"
fi

exec "$@"