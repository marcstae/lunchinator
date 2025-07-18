#!/usr/bin/env python3
"""
HTML Website Generator for Eurest Menu

This script generates a beautiful HTML website from the scraped menu data.
"""

import json
import sys
from datetime import datetime
from typing import Dict, List


def load_menu_data(json_file: str) -> Dict:
    """Load menu data from JSON file."""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading menu data: {e}")
        sys.exit(1)


def generate_css() -> str:
    """Generate CSS styles for the website."""
    return """
/* Minimalistic Futuristic Design */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', 'SF Pro Display', system-ui, sans-serif;
    line-height: 1.5;
    color: #1a1a1a;
    background: #fafafa;
    min-height: 100vh;
    padding: 24px;
    font-weight: 400;
    letter-spacing: -0.01em;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    background: #ffffff;
    border-radius: 2px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.02);
    overflow: hidden;
    border: 1px solid #e8e8e8;
}

.header {
    background: #ffffff;
    color: #1a1a1a;
    padding: 48px 32px;
    text-align: center;
    border-bottom: 1px solid #e8e8e8;
    position: relative;
}

.header::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 40px;
    height: 2px;
    background: #2563eb;
}

.header h1 {
    font-size: 2.25rem;
    margin-bottom: 8px;
    font-weight: 600;
    letter-spacing: -0.025em;
    color: #1a1a1a;
}

.header .subtitle {
    font-size: 1rem;
    color: #6b7280;
    margin-bottom: 12px;
    font-weight: 400;
}

.header .location {
    font-size: 0.875rem;
    color: #9ca3af;
    font-weight: 400;
}

.meta-info {
    background: #f9fafb;
    padding: 20px 32px;
    border-bottom: 1px solid #e8e8e8;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.875rem;
    color: #6b7280;
    font-weight: 400;
}

.meta-item .emoji {
    font-size: 1rem;
    opacity: 0.8;
}

.price-stats {
    background: #f1f5f9;
    color: #475569;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: 500;
    font-size: 0.875rem;
    border: 1px solid #e2e8f0;
}

.content {
    padding: 40px 32px;
}

.category-section {
    margin-bottom: 48px;
}

.category-header {
    background: #ffffff;
    color: #1a1a1a;
    padding: 20px 0;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 12px;
    border-bottom: 1px solid #e8e8e8;
    position: relative;
}

.category-header::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    width: 48px;
    height: 2px;
    background: #2563eb;
}

.category-header h2 {
    font-size: 1.125rem;
    margin: 0;
    font-weight: 600;
    letter-spacing: -0.01em;
}

.category-count {
    background: #f3f4f6;
    color: #6b7280;
    padding: 4px 12px;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 500;
    margin-left: auto;
}

.menu-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 24px;
}

.menu-item {
    background: #ffffff;
    border: 1px solid #e8e8e8;
    border-radius: 1px;
    padding: 24px;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
}

.menu-item:hover {
    border-color: #d1d5db;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.item-name {
    font-size: 1.125rem;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 8px;
    line-height: 1.4;
    letter-spacing: -0.01em;
}

.item-description {
    color: #6b7280;
    margin-bottom: 20px;
    font-size: 0.875rem;
    line-height: 1.5;
    font-weight: 400;
}

.item-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #f3f4f6;
}

.item-price {
    font-size: 1.25rem;
    font-weight: 600;
    color: #1a1a1a;
    letter-spacing: -0.01em;
}

.item-category {
    background: #f8fafc;
    color: #475569;
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.025em;
    border: 1px solid #e2e8f0;
}

.footer {
    background: #f9fafb;
    color: #6b7280;
    padding: 32px;
    text-align: center;
    border-top: 1px solid #e8e8e8;
}

.footer-links {
    display: flex;
    justify-content: center;
    gap: 32px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}

.footer-link {
    color: #2563eb;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.875rem;
    transition: color 0.2s ease;
}

.footer-link:hover {
    color: #1d4ed8;
}

.no-items {
    text-align: center;
    padding: 64px 32px;
    color: #9ca3af;
}

.no-items h2 {
    color: #6b7280;
    font-size: 1.25rem;
    margin-bottom: 8px;
    font-weight: 600;
}

.refresh-info {
    background: #fffbeb;
    border: 1px solid #fed7aa;
    color: #92400e;
    padding: 16px;
    border-radius: 6px;
    margin-bottom: 32px;
    text-align: center;
    font-size: 0.875rem;
    font-weight: 400;
}

/* Responsive design and mobile optimizations */
@media (max-width: 768px) {
    body {
        padding: 0;
        background: #ffffff;
    }
    
    .container {
        border-radius: 0;
        border: none;
        box-shadow: none;
        min-height: 100vh;
    }
    
    .header {
        padding: 20px 20px 32px 20px;
        /* Account for iOS status bar */
        padding-top: max(20px, env(safe-area-inset-top));
    }
    
    .header h1 {
        font-size: 1.75rem;
    }
    
    .header .subtitle {
        font-size: 0.9rem;
    }
    
    .header .location {
        font-size: 0.8rem;
    }
    
    .meta-info {
        flex-direction: column;
        text-align: center;
        padding: 16px 20px;
        gap: 12px;
    }
    
    .meta-item {
        font-size: 0.8rem;
    }
    
    .price-stats {
        font-size: 0.8rem;
        padding: 6px 12px;
    }
    
    .content {
        padding: 24px 20px;
        padding-bottom: max(24px, env(safe-area-inset-bottom));
    }
    
    .category-section {
        margin-bottom: 32px;
    }
    
    .category-header {
        padding: 16px 0;
        margin-bottom: 16px;
    }
    
    .category-header h2 {
        font-size: 1rem;
    }
    
    .category-count {
        font-size: 0.7rem;
        padding: 3px 8px;
    }
    
    .menu-grid {
        grid-template-columns: 1fr;
        gap: 16px;
    }
    
    .menu-item {
        padding: 20px;
        /* Better touch targets */
        min-height: 44px;
        cursor: pointer;
        -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
        user-select: none;
        position: relative;
    }
    
    .menu-item:active {
        background-color: #f8fafc;
    }
    
    .item-name {
        font-size: 1rem;
        margin-bottom: 6px;
    }
    
    .item-description {
        font-size: 0.8rem;
        margin-bottom: 16px;
        line-height: 1.4;
    }
    
    .item-footer {
        margin-top: 16px;
        padding-top: 16px;
    }
    
    .item-price {
        font-size: 1.1rem;
    }
    
    .item-category {
        font-size: 0.7rem;
        padding: 4px 8px;
    }
    
    .footer {
        padding: 24px 20px;
        padding-bottom: max(24px, env(safe-area-inset-bottom));
    }
    
    .footer-links {
        flex-direction: column;
        gap: 12px;
    }
    
    .footer-link {
        font-size: 0.8rem;
        padding: 8px;
        /* Better touch targets */
        min-height: 44px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .refresh-info {
        margin: 16px 20px 24px 20px;
        padding: 12px;
        font-size: 0.8rem;
    }
    
    .no-items {
        padding: 48px 20px;
    }
}

/* iOS specific styles */
@supports (-webkit-touch-callout: none) {
    body {
        /* Disable iOS bounce scroll */
        position: fixed;
        width: 100%;
        height: 100%;
        overflow: hidden;
    }
    
    .container {
        height: 100vh;
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
    }
    
    /* iOS safe area support */
    .header {
        padding-top: max(20px, env(safe-area-inset-top));
    }
    
    .footer {
        padding-bottom: max(24px, env(safe-area-inset-bottom));
    }
}

/* Touch optimizations */
@media (pointer: coarse) {
    .menu-item {
        padding: 24px;
        border-radius: 8px;
    }
    
    .footer-link,
    .menu-item {
        /* Ensure minimum touch target size */
        min-height: 44px;
    }
}

/* Print styles */
@media print {
    body {
        background: white;
        padding: 0;
    }
    
    .container {
        box-shadow: none;
        border-radius: 0;
        border: none;
    }
    
    .menu-item {
        break-inside: avoid;
        box-shadow: none;
        border: 1px solid #e8e8e8;
    }
    
    .header::after,
    .category-header::after {
        display: none;
    }
}
"""


