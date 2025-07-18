# Eurest Menu Scraper - Complete Deployment Guide

This guide walks you through setting up the complete automated menu scraping and deployment system.

## 🏗️ Architecture Overview

```
GitHub Actions (Daily Scraper)
    ↓ (Scrapes menu daily)
GitHub Releases (HTML Website)
    ↓ (Downloads latest release)
Your Server (Nginx + Cron)
    ↓ (Serves website)
Users (Web Browser)
```

## 📋 Prerequisites

- GitHub account
- Linux server with nginx
- Root/sudo access on server
- Basic knowledge of nginx and cron

## 🚀 Step 1: GitHub Repository Setup

### 1.1 Create Repository
```bash
# Create a new repository on GitHub
# Upload these files to your repository:
- python.py                           # Menu scraper
- generate_website.py                 # HTML generator
- .github/workflows/daily-menu-scraper.yml  # GitHub Action
```

### 1.2 Configure GitHub Action
1. Edit `.github/workflows/daily-menu-scraper.yml`
2. Replace `${{ github.repository }}` references with your actual repo name
3. Commit and push to GitHub

### 1.3 Test GitHub Action
```bash
# Go to GitHub → Your Repo → Actions
# Click "Daily Menu Scraper" → "Run workflow"
# Check if it creates a release with HTML website
```

## 🖥️ Step 2: Server Setup

### 2.1 Install Prerequisites
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install nginx
sudo apt install nginx -y

# Install curl and other tools
sudo apt install curl wget tar gzip -y

# Start and enable nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 2.2 Configure Nginx
```bash
# Copy nginx configuration
sudo cp nginx-eurest-menu.conf /etc/nginx/sites-available/eurest-menu

# Edit the configuration
sudo nano /etc/nginx/sites-available/eurest-menu
# Update server_name to your domain or IP

# Enable the site
sudo ln -s /etc/nginx/sites-available/eurest-menu /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

### 2.3 Setup Deployment Scripts
```bash
# Copy deployment files to your server
scp deploy-menu.sh setup-cron.sh user@yourserver:/tmp/

# On your server:
cd /tmp
sudo chmod +x deploy-menu.sh setup-cron.sh

# Edit deployment script to set your GitHub repo
sudo nano deploy-menu.sh
# Change GITHUB_REPO="yourusername/eurest-menu-scraper"
```

### 2.4 Run Initial Setup
```bash
# Setup cron job and monitoring
sudo ./setup-cron.sh

# Test manual deployment
sudo /opt/eurest-menu/deploy-menu.sh
```

## 🔄 Step 3: Automation Configuration

### 3.1 Cron Schedule
The system is configured to check for updates:
- **GitHub Actions**: Daily at 10:30 AM UTC (lunch time in Switzerland)
- **Server Cron**: Every hour from 11:00-14:00 on weekdays

### 3.2 Monitoring
```bash
# Check deployment status
sudo /opt/eurest-menu/monitor-menu.sh

# View logs
sudo tail -f /var/log/eurest-menu-deploy.log
sudo tail -f /var/log/eurest-menu-cron.log

# Check cron jobs
sudo crontab -l

# Check systemd timer (alternative to cron)
sudo systemctl status eurest-menu-deploy.timer
```

## 🌐 Step 4: Access Your Website

### 4.1 Default URLs
- **Website**: `http://yourserver/` or `http://yourdomain.com/`
- **JSON Data**: `http://yourserver/latest_menu.json`
- **Health Check**: `http://yourserver/health`
- **Status**: `http://yourserver/status`

### 4.2 SSL Configuration (Optional)
```bash
# Install certbot for Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal is usually set up automatically
sudo certbot renew --dry-run
```

## 🛠️ Customization Options

### 4.1 Modify Scraping Schedule
Edit `.github/workflows/daily-menu-scraper.yml`:
```yaml
schedule:
  # Change this cron expression
  - cron: '30 10 * * *'  # 10:30 AM UTC daily
```

### 4.2 Modify Deployment Schedule
Edit cron or systemd timer:
```bash
# Edit cron
sudo crontab -e

# Or edit systemd timer
sudo systemctl edit eurest-menu-deploy.timer
```

### 4.3 Customize Website Appearance
Edit `generate_website.py`:
- Change colors in the CSS
- Modify layout
- Add additional features

### 4.4 Add Notifications
Edit deployment scripts to add:
- Email notifications
- Slack/Discord webhooks
- SMS alerts

## 🔧 Troubleshooting

### Common Issues

#### GitHub Action Fails
```bash
# Check GitHub Actions logs
# Common fixes:
# 1. Check repository permissions
# 2. Verify workflow file syntax
# 3. Check if website is accessible
```

#### Deployment Script Fails
```bash
# Check logs
sudo tail -f /var/log/eurest-menu-deploy.log

# Common fixes:
# 1. Check internet connectivity
# 2. Verify GitHub repo name
# 3. Check file permissions
# 4. Verify nginx is running
```

#### Website Not Loading
```bash
# Check nginx status
sudo systemctl status nginx

# Check nginx error logs
sudo tail -f /var/log/nginx/error.log

# Check if files exist
ls -la /var/www/eurest-menu/

# Test nginx configuration
sudo nginx -t
```

#### Old Menu Displayed
```bash
# Force manual deployment
sudo /opt/eurest-menu/deploy-menu.sh

# Check if GitHub has new releases
# Clear browser cache
# Check deployment logs
```

### Debug Commands
```bash
# Test website connectivity
curl -I http://yourserver/

# Test JSON endpoint
curl http://yourserver/latest_menu.json

# Check file permissions
sudo ls -la /var/www/eurest-menu/

# Test deployment without deploy
cd /tmp
curl -L -o test.tar.gz "https://github.com/yourusername/yourrepo/releases/latest/download/eurest-menu-website.tar.gz"
tar -tzf test.tar.gz
```

## 📊 Monitoring Dashboard (Optional)

You can create a simple monitoring dashboard by adding this to your nginx config:

```nginx
location /admin {
    alias /opt/eurest-menu/admin;
    auth_basic "Admin Area";
    auth_basic_user_file /etc/nginx/.htpasswd;
}
```

## 🔐 Security Considerations

1. **Server Security**:
   - Keep system updated
   - Use firewall (ufw/iptables)
   - Regular security audits

2. **Nginx Security**:
   - Use HTTPS with SSL
   - Set proper headers
   - Hide nginx version

3. **Access Control**:
   - Limit admin access
   - Use strong passwords
   - Monitor access logs

## 📈 Scaling and Performance

### For High Traffic:
- Use nginx caching
- Add CloudFlare CDN
- Multiple server instances
- Load balancer

### For Multiple Restaurants:
- Modify scraper for multiple sources
- Separate deployment paths
- Database storage option

## 🆘 Support

### Logs Locations:
- **Deployment**: `/var/log/eurest-menu-deploy.log`
- **Cron**: `/var/log/eurest-menu-cron.log`
- **Nginx**: `/var/log/nginx/eurest-menu.*.log`

### Useful Commands:
```bash
# Restart everything
sudo systemctl restart nginx
sudo systemctl restart eurest-menu-deploy.timer

# Check all services
sudo systemctl status nginx
sudo systemctl status eurest-menu-deploy.timer

# Manual operations
sudo /opt/eurest-menu/deploy-menu.sh      # Deploy now
sudo /opt/eurest-menu/monitor-menu.sh     # Check status
```

---

## 🎉 You're Done!

Your automated Eurest menu system should now be running! The website will automatically update daily with the latest menu from the restaurant.

Visit your website to see the beautiful, responsive menu display that updates automatically! 🍽️
