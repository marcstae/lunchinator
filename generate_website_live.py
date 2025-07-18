#!/usr/bin/env python3
"""
Live HTML Website Generator for Eurest Menu

This script generates a PWA website with live JavaScript scraping functionality.
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
        # Return empty data structure for live scraping
        return {
            'restaurant': 'Eurest Kaserne Timeout',
            'location': 'Papiermühlestrasse 15, 3014 Bern',
            'menu_items': [],
            'total_items': 0,
            'date_info': {
                'scraped_at': datetime.now().isoformat(),
                'display_date': datetime.now().strftime('%Y-%m-%d')
            },
            'url': 'https://clients.eurest.ch/kaserne/de/Timeout'
        }


def generate_css() -> str:
    """Generate CSS styles for the website."""
    return """
/* Minimalistic Futuristic Design with Dark Mode */
:root {
    /* Light mode colors */
    --bg-primary: #fafafa;
    --bg-secondary: #ffffff;
    --bg-tertiary: #f9fafb;
    --bg-accent: #f1f5f9;
    --text-primary: #1a1a1a;
    --text-secondary: #6b7280;
    --text-tertiary: #9ca3af;
    --border-primary: #e8e8e8;
    --border-secondary: #f3f4f6;
    --accent-color: #2563eb;
    --accent-hover: #1d4ed8;
    --shadow-light: rgba(0, 0, 0, 0.04);
    --shadow-medium: rgba(0, 0, 0, 0.02);
}

@media (prefers-color-scheme: dark) {
    :root {
        /* Dark mode colors */
        --bg-primary: #0f0f0f;
        --bg-secondary: #1a1a1a;
        --bg-tertiary: #262626;
        --bg-accent: #2a2a2a;
        --text-primary: #f5f5f5;
        --text-secondary: #a3a3a3;
        --text-tertiary: #737373;
        --border-primary: #404040;
        --border-secondary: #333333;
        --accent-color: #3b82f6;
        --accent-hover: #60a5fa;
        --shadow-light: rgba(0, 0, 0, 0.3);
        --shadow-medium: rgba(0, 0, 0, 0.2);
    }
}

[data-theme="dark"] {
    /* Force dark mode */
    --bg-primary: #0f0f0f;
    --bg-secondary: #1a1a1a;
    --bg-tertiary: #262626;
    --bg-accent: #2a2a2a;
    --text-primary: #f5f5f5;
    --text-secondary: #a3a3a3;
    --text-tertiary: #737373;
    --border-primary: #404040;
    --border-secondary: #333333;
    --accent-color: #3b82f6;
    --accent-hover: #60a5fa;
    --shadow-light: rgba(0, 0, 0, 0.3);
    --shadow-medium: rgba(0, 0, 0, 0.2);
}

[data-theme="light"] {
    /* Force light mode */
    --bg-primary: #fafafa;
    --bg-secondary: #ffffff;
    --bg-tertiary: #f9fafb;
    --bg-accent: #f1f5f9;
    --text-primary: #1a1a1a;
    --text-secondary: #6b7280;
    --text-tertiary: #9ca3af;
    --border-primary: #e8e8e8;
    --border-secondary: #f3f4f6;
    --accent-color: #2563eb;
    --accent-hover: #1d4ed8;
    --shadow-light: rgba(0, 0, 0, 0.04);
    --shadow-medium: rgba(0, 0, 0, 0.02);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', 'SF Pro Display', system-ui, sans-serif;
    line-height: 1.5;
    color: var(--text-primary);
    background: var(--bg-primary);
    min-height: 100vh;
    padding: 24px;
    font-weight: 400;
    letter-spacing: -0.01em;
    transition: background-color 0.3s ease, color 0.3s ease;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    background: var(--bg-secondary);
    border-radius: 2px;
    box-shadow: 0 1px 3px var(--shadow-light), 0 1px 2px var(--shadow-medium);
    overflow: hidden;
    border: 1px solid var(--border-primary);
    transition: background-color 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
}

.dark-mode-toggle {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1000;
    background: var(--bg-secondary);
    border: 1px solid var(--border-primary);
    border-radius: 50%;
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 20px;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px var(--shadow-light);
}

.dark-mode-toggle:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px var(--shadow-light);
}

.header {
    background: var(--bg-secondary);
    color: var(--text-primary);
    padding: 48px 32px;
    text-align: center;
    border-bottom: 1px solid var(--border-primary);
    position: relative;
    transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}