def get_category_emoji(category: str) -> str:
    """Get emoji for category."""
    emoji_map = {
        'Menu': '🍽️',
        'Vegi': '🥗',
        'Hit': '⭐',
        'Frühstück': '🥐',
        'Other': '🍴'
    }
    return emoji_map.get(category, '🍴')


def organize_by_category(menu_items: List[Dict]) -> Dict:
    """Organize menu items by category."""
    categories = {}
    for item in menu_items:
        category = item.get('category', 'Other')
        if category not in categories:
            categories[category] = []
        categories[category].append(item)
    return categories


def generate_html(menu_data: Dict) -> str:
    """Generate the complete HTML website."""
    
    # Calculate statistics
    total_items = menu_data.get('total_items', 0)
    prices = [item['price'] for item in menu_data.get('menu_items', []) if item.get('price')]
    
    if prices:
        min_price = min(prices)
        max_price = max(prices)
        avg_price = sum(prices) / len(prices)
        price_range = f"CHF {min_price:.2f} - CHF {max_price:.2f}"
        avg_price_str = f"CHF {avg_price:.2f}"
    else:
        price_range = "N/A"
        avg_price_str = "N/A"
    
    # Get date info
    scraped_at = menu_data.get('date_info', {}).get('scraped_at', '')
    display_date = menu_data.get('date_info', {}).get('display_date', '')
    
    if scraped_at:
        try:
            scraped_dt = datetime.fromisoformat(scraped_at.replace('Z', '+00:00'))
            scraped_formatted = scraped_dt.strftime('%B %d, %Y at %H:%M UTC')
        except:
            scraped_formatted = scraped_at
    else:
        scraped_formatted = "Unknown"
    
    # Organize items by category
    categories = organize_by_category(menu_data.get('menu_items', []))
    
    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Eurest Kaserne Timeout - Daily Menu</title>
    <meta name="description" content="Daily lunch menu from Eurest Kaserne Timeout restaurant in Bern, Switzerland">
    <meta name="keywords" content="Eurest, Kaserne, Timeout, Bern, lunch, menu, restaurant">
    
    <!-- PWA Meta Tags -->
    <meta name="application-name" content="Eurest Menu">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="Eurest Menu">
    <meta name="format-detection" content="telephone=no">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="theme-color" content="#2563eb">
    
    <!-- Manifest -->
    <link rel="manifest" href="./manifest.json">
    
    <!-- Apple Touch Icons -->
    <link rel="apple-touch-icon" sizes="180x180" href="./icon-180.png">
    <link rel="apple-touch-icon" sizes="152x152" href="./icon-152.png">
    <link rel="apple-touch-icon" sizes="120x120" href="./icon-120.png">
    <link rel="icon" type="image/png" sizes="32x32" href="./icon-32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="./icon-16.png">
    
    <style>{generate_css()}</style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>🍽️ {menu_data.get('restaurant', 'Eurest Kaserne Timeout')}</h1>
            <div class="subtitle">Daily Lunch Menu</div>
            <div class="location">📍 {menu_data.get('location', 'Papiermühlestrasse 15, 3014 Bern')}</div>
        </header>
        
        <div class="meta-info">
            <div class="meta-item">
                <span class="emoji">📅</span>
                <span>Updated: {scraped_formatted}</span>
            </div>
            <div class="meta-item">
                <span class="emoji">🍴</span>
                <span>{total_items} menu items</span>
            </div>
            <div class="price-stats">
                💰 {price_range} | Avg: {avg_price_str}
            </div>
        </div>
        
        <main class="content">
            <div class="refresh-info">
                ℹ️ This menu is automatically updated daily. Prices and availability may change.
            </div>
