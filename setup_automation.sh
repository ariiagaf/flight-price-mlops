#!/bin/bash

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
INTERVAL_SECONDS=300

if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Setting up automation with launchd..."

    PLIST_PATH="$HOME/Library/LaunchAgents/com.flightprice.pipeline.plist"

    mkdir -p "$HOME/Library/LaunchAgents"

    cat > "$PLIST_PATH" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">

<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.flightprice.pipeline</string>

    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$PROJECT_DIR/run_pipeline.sh</string>
    </array>

    <key>WorkingDirectory</key>
    <string>$PROJECT_DIR</string>

    <key>StartInterval</key>
    <integer>$INTERVAL_SECONDS</integer>

    <key>StandardOutPath</key>
    <string>$PROJECT_DIR/pipeline.log</string>

    <key>StandardErrorPath</key>
    <string>$PROJECT_DIR/pipeline_error.log</string>
</dict>
</plist>
EOF

    launchctl bootout gui/$(id -u) "$PLIST_PATH" 2>/dev/null || true
    launchctl bootstrap gui/$(id -u) "$PLIST_PATH"

    echo "Automation installed successfully."
    echo "Pipeline will run every 5 minutes."

elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Setting up automation with cron..."

    CRON_JOB="*/5 * * * * cd \"$PROJECT_DIR\" && /bin/bash \"$PROJECT_DIR/run_pipeline.sh\" >> \"$PROJECT_DIR/pipeline.log\" 2>&1"

    (
        crontab -l 2>/dev/null | grep -v "flight-price-mlops/run_pipeline.sh" || true
        echo "$CRON_JOB"
    ) | crontab -

    echo "Automation installed successfully."
    echo "Pipeline will run every 5 minutes."

else
    echo "Unsupported operating system."
    exit 1
fi