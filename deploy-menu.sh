#!/bin/bash

# Nginx Deployment Script for Eurest Menu Website
# This script downloads the latest release from GitHub and deploys it to nginx

set -e  # Exit on any error

# Configuration
GITHUB_REPO="yourusername/eurest-menu-scraper"  # Replace with your actual repo
NGINX_WEB_ROOT="/var/www/eurest-menu"
TEMP_DIR="/tmp/eurest-menu-deploy"
LOG_FILE="/var/log/eurest-menu-deploy.log"
BACKUP_DIR="/var/backups/eurest-menu"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1" | tee -a "$LOG_FILE"
}

# Check if running as root or with sudo
check_permissions() {
    if [[ $EUID -ne 0 ]]; then
        error "This script must be run as root or with sudo"
        exit 1
    fi
}

# Create necessary directories
setup_directories() {
    log "Setting up directories..."
    
    mkdir -p "$NGINX_WEB_ROOT"
    mkdir -p "$TEMP_DIR"
    mkdir -p "$BACKUP_DIR"
    mkdir -p "$(dirname "$LOG_FILE")"
    
    # Set proper ownership and permissions
    chown -R www-data:www-data "$NGINX_WEB_ROOT"
    chmod -R 755 "$NGINX_WEB_ROOT"
}

# Backup current deployment
backup_current() {
    if [ -d "$NGINX_WEB_ROOT" ] && [ "$(ls -A $NGINX_WEB_ROOT)" ]; then
        log "Backing up current deployment..."
        
        BACKUP_NAME="backup-$(date +%Y%m%d_%H%M%S)"
        mkdir -p "$BACKUP_DIR/$BACKUP_NAME"
        cp -r "$NGINX_WEB_ROOT"/* "$BACKUP_DIR/$BACKUP_NAME/" 2>/dev/null || true
        
        # Keep only last 5 backups
        cd "$BACKUP_DIR"
        ls -t | tail -n +6 | xargs rm -rf 2>/dev/null || true
        
        log "Backup created: $BACKUP_DIR/$BACKUP_NAME"
    fi
}

# Get latest release information
get_latest_release() {
    log "Fetching latest release information..."
    
    # Get latest release tag
    LATEST_TAG=$(curl -s "https://api.github.com/repos/$GITHUB_REPO/releases/latest" | \
                 grep '"tag_name":' | \
                 sed -E 's/.*"([^"]+)".*/\1/')
    
    if [ -z "$LATEST_TAG" ]; then
        error "Could not fetch latest release tag"
        exit 1
    fi
    
    log "Latest release: $LATEST_TAG"
    
    # Construct download URL
    DOWNLOAD_URL="https://github.com/$GITHUB_REPO/releases/download/$LATEST_TAG/eurest-menu-website.tar.gz"
    log "Download URL: $DOWNLOAD_URL"
}

# Download and extract release
download_release() {
    log "Downloading release..."
    
    cd "$TEMP_DIR"
    rm -rf ./* 2>/dev/null || true
    
    # Download the release archive
    if ! curl -L -o "eurest-menu-website.tar.gz" "$DOWNLOAD_URL"; then
        error "Failed to download release"
        exit 1
    fi
    
    # Extract archive
    if ! tar -xzf "eurest-menu-website.tar.gz"; then
        error "Failed to extract release archive"
        exit 1
    fi
    
    log "Release downloaded and extracted successfully"
}

# Validate downloaded content
validate_content() {
    log "Validating downloaded content..."
    
    if [ ! -f "$TEMP_DIR/index.html" ]; then
        error "index.html not found in release"
        exit 1
    fi
    
    if [ ! -f "$TEMP_DIR/latest_menu.json" ]; then
        warning "latest_menu.json not found in release"
    fi
    
    # Check if HTML file is valid (basic check)
    if ! grep -q "<html" "$TEMP_DIR/index.html"; then
        error "index.html appears to be invalid"
        exit 1
    fi
    
    log "Content validation passed"
}

# Deploy to nginx
deploy_content() {
    log "Deploying content to nginx..."
    
    # Clear current web root
    rm -rf "$NGINX_WEB_ROOT"/*
    
    # Copy new content
    cp -r "$TEMP_DIR"/* "$NGINX_WEB_ROOT/"
    
    # Set proper ownership and permissions
    chown -R www-data:www-data "$NGINX_WEB_ROOT"
    chmod -R 755 "$NGINX_WEB_ROOT"
    
    # Create deployment info file
    cat > "$NGINX_WEB_ROOT/deployment-info.txt" << EOF
Deployment Information
======================
Release Tag: $LATEST_TAG
Deployed At: $(date)
Download URL: $DOWNLOAD_URL
Deployed By: $(whoami)
Hostname: $(hostname)
EOF
    
    log "Content deployed successfully"
}

# Test nginx configuration
test_nginx() {
    log "Testing nginx configuration..."
    
    if command -v nginx > /dev/null; then
        if nginx -t; then
            log "Nginx configuration test passed"
            
            # Reload nginx
            systemctl reload nginx
            log "Nginx reloaded successfully"
        else
            error "Nginx configuration test failed"
            exit 1
        fi
    else
        warning "Nginx not found - skipping configuration test"
    fi
}

# Cleanup temp files
cleanup() {
    log "Cleaning up temporary files..."
    rm -rf "$TEMP_DIR"
}

# Send notification (optional)
send_notification() {
    log "Deployment completed successfully!"
    
    # You can add email/webhook notifications here
    # Example: curl -X POST -d "Eurest menu deployed: $LATEST_TAG" your-webhook-url
}

# Main deployment function
main() {
    log "Starting Eurest menu deployment..."
    
    check_permissions
    setup_directories
    backup_current
    get_latest_release
    download_release
    validate_content
    deploy_content
    test_nginx
    cleanup
    send_notification
    
    log "Deployment completed successfully!"
    log "Website available at: http://$(hostname)/eurest-menu/ (or your configured URL)"
}

# Error handling
trap 'error "Deployment failed at line $LINENO"; cleanup; exit 1' ERR

# Run main function
main "$@"