.header::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 40px;
    height: 2px;
    background: var(--accent-color);
    transition: background-color 0.3s ease;
}

.header h1 {
    font-size: 2.25rem;
    margin-bottom: 8px;
    font-weight: 600;
    letter-spacing: -0.025em;
    color: var(--text-primary);
    transition: color 0.3s ease;
}

.header .subtitle {
    font-size: 1rem;
    color: var(--text-secondary);
    margin-bottom: 12px;
    font-weight: 400;
    transition: color 0.3s ease;
}

.header .location {
    font-size: 0.875rem;
    color: var(--text-tertiary);
    font-weight: 400;
    transition: color 0.3s ease;
}

.meta-info {
    background: var(--bg-tertiary);
    padding: 20px 32px;
    border-bottom: 1px solid var(--border-primary);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
    transition: background-color 0.3s ease, border-color 0.3s ease;
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.875rem;
    color: var(--text-secondary);
    font-weight: 400;
    transition: color 0.3s ease;
}

.meta-item .emoji {
    font-size: 1rem;
    opacity: 0.8;
}

.price-stats {
    background: var(--bg-accent);
    color: var(--text-secondary);
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: 500;
    font-size: 0.875rem;
    border: 1px solid var(--border-secondary);
    transition: all 0.3s ease;
}

.content {
    padding: 40px 32px;
    background: var(--bg-secondary);
    transition: background-color 0.3s ease;
}

.category-section {
    margin-bottom: 48px;
}

.category-header {
    background: transparent;
    color: var(--text-primary);
    padding: 20px 0;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 12px;
    border-bottom: 1px solid var(--border-primary);
    position: relative;
    transition: color 0.3s ease, border-color 0.3s ease;
}

.category-header::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    width: 48px;
    height: 2px;
    background: var(--accent-color);
    transition: background-color 0.3s ease;
}

.category-header h2 {
    font-size: 1.125rem;
    margin: 0;
    font-weight: 600;
    letter-spacing: -0.01em;
    color: var(--text-primary);
    transition: color 0.3s ease;
}

.category-count {
    background: var(--bg-accent);
    color: var(--text-secondary);
    padding: 4px 12px;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 500;
    margin-left: auto;
    transition: all 0.3s ease;
}

.menu-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 24px;
}

.menu-item {
    background: var(--bg-secondary);
    border: 1px solid var(--border-primary);
    border-radius: 1px;
    padding: 24px;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
}

.menu-item:hover {
    border-color: var(--border-secondary);
    box-shadow: 0 2px 8px var(--shadow-light);
    transform: translateY(-1px);
}

.item-name {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 8px;
    line-height: 1.4;
    letter-spacing: -0.01em;
    transition: color 0.3s ease;
}

.item-description {
    color: var(--text-secondary);
    margin-bottom: 20px;
    font-size: 0.875rem;
    line-height: 1.5;
    font-weight: 400;
    transition: color 0.3s ease;
}

.item-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid var(--border-secondary);
    transition: border-color 0.3s ease;
}

.item-price {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: -0.01em;
    transition: color 0.3s ease;
}

.item-category {
    background: var(--bg-accent);
    color: var(--text-secondary);
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.025em;
    border: 1px solid var(--border-secondary);
    transition: all 0.3s ease;
}

.footer {
    background: var(--bg-tertiary);
    color: var(--text-secondary);
    padding: 32px;
    text-align: center;
    border-top: 1px solid var(--border-primary);
    transition: all 0.3s ease;
}

.footer-links {
    display: flex;
    justify-content: center;
    gap: 32px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}

.footer-link {
    color: var(--accent-color);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.875rem;
    transition: color 0.2s ease;
}

.footer-link:hover {
    color: var(--accent-hover);
}

.no-items {
    text-align: center;
    padding: 64px 32px;
    color: var(--text-tertiary);
    transition: color 0.3s ease;
}

.no-items h2 {
    color: var(--text-secondary);
    font-size: 1.25rem;
    margin-bottom: 8px;
    font-weight: 600;
    transition: color 0.3s ease;
}

.refresh-info {
    background: var(--bg-accent);
    border: 1px solid var(--border-secondary);
    color: var(--text-secondary);
    padding: 16px;
    border-radius: 6px;
    margin-bottom: 32px;
    text-align: center;
    font-size: 0.875rem;
    font-weight: 400;
    transition: all 0.3s ease;
}

