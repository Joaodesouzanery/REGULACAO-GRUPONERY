#!/bin/bash
# Instala um agendamento semanal (segunda-feira 09:00) no Mac usando launchd. Desinstalar: launchctl unload ~/Library/LaunchAgents/br.antt.monitor.plist
REPO="$(cd "$(dirname "$0")/.." && pwd)"
PLIST="$HOME/Library/LaunchAgents/br.antt.monitor.plist"
mkdir -p "$HOME/Library/LaunchAgents"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>br.antt.monitor</string>
<key>ProgramArguments</key><array><string>/bin/bash</string><string>$REPO/pipeline/monitorar.sh</string></array>
<key>StartCalendarInterval</key><dict><key>Weekday</key><integer>1</integer><key>Hour</key><integer>9</integer><key>Minute</key><integer>0</integer></dict>
<key>StandardOutPath</key><string>$REPO/data/monitor.log</string><key>StandardErrorPath</key><string>$REPO/data/monitor.log</string>
</dict></plist>
EOF
launchctl unload "$PLIST" 2>/dev/null; launchctl load "$PLIST" && echo "Agendado: toda segunda 09:00 (o Mac precisa estar ligado/acordado). Log: $REPO/data/monitor.log"