"""

    if not categories:
        html += """
            <div class="no-items">
                <h2>😔 No menu items available</h2>
                <p>The menu could not be loaded at this time. Please check back later or visit the restaurant directly.</p>
            </div>
"""
    else:
        # Generate category sections
        category_order = ['Frühstück', 'Menu', 'Vegi', 'Hit', 'Other']
        
        for category in category_order:
            if category not in categories:
                continue
                
            items = categories[category]
            emoji = get_category_emoji(category)
            
            html += f"""
            <section class="category-section">
                <div class="category-header">
                    <span>{emoji}</span>
                    <h2>{category.upper()}</h2>
                    <span class="category-count">{len(items)} items</span>
                </div>
                
                <div class="menu-grid">
"""
            
            for item in items:
                name = item.get('name', 'Unknown Item')
                description = item.get('description', '')
                price = item.get('price')
                category_name = item.get('category', 'Other')
                
                # Clean up description
                if description and len(description) > 200:
                    description = description[:200] + "..."
                
                price_html = f'<span class="item-price">CHF {price:.2f}</span>' if price else ''
                
                html += f"""
                    <div class="menu-item">
                        <div class="item-name">{name}</div>
"""
                
                if description:
                    html += f'                        <div class="item-description">{description}</div>\n'
                
                html += f"""
                        <div class="item-footer">
                            {price_html}
                            <span class="item-category">{category_name}</span>
                        </div>
                    </div>