/* Loading and error states */
.loading-state,
.error-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 64px 32px;
    text-align: center;
    color: var(--text-secondary);
}

.loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid var(--border-secondary);
    border-top: 3px solid var(--accent-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 16px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.retry-button {
    background: var(--accent-color);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 6px;
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    margin-top: 16px;
    transition: background-color 0.2s ease;
}

.retry-button:hover {
    background: var(--accent-hover);
}

.live-indicator {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.8rem;
    color: var(--accent-color);
    font-weight: 500;
}

.live-dot {
    width: 8px;
    height: 8px;
    background: var(--accent-color);
    border-radius: 50%;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* Responsive design and mobile optimizations */
@media (max-width: 768px) {
    body {
        padding: 0;
        background: var(--bg-secondary);
    }
    
    .dark-mode-toggle {
        top: 16px;
        right: 16px;
        width: 44px;
        height: 44px;
        font-size: 18px;
    }
    
    .container {
        border-radius: 0;
        border: none;
        box-shadow: none;
        min-height: 100vh;
    }
    
    .header {
        padding: 20px 20px 32px 20px;
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
        min-height: 44px;
        cursor: pointer;
        -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
        user-select: none;
        position: relative;
    }
    
    .menu-item:active {
        background-color: var(--bg-accent);
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
        border: 1px solid var(--border-primary);
    }
    
    .header::after,
    .category-header::after {
        display: none;
    }
    
    .dark-mode-toggle {
        display: none;
    }
}
"""


def generate_live_scraper_js() -> str:
    """Generate JavaScript code to scrape menu data directly in the browser."""
    return '''
// Live menu scraper - runs in the browser
class EurestMenuScraper {
    constructor() {
        this.baseUrl = 'https://clients.eurest.ch/kaserne/de/Timeout';
        this.proxyUrl = 'https://api.allorigins.win/get?url=';
        this.cache = null;
        this.cacheTime = null;
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
    }

    async fetchWithProxy(url) {
        try {
            const response = await fetch(this.proxyUrl + encodeURIComponent(url));
            const data = await response.json();
            return data.contents;
        } catch (error) {
            console.error('Proxy fetch failed:', error);
            throw error;
        }
    }

    parseMenuData(html) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        
        const menuItems = [];
        
        // Look for menu items (adjust selectors based on actual site structure)
        const items = doc.querySelectorAll('.menu-item, .dish, .meal, [class*="menu"], [class*="dish"], .card, .product');
        
        items.forEach((item, index) => {
            const nameEl = item.querySelector('h3, h4, .name, .title, [class*="name"], [class*="title"], strong, b');
            const descEl = item.querySelector('.description, .desc, .ingredients, p, .text');
            const priceEl = item.querySelector('.price, [class*="price"], [data-price]');
            
            const name = nameEl?.textContent?.trim() || `Menu Item ${index + 1}`;
            const description = descEl?.textContent?.trim() || '';
            const priceText = priceEl?.textContent?.trim() || '';
            const price = this.parsePrice(priceText);
            
            // Determine category based on content or position
            let category = 'Menu';
            const text = item.textContent.toLowerCase();
            if (text.includes('vegi') || text.includes('vegetarian')) category = 'Vegi';
            if (text.includes('hit') || text.includes('special') || text.includes('daily')) category = 'Hit';
            if (text.includes('frühstück') || text.includes('breakfast')) category = 'Frühstück';
            
            if (name.length > 3 && !name.includes('Cookie') && !name.includes('Accept')) {
                menuItems.push({
                    name,
                    description,
                    price,
                    category
                });
            }
        });
        
        return {
            restaurant: 'Eurest Kaserne Timeout',
            location: 'Papiermühlestrasse 15, 3014 Bern',
            menu_items: menuItems,
            total_items: menuItems.length,
            date_info: {
                scraped_at: new Date().toISOString(),
                display_date: new Date().toLocaleDateString('de-CH')
            },
            url: this.baseUrl
        };
    }

    parsePrice(priceText) {
        if (!priceText) return null;
        const match = priceText.match(/(\\d+\\.?\\d*)/);
        return match ? parseFloat(match[1]) : null;
    }

    async scrapeMenu() {
        // Check cache first
        if (this.cache && this.cacheTime && 
            (Date.now() - this.cacheTime < this.cacheTimeout)) {
            return this.cache;
        }

        try {
            console.log('🔄 Fetching fresh menu data...');
            const html = await this.fetchWithProxy(this.baseUrl);
            const menuData = this.parseMenuData(html);
            
            // Cache the result
            this.cache = menuData;
            this.cacheTime = Date.now();
            
            console.log('✅ Menu data updated successfully', menuData);
            return menuData;
            
        } catch (error) {
            console.error('❌ Failed to fetch menu data:', error);
            
            // Return fallback data
            return {
                restaurant: 'Eurest Kaserne Timeout',
                location: 'Papiermühlestrasse 15, 3014 Bern',
                menu_items: [{
                    name: 'Menu temporarily unavailable',
                    description: 'Please visit the restaurant website for current menu information.',
                    price: null,
                    category: 'Other'
                }],
                total_items: 1,
                date_info: {
                    scraped_at: new Date().toISOString(),
                    display_date: new Date().toLocaleDateString('de-CH')
                },
                url: this.baseUrl,
                error: 'Failed to fetch live data. Please try again later.'
            };
        }
    }
}

// Menu renderer
class MenuRenderer {
    constructor() {
        this.scraper = new EurestMenuScraper();
    }

    getCategoryEmoji(category) {
        const emojiMap = {
            'Menu': '🍽️',
            'Vegi': '🥗',
            'Hit': '⭐',
            'Frühstück': '🥐',
            'Other': '🍴'
        };
        return emojiMap[category] || '🍴';
    }

    organizeByCategory(menuItems) {
        const categories = {};
        menuItems.forEach(item => {
            const category = item.category || 'Other';
            if (!categories[category]) {
                categories[category] = [];
            }
            categories[category].push(item);
        });
        return categories;
    }

    renderLoadingState() {
        document.getElementById('menuContent').innerHTML = `
            <div class="loading-state">
                <div class="loading-spinner"></div>
                <p>🔄 Loading fresh menu data...</p>
            </div>
        `;
    }

    renderErrorState(error) {
        document.getElementById('menuContent').innerHTML = `
            <div class="error-state">
                <h2>😔 Unable to load menu</h2>
                <p>${error}</p>
                <button onclick="menuApp.loadMenu()" class="retry-button">🔄 Try Again</button>
            </div>
        `;
    }

    renderMenu(menuData) {
        const container = document.getElementById('menuContent');
        const categories = this.organizeByCategory(menuData.menu_items || []);
        
        // Update meta info
        this.updateMetaInfo(menuData);
        
        if (menuData.error && menuData.total_items === 0) {
            this.renderErrorState(menuData.error);
            return;
        }

        if (Object.keys(categories).length === 0) {
            container.innerHTML = `
                <div class="no-items">
                    <h2>😔 No menu items available</h2>
                    <p>The menu could not be loaded at this time. Please check back later.</p>
                    <button onclick="menuApp.loadMenu()" class="retry-button">🔄 Refresh</button>
                </div>
            `;
            return;
        }

        let html = '';
        const categoryOrder = ['Frühstück', 'Menu', 'Vegi', 'Hit', 'Other'];
        
        categoryOrder.forEach(category => {
            if (!categories[category]) return;
            
            const items = categories[category];
            const emoji = this.getCategoryEmoji(category);
            
            html += `
                <section class="category-section">
                    <div class="category-header">
                        <span>${emoji}</span>
                        <h2>${category.toUpperCase()}</h2>
                        <span class="category-count">${items.length} items</span>
                    </div>
                    
                    <div class="menu-grid">
            `;
            
            items.forEach(item => {
                const priceHtml = item.price ? 
                    `<span class="item-price">CHF ${item.price.toFixed(2)}</span>` : '';
                
                html += `
                    <div class="menu-item">
                        <div class="item-name">${item.name}</div>
                        ${item.description ? `<div class="item-description">${item.description}</div>` : ''}
                        <div class="item-footer">
                            ${priceHtml}
                            <span class="item-category">${item.category}</span>
                        </div>
                    </div>
                `;
            });
            
            html += `
                    </div>
                </section>
            `;
        });

        container.innerHTML = html;
        
        // Re-attach event listeners for mobile interactions
        this.attachMenuItemListeners();
    }

    updateMetaInfo(menuData) {
        const totalItems = menuData.total_items || 0;
        const prices = (menuData.menu_items || [])
            .map(item => item.price)
            .filter(price => price !== null);
        
        let priceRange = 'N/A';
        let avgPrice = 'N/A';
        
        if (prices.length > 0) {
            const minPrice = Math.min(...prices);
            const maxPrice = Math.max(...prices);
            const average = prices.reduce((a, b) => a + b, 0) / prices.length;
            priceRange = `CHF ${minPrice.toFixed(2)} - CHF ${maxPrice.toFixed(2)}`;
            avgPrice = `CHF ${average.toFixed(2)}`;
        }

        const scrapedAt = menuData.date_info?.scraped_at || new Date().toISOString();
        const scrapedFormatted = new Date(scrapedAt).toLocaleString('de-CH');

        const totalEl = document.querySelector('[data-total-items]');
        const priceEl = document.querySelector('[data-price-stats]');
        const updatedEl = document.querySelector('[data-updated]');
        
        if (totalEl) totalEl.textContent = `${totalItems} menu items`;
        if (priceEl) priceEl.textContent = `💰 ${priceRange} | Avg: ${avgPrice}`;
        if (updatedEl) updatedEl.textContent = `Updated: ${scrapedFormatted}`;
    }

    attachMenuItemListeners() {
        document.querySelectorAll('.menu-item').forEach(item => {
            item.addEventListener('touchstart', function() {
                this.style.backgroundColor = 'var(--bg-accent)';
            });
            
            item.addEventListener('touchend', function() {
                setTimeout(() => {
                    this.style.backgroundColor = '';
                }, 150);
            });
            
            item.addEventListener('click', function() {
                this.style.transform = 'scale(0.98)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 150);
            });
        });
    }

    async loadMenu() {
        this.renderLoadingState();
        const menuData = await this.scraper.scrapeMenu();
        this.renderMenu(menuData);
    }
}

// Global menu app instance
const menuApp = new MenuRenderer();

// Auto-refresh functionality
setInterval(() => {
    console.log('🔄 Auto-refreshing menu data...');
    menuApp.loadMenu();
}, 10 * 60 * 1000); // Refresh every 10 minutes
'''


def generate_html(menu_data: Dict) -> str:
    """Generate the complete HTML website."""
    
    # Generate the live scraper JavaScript
    live_scraper_js = generate_live_scraper_js()
    
    # Get website URL for footer
    website_url = menu_data.get('url', 'https://clients.eurest.ch/kaserne/de/Timeout')
    
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
        <button class="dark-mode-toggle" id="darkModeToggle" title="Toggle dark mode">
            <span id="darkModeIcon">🌙</span>
        </button>
        
        <header class="header">
            <h1>🍽️ {menu_data.get('restaurant', 'Eurest Kaserne Timeout')}</h1>
            <div class="subtitle">Daily Lunch Menu - Live Data</div>
            <div class="location">📍 {menu_data.get('location', 'Papiermühlestrasse 15, 3014 Bern')}</div>
        </header>
        
        <div class="meta-info">
            <div class="meta-item">
                <span class="emoji">📅</span>
                <span data-updated>Loading...</span>
            </div>
            <div class="meta-item">
                <span class="emoji">🍴</span>
                <span data-total-items>Loading...</span>
            </div>
            <div class="meta-item">
                <span class="live-indicator">
                    <span class="live-dot"></span>
                    LIVE
                </span>
            </div>
            <div class="price-stats" data-price-stats>
                💰 Loading...
            </div>
        </div>
        
        <main class="content">
            <div class="refresh-info">
                ℹ️ This menu updates automatically with live data. Pull down to refresh manually.
            </div>
            
            <div id="menuContent">
                <div class="loading-state">
                    <div class="loading-spinner"></div>
                    <p>🔄 Loading fresh menu data...</p>
                </div>
            </div>
        </main>
        
        <footer class="footer">
            <div class="footer-links">
                <a href="{website_url}" target="_blank" rel="noopener" class="footer-link">🌐 Visit Restaurant Website</a>
                <a href="javascript:menuApp.loadMenu()" class="footer-link">🔄 Refresh Menu</a>
                <a href="javascript:window.print()" class="footer-link">🖨️ Print Menu</a>
            </div>
            <p>
                <small>
                    Live data from <a href="{website_url}" target="_blank" rel="noopener" class="footer-link">Eurest Kaserne Timeout</a><br>
                    Auto-refreshes every 10 minutes | Generated with ❤️ by GitHub Actions
                </small>
            </p>
        </footer>
    </div>
    
    <script>
        {live_scraper_js}
        
        // Initialize dark mode and live menu loading
        document.addEventListener('DOMContentLoaded', function() {{
            // Dark mode functionality
            const darkModeToggle = document.getElementById('darkModeToggle');
            const darkModeIcon = document.getElementById('darkModeIcon');
            const html = document.documentElement;
            
            // Check for saved theme or default to auto
            const savedTheme = localStorage.getItem('theme');
            const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            
            // Initialize theme
            if (savedTheme) {{
                html.setAttribute('data-theme', savedTheme);
                updateIcon(savedTheme);
            }} else if (systemPrefersDark) {{
                updateIcon('dark');
            }} else {{
                updateIcon('light');
            }}
            
            function updateIcon(theme) {{
                if (theme === 'dark' || (!theme && systemPrefersDark)) {{
                    darkModeIcon.textContent = '☀️';
                }} else {{
                    darkModeIcon.textContent = '🌙';
                }}
            }}
            
            darkModeToggle.addEventListener('click', function() {{
                const currentTheme = html.getAttribute('data-theme');
                let newTheme;
                
                if (currentTheme === 'dark') {{
                    newTheme = 'light';
                }} else if (currentTheme === 'light') {{
                    newTheme = 'dark';
                }} else {{
                    // Auto mode - toggle opposite of system preference
                    newTheme = systemPrefersDark ? 'light' : 'dark';
                }}
                
                html.setAttribute('data-theme', newTheme);
                localStorage.setItem('theme', newTheme);
                updateIcon(newTheme);
                
                // Add feedback animation
                darkModeToggle.style.transform = 'scale(0.9)';
                setTimeout(() => {{
                    darkModeToggle.style.transform = '';
                }}, 150);
            }});
            
            // Listen for system theme changes
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {{
                if (!localStorage.getItem('theme')) {{
                    updateIcon(e.matches ? 'dark' : 'light');
                }}
            }});
            
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
            
            // Initialize live menu loading
            menuApp.loadMenu();
            
            // Add current time display
            const now = new Date();
            const timeStr = now.toLocaleString('de-CH');
            console.log('Page loaded at:', timeStr);
            
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
                    console.log('🔄 Pull-to-refresh triggered');
                    menuApp.loadMenu();
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
    ],
    "edge_side_panel": {
        "preferred_width": 400
    },
    "user_preferences": {
        "color_scheme_dark": {
            "theme_color": "#1a1a1a",
            "background_color": "#0f0f0f"
        }
    }
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
    print(f"Generating live PWA website from {json_file}...")
    
    # Load menu data (used for fallback)
    menu_data = load_menu_data(json_file)
    
    # Generate HTML with live scraping
    html_content = generate_html(menu_data)
    
    # Generate PWA files
    manifest_content = generate_manifest()
    sw_content = generate_service_worker()
    
    # Save HTML file
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Save PWA files
    with open('manifest.json', 'w', encoding='utf-8') as f:
        f.write(manifest_content)
        
    with open('sw.js', 'w', encoding='utf-8') as f:
        f.write(sw_content)
    
    print("✅ Live PWA website generated successfully!")
    print("📁 Files created:")
    print("   - index.html (main website with live scraper)")
    print("   - manifest.json (PWA manifest)")
    print("   - sw.js (service worker)")
    print(f"   - {json_file} (source data - used as fallback)")
    print("")
    print("🔴 LIVE Features:")
    print("   - Real-time menu scraping in browser")
    print("   - Auto-refresh every 10 minutes")
    print("   - Pull-to-refresh on mobile")
    print("   - No server required - runs entirely in browser")
    print("   - Dark mode with system detection")
    print("   - Installable as PWA on mobile devices")
    print("")
    print("🖼️  Note: Add app icons for full PWA experience:")
    print("   - icon-16.png, icon-32.png (favicon)")
    print("   - icon-120.png, icon-152.png, icon-180.png (iOS)")
    print("   - icon-192.png, icon-512.png (Android)")
    print("")
    print("📲 Installation: Open in Safari/Chrome and tap 'Add to Home Screen'")
    print("🌐 The website will now fetch fresh menu data every time it loads!")
    
    # Print some statistics
    total_items = menu_data.get('total_items', 0)
    print(f"📊 Fallback data contains {total_items} items")


if __name__ == "__main__":
    main()
