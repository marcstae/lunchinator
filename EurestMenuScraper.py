# Eurest Kaserne Timeout Menu Scraper

A Python web scraper for the lunch menu from Eurest Kaserne Timeout restaurant in Bern.

## Features

- Scrapes daily lunch menu items with names, descriptions, prices, and categories
- Handles different menu categories (Menu, Vegi, Hit, Frühstück)
- Extracts price information and calculates statistics
- Saves data to JSON format for further processing
- Uses only built-in Python libraries (no external dependencies required)
- Handles network issues and encoding problems gracefully

## Usage

### Basic Usage

```python
# Run the scraper
python python.py
```

### Programming Usage

```python
from python import EurestMenuScraper

# Create scraper instance
scraper = EurestMenuScraper()

# Scrape the menu
menu_data = scraper.scrape_menu()

# Display the menu
scraper.display_menu(menu_data)

# Save to JSON
scraper.save_to_json(menu_data, "today_menu.json")
```

### Example Output

```
============================================================
🍽️  Eurest Kaserne Timeout
📍 Papiermühlestrasse 15, 3014 Bern
🌐 https://clients.eurest.ch/kaserne/de/Timeout
📅 Scraped: 2025-07-18T14:07:13
📅 Menu Date: 6.1.10
============================================================

💰 Price Range: CHF 14.80 - CHF 14.80 | Average: CHF 14.80

📋 Today's Menu (3 items):

🏷️  MENU (1 items):
  1. Schlemmerfilet Italiano
     📝 Gemüsereis, Romanesco.
     💰 CHF 14.80

🏷️  VEGI (1 items):
  1. Tortellini
     📝 mit Ricotta-Spinat Füllung, Tagessalat.
     💰 CHF 14.80

🏷️  HIT (1 items):
  1. Schweinsrahmschnitzel (CH)
     💰 CHF 14.80
```

## JSON Output Format

The scraper saves data in the following JSON format:

```json
{
  "restaurant": "Eurest Kaserne Timeout",
  "location": "Papiermühlestrasse 15, 3014 Bern",
  "url": "https://clients.eurest.ch/kaserne/de/Timeout",
  "date_info": {
    "scraped_at": "2025-07-18T14:07:13.123456",
    "display_date": "6.1.10"
  },
  "menu_items": [
    {
      "name": "Schlemmerfilet Italiano",
      "description": "Gemüsereis, Romanesco.",
      "price": 14.8,
      "category": "Menu"
    }
  ],
  "total_items": 3
}
```

## Requirements

- Python 3.6+
- Internet connection
- No external libraries required (uses built-in urllib, html.parser, re, json, datetime)

## Error Handling

The scraper includes robust error handling for:
- Network connectivity issues
- Website structure changes
- Encoding problems
- Missing data

## Limitations

- Depends on the website structure (may need updates if the site changes)
- Limited to current day's menu
- May not capture all special offers or temporary menu changes

## Restaurant Information

- **Name:** Eurest Kaserne Timeout
- **Location:** Papiermühlestrasse 15, 3014 Bern
- **Website:** https://clients.eurest.ch/kaserne/de/Timeout
- **Hours:** Monday-Friday 6:00-19:00, Lunch 11:30-13:00

## License

This scraper is for educational and personal use only. Please respect the website's terms of service and don't overload their servers with frequent requests.
