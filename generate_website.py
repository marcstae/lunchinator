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
/* Modern, clean styling for the menu website */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}

.container {
    max-width: 1000px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}

.header {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
    color: white;
    padding: 30px;
    text-align: center;
}

.header h1 {
    font-size: 2.5em;
    margin-bottom: 10px;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.header .subtitle {
    font-size: 1.2em;
    opacity: 0.9;
    margin-bottom: 10px;
}

.header .location {
    font-size: 1em;
    opacity: 0.8;
}

.meta-info {
    background: #f8f9fa;
    padding: 20px 30px;
    border-bottom: 1px solid #e9ecef;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 15px;
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.95em;
    color: #666;
}

.meta-item .emoji {
    font-size: 1.2em;
}

.price-stats {
    background: #e3f2fd;
    color: #1565c0;
    padding: 10px 15px;
    border-radius: 10px;
    font-weight: 600;
}

.content {
    padding: 30px;
}

.category-section {
    margin-bottom: 40px;
}

.category-header {
    background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
    color: white;
    padding: 15px 25px;
    border-radius: 15px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.category-header h2 {
    font-size: 1.4em;
    margin: 0;
}

.category-count {
    background: rgba(255, 255, 255, 0.2);
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 0.9em;
}

.menu-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 20px;
}

.menu-item {
    background: white;
    border: 1px solid #e9ecef;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.menu-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.item-name {
    font-size: 1.3em;
    font-weight: 700;
    color: #2d3436;
    margin-bottom: 10px;
    line-height: 1.3;
}

.item-description {
    color: #636e72;
    margin-bottom: 15px;
    font-size: 0.95em;
    line-height: 1.5;
}

.item-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px solid #f1f3f4;
}

.item-price {
    font-size: 1.4em;
    font-weight: 700;
    color: #00b894;
}

.item-category {
    background: linear-gradient(135deg, #a29bfe 0%, #6c5ce7 100%);
    color: white;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.85em;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.footer {
    background: #2d3436;
    color: white;
    padding: 25px 30px;
    text-align: center;
}

.footer-links {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-bottom: 15px;
    flex-wrap: wrap;
}

.footer-link {
    color: #74b9ff;
    text-decoration: none;
    transition: color 0.3s ease;
}

.footer-link:hover {
    color: #0984e3;
}

.no-items {
    text-align: center;
    padding: 40px;
    color: #666;
    font-style: italic;
}

.refresh-info {
    background: #fff3cd;
    border: 1px solid #ffeaa7;
    color: #856404;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 20px;
    text-align: center;
}

/* Responsive design */
@media (max-width: 768px) {
    body {
        padding: 10px;
    }
    
    .header h1 {
        font-size: 2em;
    }
    
    .meta-info {
        flex-direction: column;
        text-align: center;
    }
    
    .content {
        padding: 20px;
    }
    
    .menu-grid {
        grid-template-columns: 1fr;
    }
    
    .footer-links {
        flex-direction: column;
        gap: 10px;
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
    }
    
    .menu-item {
        break-inside: avoid;
        box-shadow: none;
        border: 1px solid #ddd;
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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eurest Kaserne Timeout - Daily Menu</title>
    <meta name="description" content="Daily lunch menu from Eurest Kaserne Timeout restaurant in Bern, Switzerland">
    <meta name="keywords" content="Eurest, Kaserne, Timeout, Bern, lunch, menu, restaurant">
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
        // Simple JavaScript for enhanced functionality
        document.addEventListener('DOMContentLoaded', function() {{
            // Add current time display
            const now = new Date();
            const timeStr = now.toLocaleString('de-CH');
            console.log('Page loaded at:', timeStr);
            
            // Add click tracking for menu items (optional)
            document.querySelectorAll('.menu-item').forEach(item => {{
                item.addEventListener('click', function() {{
                    this.style.transform = 'scale(1.02)';
                    setTimeout(() => {{
                        this.style.transform = '';
                    }}, 200);
                }});
            }});
        }});
    </script>
</body>
</html>"""

    return html


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
    
    print("✅ Website generated successfully!")
    print("📁 Files created:")
    print("   - index.html (main website)")
    print(f"   - {json_file} (source data)")
    
    # Print some statistics
    total_items = menu_data.get('total_items', 0)
    print(f"📊 Menu contains {total_items} items")


if __name__ == "__main__":
    main()
