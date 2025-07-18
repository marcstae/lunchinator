#!/usr/bin/env python3
"""
Eurest Kaserne Timeout Lunch Menu Web Scraper

This script scrapes the lunch menu from the Eurest Kaserne Timeout restaurant
and displays it in a structured format.

Website: https://clients.eurest.ch/kaserne/de/Timeout

Note: This version uses built-in libraries only. For production use, consider
installing requests and beautifulsoup4 for better HTML parsing.
"""

import urllib.request
import urllib.parse
import urllib.error
import html.parser
import re
from datetime import datetime
from typing import List, Dict, Optional
import json


class MenuHTMLParser(html.parser.HTMLParser):
    """Simple HTML parser to extract menu information."""
    
    def __init__(self):
        super().__init__()
        self.menu_items = []
        self.current_item = {}
        self.in_h3 = False
        self.in_text_element = False
        self.current_text = ""
        self.text_buffer = []
    
    def handle_starttag(self, tag, attrs):
        if tag == 'h3':
            self.in_h3 = True
            self.current_text = ""
        elif tag in ['p', 'div', 'span']:
            self.in_text_element = True
            self.current_text = ""
    
    def handle_endtag(self, tag):
        if tag == 'h3' and self.in_h3:
            self.in_h3 = False
            item_name = self.current_text.strip()
            if item_name and not self.is_skip_item(item_name):
                self.current_item = {'name': item_name, 'description': '', 'price': None, 'category': None}
                self.menu_items.append(self.current_item)
        elif tag in ['p', 'div', 'span'] and self.in_text_element:
            self.in_text_element = False
            text = self.current_text.strip()
            if text and self.current_item:
                self.process_text(text)
    
    def handle_data(self, data):
        if self.in_h3 or self.in_text_element:
            self.current_text += data
    
    def is_skip_item(self, text):
        """Check if the text should be skipped as it's not a menu item."""
        skip_patterns = [
            'öffnungszeiten', 'kontakt', 'ihre meinung', 'wir machen',
            'hot & delicious', 'dessert bieten wir', 'kaffee, tee',
            'compass group', 'jobs', 'impressum', 'datenschutz'
        ]
        return any(pattern in text.lower() for pattern in skip_patterns)
    
    def process_text(self, text):
        """Process text to extract price, category, and description."""
        if not self.current_item:
            return
        
        # Extract price
        price_match = re.search(r'CHF\s*(\d+[,.]?\d*)', text)
        if price_match and not self.current_item['price']:
            price_str = price_match.group(1).replace(',', '.')
            try:
                self.current_item['price'] = float(price_str)
            except ValueError:
                pass
        
        # Also try to extract price from patterns like "14,80"
        if not self.current_item['price']:
            standalone_price = re.search(r'\b(\d{1,2}[,.]\d{2})\b', text)
            if standalone_price:
                price_str = standalone_price.group(1).replace(',', '.')
                try:
                    price_val = float(price_str)
                    if 5.0 <= price_val <= 50.0:  # Reasonable price range for lunch
                        self.current_item['price'] = price_val
                except ValueError:
                    pass
        
        # Extract category
        categories = ['Menu', 'Vegi', 'Hit', 'Frühstück']
        for cat in categories:
            if cat in text and not self.current_item['category']:
                self.current_item['category'] = cat
                break
        
        # Add to description if it's not just price/category
        if (not price_match and text not in categories and len(text) > 3 and
            not re.search(r'\b\d{1,2}[,.]\d{2}\b', text) and  # Skip standalone prices
            'CHF' not in text):
            
            # Clean up the text
            clean_text = re.sub(r'\s+', ' ', text).strip()
            if len(clean_text) > 3 and len(clean_text) < 200:  # Reasonable length
                if self.current_item['description']:
                    self.current_item['description'] += ' ' + clean_text
                else:
                    self.current_item['description'] = clean_text