"""
            
            html += """
                </div>
            </section>
"""

    # Add footer
    website_url = menu_data.get('url', 'https://clients.eurest.ch/kaserne/de/Timeout')
    
    html += f"""
        </main>
        
        <footer class="footer">
            <div class="footer-links">
                <a href="{website_url}" target="_blank" rel="noopener" class="footer-link">🌐 Visit Restaurant Website</a>
                <a href="./latest_menu.json" class="footer-link">📄 Download JSON Data</a>
                <a href="javascript:window.print()" class="footer-link">🖨️ Print Menu</a>
            </div>
            <p>
                <small>
                    Data automatically scraped from <a href="{website_url}" target="_blank" rel="noopener" class="footer-link">Eurest Kaserne Timeout</a><br>
                    Last updated: {scraped_formatted} | Generated with ❤️ by GitHub Actions
                </small>
            </p>
        </footer>
    </div>
    
    <script>
        // Progressive Web App functionality
        document.addEventListener('DOMContentLoaded', function() {{
            // Register service worker
            if ('serviceWorker' in navigator) {{
                navigator.serviceWorker.register('./sw.js')
                    .then(registration => {{
                        console.log('SW registered successfully');
                    }})
                    .catch(error => {{
                        console.log('SW registration failed');
                    }});
            }}
            
            // Add current time display
            const now = new Date();
            const timeStr = now.toLocaleString('de-CH');
            console.log('Page loaded at:', timeStr);
            
            // Enhanced mobile interactions
            document.querySelectorAll('.menu-item').forEach(item => {{
                // Touch feedback
                item.addEventListener('touchstart', function() {{
                    this.style.backgroundColor = '#f8fafc';
                }});
                
                item.addEventListener('touchend', function() {{
                    setTimeout(() => {{
                        this.style.backgroundColor = '';
                    }}, 150);
                }});
                
                // Click animation
                item.addEventListener('click', function() {{
                    this.style.transform = 'scale(0.98)';
                    setTimeout(() => {{
                        this.style.transform = '';
                    }}, 150);
                }});
            }});
            
            // Pull-to-refresh simulation
            let startY = 0;
            let pullDistance = 0;
            const threshold = 100;
            
            document.addEventListener('touchstart', (e) => {{
                startY = e.touches[0].clientY;
            }});
            
            document.addEventListener('touchmove', (e) => {{
                pullDistance = e.touches[0].clientY - startY;
                if (pullDistance > 0 && window.scrollY === 0) {{
                    e.preventDefault();
                }}
            }});
            
            document.addEventListener('touchend', () => {{
                if (pullDistance > threshold && window.scrollY === 0) {{
                    window.location.reload();
                }}
                pullDistance = 0;
            }});
        }});
    </script>
