# 🍽️ Eatinator

A Progressive Web App (PWA) that displays the daily lunch menu from the Eurest restaurant at Kaserne Bern. It scrapes the menu directly from the website and presents it in a clean, dark-mode interface.

## ✨ Features

- **Automatic Scraping**: Fetches the latest menu data automatically.
- **PWA**: Installable on mobile and desktop devices for an app-like experience with offline access.
- **Dark Mode**: Easy-to-read interface, perfect for all lighting conditions.
- **Menu Categorization**: Automatically categorizes meals into "Menu", "Vegi", and "Hit".
- **Fallback System**: If direct API access fails, it falls back to scraping the HTML to ensure you always get the menu.
- **Zero Dependencies**: Runs in any modern browser without needing any special setup.

## 🔧 How It Works

The application first attempts to fetch menu data from a series of potential, unnofficial API endpoints on the `clients.eurest.ch` domain. If these endpoints do not respond or do not provide valid menu data, the app automatically falls back to a more robust method:

1.  It fetches the entire HTML content of the restaurant's menu page.
2.  It then parses this HTML, looking for patterns that indicate menu items, such as titles, descriptions, prices, and categories.
3.  It uses a series of increasingly general CSS selectors to find the menu content, making it resilient to minor changes in the website's structure.
4.  The extracted data is cleaned, categorized, and displayed to the user.

This ensures that even without a formal API, the Eatinator can reliably provide the daily menu.