class EurestMenuScraper:
    """Web scraper for Eurest Kaserne Timeout lunch menu."""
    
    def __init__(self):
        self.base_url = "https://clients.eurest.ch/kaserne/de/Timeout"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'de-DE,de;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive'
        }
    
    def fetch_page(self) -> Optional[str]:
        """Fetch the webpage and return the HTML content."""
        try:
            # Remove gzip from headers to avoid compression issues
            headers = self.headers.copy()
            headers['Accept-Encoding'] = 'identity'
            
            request = urllib.request.Request(self.base_url, headers=headers)
            with urllib.request.urlopen(request, timeout=10) as response:
                # Handle encoding
                content = response.read()
                
                # Check if content is gzipped
                if content.startswith(b'\x1f\x8b'):
                    import gzip
                    content = gzip.decompress(content)
                
                # Decode content
                charset = response.headers.get_content_charset()
                if charset:
                    return content.decode(charset)
                else:
                    # Try common encodings
                    for encoding in ['utf-8', 'iso-8859-1', 'windows-1252']:
                        try:
                            return content.decode(encoding)
                        except UnicodeDecodeError:
                            continue
                    return content.decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"Error fetching webpage: {e}")
            return None
    
    def parse_html(self, html_content: str) -> List[Dict]:
        """Parse HTML content to extract menu items."""
        parser = MenuHTMLParser()
        parser.feed(html_content)
        
        # Clean up and validate menu items
        cleaned_items = []
        for item in parser.menu_items:
            if item['name'] and (item['price'] or item['description']):
                # Clean up description - remove excessive text
                if item['description']:
                    # Split by sentences and take only the first few relevant ones
                    desc = item['description']
                    # Remove long promotional text and contact info
                    sentences = re.split(r'[.!?]', desc)
                    relevant_sentences = []
                    for sentence in sentences[:3]:  # Max 3 sentences
                        sentence = sentence.strip()
                        if (len(sentence) > 5 and len(sentence) < 100 and
                            not any(skip in sentence.lower() for skip in 
                            ['feedback', 'umfrage', 'lächeln', 'öffnungszeiten', 'burger-variationen',
                             'behling', 'betriebsleiter', 'compass', 'kaserne@', '+41', 'jobs',
                             'copyright', 'impressum', 'datenschutz', 'cookies']) and
                            not re.search(r'[a-z]+@[a-z]+\.[a-z]+', sentence) and  # email
                            not re.search(r'\+\d+\s+\d+', sentence)):  # phone
                            relevant_sentences.append(sentence)
                    
                    item['description'] = '. '.join(relevant_sentences)
                    if item['description'] and not item['description'].endswith('.'):
                        item['description'] += '.'
                
                # Extract price from description if not found yet
                if not item['price'] and item['description']:
                    price_in_desc = re.search(r'(\d{1,2}[,.]\d{2})', item['description'])
                    if price_in_desc:
                        try:
                            price_val = float(price_in_desc.group(1).replace(',', '.'))
                            if 5.0 <= price_val <= 50.0:
                                item['price'] = price_val
                                # Remove price from description
                                item['description'] = re.sub(r'\s*\d{1,2}[,.]\d{2}\s*', ' ', item['description'])
                        except ValueError:
                            pass
                
                cleaned_items.append(item)
        
        return cleaned_items
    
    def extract_date_from_html(self, html_content: str) -> Optional[str]:
        """Extract date information from HTML."""
        date_pattern = r'\b\d{1,2}\.\d{1,2}\.\d{2,4}\b'
        matches = re.findall(date_pattern, html_content)
        return matches[0] if matches else None
    
    def scrape_menu(self) -> Dict:
        """Main method to scrape the complete menu."""
        print("Fetching menu from Eurest Kaserne Timeout...")
        
        html_content = self.fetch_page()
        if not html_content:
            return {"error": "Failed to fetch webpage"}
        
        menu_items = self.parse_html(html_content)
        display_date = self.extract_date_from_html(html_content)
        
        result = {
            "restaurant": "Eurest Kaserne Timeout",
            "location": "Papiermühlestrasse 15, 3014 Bern",
            "url": self.base_url,
            "date_info": {
                "scraped_at": datetime.now().isoformat(),
                "display_date": display_date
            },
            "menu_items": menu_items,
            "total_items": len(menu_items)
        }
        
        return result
    
    def display_menu(self, menu_data: Dict):
        """Display the menu in a formatted way."""
        if "error" in menu_data:
            print(f"Error: {menu_data['error']}")
            return
        
        print("=" * 60)
        print(f"🍽️  {menu_data['restaurant']}")
        print(f"📍 {menu_data['location']}")
        print(f"🌐 {menu_data['url']}")
        print(f"📅 Scraped: {menu_data['date_info']['scraped_at'][:19]}")
        if menu_data['date_info']['display_date']:
            print(f"📅 Menu Date: {menu_data['date_info']['display_date']}")
        print("=" * 60)
        
        if not menu_data['menu_items']:
            print("No menu items found.")
            return
        
        # Show price statistics
        stats = self.get_price_statistics(menu_data['menu_items'])
        if stats:
            print(f"\n💰 Price Range: {stats['price_range']} | Average: CHF {stats['avg_price']:.2f}")
        
        # Organize by categories
        categories = self.get_all_menu_categories(menu_data['menu_items'])
        
        print(f"\n📋 Today's Menu ({menu_data['total_items']} items):\n")
        
        for category, items in categories.items():
            if items:
                print(f"🏷️  {category.upper()} ({len(items)} items):")
                for i, item in enumerate(items, 1):
                    print(f"  {i}. {item['name']}")
                    
                    if item['description']:
                        print(f"     📝 {item['description']}")
                    
                    if item['price']:
                        print(f"     💰 CHF {item['price']:.2f}")
                    
                    print()
                print()
    
    def save_to_json(self, menu_data: Dict, filename: str = None):
        """Save menu data to JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"eurest_menu_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(menu_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Menu saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving to file: {e}")
    
    def get_all_menu_categories(self, menu_items: List[Dict]) -> Dict:
        """Organize menu items by category."""
        categories = {
            'Frühstück': [],
            'Menu': [],
            'Vegi': [],
            'Hit': [],
            'Other': []
        }
        
        for item in menu_items:
            category = item.get('category', 'Other')
            if category in categories:
                categories[category].append(item)
            else:
                categories['Other'].append(item)
        
        # Remove empty categories
        return {k: v for k, v in categories.items() if v}
    
    def get_price_statistics(self, menu_items: List[Dict]) -> Dict:
        """Calculate price statistics for the menu."""
        prices = [item['price'] for item in menu_items if item['price']]
        
        if not prices:
            return {}
        
        return {
            'min_price': min(prices),
            'max_price': max(prices),
            'avg_price': round(sum(prices) / len(prices), 2),
            'price_range': f"CHF {min(prices):.2f} - CHF {max(prices):.2f}"
        }


def create_simple_scraper():
    """Create a simple regex-based scraper as fallback."""
    def simple_scrape():
        """Simple regex-based scraper using urllib."""
        url = "https://clients.eurest.ch/kaserne/de/Timeout"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
                'Accept-Encoding': 'identity'  # Avoid compression
            }
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=10) as response:
                content = response.read()
                
                # Handle gzip compression if present
                if content.startswith(b'\x1f\x8b'):
                    import gzip
                    content = gzip.decompress(content)
                
                # Decode content
                html_content = content.decode('utf-8', errors='ignore')
            
            print("Successfully fetched webpage!")
            print("Content length:", len(html_content))
            print("\nLooking for menu items...")
            
            # Extract menu items using regex
            menu_items = []
            
            # Look for h3 elements with menu items
            h3_pattern = r'<h3[^>]*>([^<]+)</h3>'
            h3_matches = re.findall(h3_pattern, html_content, re.IGNORECASE)
            
            for h3_text in h3_matches:
                name = h3_text.strip()
                
                # Skip non-menu items
                skip_patterns = ['öffnungszeiten', 'kontakt', 'ihre meinung', 'wir machen', 
                               'hot & delicious', 'dessert bieten wir', 'burger vom']
                if any(pattern in name.lower() for pattern in skip_patterns):
                    continue
                
                if len(name) > 3:
                    print(f"Found potential menu item: {name}")
                    
                    # Look for price and description around this item
                    # Create a window around the h3 tag
                    h3_pos = html_content.find(f'<h3[^>]*>{re.escape(h3_text)}</h3>')
                    if h3_pos >= 0:
                        # Get 1000 characters after the h3
                        window = html_content[h3_pos:h3_pos + 1000]
                        
                        # Extract price
                        price_match = re.search(r'CHF\s*(\d+[,.]?\d*)', window)
                        price = float(price_match.group(1).replace(',', '.')) if price_match else None
                        
                        # Extract description (text between tags)
                        text_matches = re.findall(r'>([^<]+)<', window)
                        description_parts = []
                        for text in text_matches:
                            text = text.strip()
                            if (text and len(text) > 3 and 
                                not re.search(r'CHF\s*\d+', text) and
                                text not in ['Menu', 'Vegi', 'Hit', 'Frühstück'] and
                                text != name):
                                description_parts.append(text)
                        
                        description = ' '.join(description_parts[:3])  # Limit description
                        
                        item = {
                            'name': name,
                            'description': description,
                            'price': price,
                            'category': None
                        }
                        
                        # Detect category
                        for cat in ['Menu', 'Vegi', 'Hit', 'Frühstück']:
                            if cat in window:
                                item['category'] = cat
                                break
                        
                        menu_items.append(item)
            
            # Alternative approach: look for patterns with CHF prices
            if not menu_items:
                print("Trying alternative pattern matching...")
                # Look for text patterns that might be menu items with prices
                price_pattern = r'([^<>\n]{10,80})\s*.*?CHF\s*(\d+[,.]?\d*)'
                price_matches = re.findall(price_pattern, html_content)
                
                for match in price_matches:
                    name = re.sub(r'<[^>]+>', '', match[0]).strip()
                    price = match[1]
                    
                    # Filter out non-menu items
                    if (len(name) > 5 and len(name) < 60 and 
                        not any(skip in name.lower() for skip in 
                        ['copyright', 'compass', 'group', 'öffnungszeiten', 'kontakt', 'impressum'])):
                        
                        print(f"Found item with price: {name} - CHF {price}")
                        item = {
                            'name': name,
                            'description': "",
                            'price': float(price.replace(',', '.')),
                            'category': None
                        }
                        menu_items.append(item)
            
            print(f"Found {len(menu_items)} menu items")
            
            return {
                'restaurant': 'Eurest Kaserne Timeout',
                'location': 'Papiermühlestrasse 15, 3014 Bern',
                'url': url,
                'date_info': {
                    'scraped_at': datetime.now().isoformat(),
                    'display_date': None
                },
                'menu_items': menu_items,
                'total_items': len(menu_items)
            }
            
        except Exception as e:
            print(f"Error in simple scraper: {e}")
            return {'error': str(e)}
    
    return simple_scrape


def main():
    """Main function to run the scraper."""
    scraper = EurestMenuScraper()
    
    # Try the main scraper first
    menu_data = scraper.scrape_menu()
    
    # If no items found, try the simple scraper
    if menu_data.get('total_items', 0) == 0:
        print("\nTrying alternative scraping method...")
        simple_scrape = create_simple_scraper()
        simple_data = simple_scrape()
        
        if 'error' not in simple_data and simple_data.get('menu_items'):
            menu_data = simple_data
            menu_data['total_items'] = len(simple_data['menu_items'])
    
    # Display the menu
    scraper.display_menu(menu_data)
    
    # Save to JSON file
    scraper.save_to_json(menu_data)
    
    # Return data for potential further use
    return menu_data


if __name__ == "__main__":
    menu_data = main()