</body>
</html>"""

    return html


def generate_manifest() -> str:
    """Generate PWA manifest.json file."""
    return """{
    "name": "Eurest Kaserne Timeout Menu",
    "short_name": "Eurest Menu",
    "description": "Daily lunch menu from Eurest Kaserne Timeout restaurant in Bern, Switzerland",
    "start_url": "./index.html",
    "display": "standalone",
    "orientation": "portrait-primary",
    "theme_color": "#2563eb",
    "background_color": "#ffffff",
    "scope": "./",
    "lang": "de",
    "icons": [
        {
            "src": "./icon-192.png",
            "sizes": "192x192",
            "type": "image/png",
            "purpose": "any maskable"
        },
        {
            "src": "./icon-512.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "any maskable"
        },
        {
            "src": "./icon-180.png",
            "sizes": "180x180",
            "type": "image/png",
            "purpose": "any"
        }
    ],
    "categories": ["food", "lifestyle"],
    "shortcuts": [
        {
            "name": "Today's Menu",
            "short_name": "Menu",
            "description": "View today's lunch menu",
            "url": "./index.html",
            "icons": [
                {
                    "src": "./icon-192.png",
                    "sizes": "192x192"
                }
            ]
        }
    ]
}"""


def generate_service_worker() -> str:
    """Generate service worker for PWA functionality."""
    return """const CACHE_NAME = 'eurest-menu-v1';
const urlsToCache = [
    './',
    './index.html',
    './manifest.json',
    './icon-192.png',
    './icon-512.png'
];

// Install event - cache resources
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                return cache.addAll(urlsToCache);
            })
    );
});

// Fetch event - serve from cache when offline
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // Return cached version or fetch from network
                return response || fetch(event.request);
            }
        )
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});"""


def main():
    """Main function to generate the website."""
    if len(sys.argv) != 2:
        print("Usage: python generate_website.py <menu_json_file>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    print(f"Generating website from {json_file}...")
    
    # Load menu data
    menu_data = load_menu_data(json_file)
    
    # Generate HTML
    html_content = generate_html(menu_data)
    
    # Save HTML file
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Save manifest file
    with open('manifest.json', 'w', encoding='utf-8') as f:
        f.write(generate_manifest())
    
    # Save service worker file
    with open('sw.js', 'w', encoding='utf-8') as f:
        f.write(generate_service_worker())
    
    print("✅ PWA website generated successfully!")
    print("📁 Files created:")
    print("   - index.html (main website)")
    print("   - manifest.json (PWA manifest)")
    print("   - sw.js (service worker)")
    print(f"   - {json_file} (source data)")
    print("")
    print("📱 PWA Features:")
    print("   - Installable as app on iOS/Android")
    print("   - Offline support")
    print("   - App-like experience")
    print("   - Touch-optimized interface")
    print("   - Pull-to-refresh functionality")
    print("")
    print("🖼️  Note: Add app icons for full PWA experience:")
    print("   - icon-16.png, icon-32.png (favicon)")
    print("   - icon-120.png, icon-152.png, icon-180.png (iOS)")
    print("   - icon-192.png, icon-512.png (Android)")
    print("")
    print("📲 Installation: Open in Safari/Chrome and tap 'Add to Home Screen'")
    
    # Print some statistics
    total_items = menu_data.get('total_items', 0)
    print(f"📊 Menu contains {total_items} items")


if __name__ == "__main__":
    main()
