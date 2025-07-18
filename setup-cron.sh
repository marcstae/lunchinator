#!/bin/bash

# Cron Job Setup Script for Eurest Menu Auto-Deployment
# This script sets up a cron job to automatically deploy menu updates

set -e

# Configuration
SCRIPT_DIR="/opt/eurest-menu"
DEPLOY_SCRIPT="$SCRIPT_DIR/deploy-menu.sh"
CRON_LOG="/var/log/eurest-menu-cron.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
}

warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

# Check if running as root
check_permissions() {
    if [[ $EUID -ne 0 ]]; then
        error "This script must be run as root or with sudo"
        exit 1
    fi
}

# Setup directory and copy scripts
setup_scripts() {
    log "Setting up deployment scripts..."
    
    # Create directory
    mkdir -p "$SCRIPT_DIR"
    
    # Copy deployment script
    if [ -f "./deploy-menu.sh" ]; then
        cp "./deploy-menu.sh" "$DEPLOY_SCRIPT"
        chmod +x "$DEPLOY_SCRIPT"
        log "Deployment script copied to $DEPLOY_SCRIPT"
    else
        error "deploy-menu.sh not found in current directory"
        exit 1
    fi
    
    # Create log file
    touch "$CRON_LOG"
    chmod 644 "$CRON_LOG"
}

# Setup cron job
setup_cron() {
    log "Setting up cron job..."
    
    # Cron job configuration
    # Runs every hour during lunch hours (11:00-14:00) on weekdays
    CRON_SCHEDULE="0 11,12,13,14 * * 1-5"
    CRON_COMMAND="$DEPLOY_SCRIPT >> $CRON_LOG 2>&1"
    CRON_ENTRY="$CRON_SCHEDULE $CRON_COMMAND"
    
    # Add cron job
    (crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
    
    log "Cron job added: $CRON_ENTRY"
    log "This will run every hour from 11:00-14:00 on weekdays"
}

# Create monitoring script
create_monitor() {
    log "Creating monitoring script..."
    
    cat > "$SCRIPT_DIR/monitor-menu.sh" << 'EOF'
#!/bin/bash

# Menu Deployment Monitor
# Check if menu is up-to-date and deployment is working

LOG_FILE="/var/log/eurest-menu-deploy.log"
WEB_ROOT="/var/www/eurest-menu"
ALERT_EMAIL="admin@yourdomain.com"  # Configure your email

check_deployment() {
    echo "=== Menu Deployment Status Check ==="
    echo "Time: $(date)"
    echo
    
    # Check if web root exists
    if [ ! -d "$WEB_ROOT" ]; then
        echo "❌ Web root directory not found: $WEB_ROOT"
        return 1
    fi
    
    # Check if index.html exists
    if [ ! -f "$WEB_ROOT/index.html" ]; then
        echo "❌ index.html not found"
        return 1
    fi
    
    # Check file age
    INDEX_AGE=$(stat -c %Y "$WEB_ROOT/index.html")
    CURRENT_TIME=$(date +%s)
    AGE_HOURS=$(( (CURRENT_TIME - INDEX_AGE) / 3600 ))
    
    echo "📄 index.html age: $AGE_HOURS hours"
    
    if [ $AGE_HOURS -gt 25 ]; then
        echo "⚠️  WARNING: Menu is more than 25 hours old"
        return 1
    fi
    
    # Check deployment info
    if [ -f "$WEB_ROOT/deployment-info.txt" ]; then
        echo "📊 Last deployment info:"
        cat "$WEB_ROOT/deployment-info.txt"
    fi
    
    echo "✅ Menu deployment appears healthy"
    return 0
}

# Run check
if ! check_deployment; then
    echo "❌ Menu deployment check failed"
    
    # Optionally send alert email (requires mail command)
    # echo "Menu deployment check failed on $(hostname)" | mail -s "Eurest Menu Alert" "$ALERT_EMAIL"
    
    exit 1
fi
EOF

    chmod +x "$SCRIPT_DIR/monitor-menu.sh"
    log "Monitor script created: $SCRIPT_DIR/monitor-menu.sh"
}

# Create systemd service (optional)
create_service() {
    log "Creating systemd service..."
    
    cat > "/etc/systemd/system/eurest-menu-deploy.service" << EOF
[Unit]
Description=Eurest Menu Deployment
After=network.target

[Service]
Type=oneshot
ExecStart=$DEPLOY_SCRIPT
User=root
WorkingDirectory=$SCRIPT_DIR

[Install]
WantedBy=multi-user.target
EOF

    cat > "/etc/systemd/system/eurest-menu-deploy.timer" << EOF
[Unit]
Description=Run Eurest Menu Deployment
Requires=eurest-menu-deploy.service

[Timer]
OnCalendar=*-*-* 11,12,13,14:00:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

    systemctl daemon-reload
    systemctl enable eurest-menu-deploy.timer
    systemctl start eurest-menu-deploy.timer
    
    log "Systemd timer created and started"
    log "You can use 'systemctl status eurest-menu-deploy.timer' to check status"
}

# Create logrotate configuration
setup_logrotate() {
    log "Setting up log rotation..."
    
    cat > "/etc/logrotate.d/eurest-menu" << EOF
/var/log/eurest-menu*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 root root
    postrotate
        # No special action needed
    endscript
}
EOF

    log "Logrotate configuration created"
}

# Show usage instructions
show_usage() {
    echo
    log "Setup completed! Here's what was configured:"
    echo
    echo "📁 Scripts location: $SCRIPT_DIR"
    echo "📋 Cron job: Runs hourly during lunch hours (11:00-14:00) on weekdays"
    echo "📊 Logs: $CRON_LOG"
    echo "🔧 Monitor: $SCRIPT_DIR/monitor-menu.sh"
    echo
    echo "Useful commands:"
    echo "  sudo $DEPLOY_SCRIPT                    # Manual deployment"
    echo "  sudo $SCRIPT_DIR/monitor-menu.sh       # Check status"
    echo "  sudo tail -f $CRON_LOG                 # Watch logs"
    echo "  sudo crontab -l                        # View cron jobs"
    echo
    echo "To test the deployment manually:"
    echo "  sudo $DEPLOY_SCRIPT"
    echo
}

main() {
    log "Setting up Eurest Menu auto-deployment..."
    
    check_permissions
    setup_scripts
    setup_cron
    create_monitor
    create_service
    setup_logrotate
    show_usage
    
    log "Setup completed successfully!"
}

# Run main function
main "$@"
