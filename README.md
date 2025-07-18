# 🍽️ Lunchinator

Eine Progressive Web App (PWA), die das tägliche Mittagsmenü der Kaserne Timeout (Eurest) in Bern anzeigt. Die App scrapt automatisch die neuesten Menüdaten direkt von der offiziellen Website und präsentiert sie in einem benutzerfreundlichen Dark Mode Interface.

## ✨ Features

### 🌐 **Web Scraping**
- Automatisches Scraping der Eurest Kaserne Timeout Website
- Intelligente Datenextraktion mit mehreren Fallback-Strategien
- Filtert automatisch Frühstück und Dessert heraus
- Erkennt und kategorisiert Menüs (Menu, Vegi, Hit)

### 📱 **Progressive Web App (PWA)**
- Vollständig installierbar auf mobilen Geräten und Desktop
- Offline-Funktionalität durch Service Worker
- App-ähnliche Erfahrung mit nativer Navigation
- Automatische Updates und Caching

### 🌑 **Dark Mode Design**
- Permanent aktivierter Dark Mode für bessere Lesbarkeit
- Moderne, minimalistische Benutzeroberfläche
- Responsive Design für alle Bildschirmgrößen
- Smooth Animations und Hover-Effekte

### 🎯 **Smart Menu Detection**
- Erkennt alle verfügbaren Mittagsmenüs (normalerweise 2-3 Stück)
- Automatische Kategorisierung:
  - **Menu**: Fisch und allgemeine Hauptgerichte
  - **Vegi**: Vegetarische Gerichte
  - **Hit**: Fleischgerichte
- Duplikat-Erkennung und Filterung

## 🚀 Getting Started

### Installation

1. **Repository klonen:**
   ```bash
   git clone https://github.com/marcstae/lunchinator.git
   cd lunchinator
   ```

2. **Webserver starten:**
   ```bash
   # Mit Python
   python -m http.server 8000
   
   # Mit Node.js
   npx serve .
   
   # Mit PHP
   php -S localhost:8000
   ```

3. **App öffnen:**
   - Navigiere zu `http://localhost:8000` in deinem Browser
   - Oder öffne die `index.html` direkt (eingeschränkte Funktionalität)

### PWA Installation

1. Öffne die Website in einem modernen Browser (Chrome, Firefox, Safari)
2. Klicke auf das Install-Banner oder verwende "Zur Startseite hinzufügen"
3. Die App wird als eigenständige Anwendung installiert

## 🛠️ Technische Details

### Architektur

```
lunchinator/
├── index.html          # Haupt-App mit allem Code
├── manifest.json       # PWA Manifest
├── sw.js              # Service Worker für Offline-Funktionalität
└── README.md          # Diese Datei
```

### Web Scraping Technologie

Die App verwendet einen mehrstufigen Ansatz zum Scraping:

1. **API-Endpunkt Tests**: Versucht verschiedene potentielle API-Endpoints
2. **Strukturierte Text-Extraktion**: Parst das HTML nach dem Eurest-Menüformat
3. **DOM-basiertes Scraping**: Fallback mit CSS-Selektoren
4. **Pattern-Matching**: Regex-basierte Extraktion als letzte Option

### Browser-Kompatibilität

- ✅ Chrome 60+
- ✅ Firefox 55+
- ✅ Safari 11+
- ✅ Edge 79+
- ✅ Mobile Browsers (iOS Safari, Chrome Mobile)

### Performance

- **Erstladezeit**: < 2 Sekunden
- **Caching**: Aggressive Caching für Offline-Nutzung
- **Bundle-Größe**: < 50KB (alles in einer Datei)
- **Mobile-optimiert**: Touch-freundliche Bedienung

## 🔧 Konfiguration

### Anpassung der Quelle

Um eine andere Eurest-Location zu verwenden, ändere die `apiBase` URL in `index.html`:

```javascript
this.apiBase = 'https://clients.eurest.ch/DEINE-LOCATION/de/RESTAURANT-NAME';
```

### Menu-Filterung anpassen

Bearbeite die Arrays in den Funktionen `shouldIncludeMenuItem()`:

```javascript
// Weitere Begriffe hinzufügen oder entfernen
const breakfastKeywords = ['frühstück', 'kaffee', ...];
const dessertKeywords = ['dessert', 'kuchen', ...];
```

## 🐛 Troubleshooting

### Keine Menüs werden angezeigt

1. **Netzwerkverbindung prüfen**: Stelle sicher, dass die Eurest-Website erreichbar ist
2. **Browser-Konsole öffnen**: Drücke F12 und schaue nach Fehlermeldungen
3. **CORS-Probleme**: Verwende einen lokalen Server statt `file://` URLs
4. **Website-Änderungen**: Die Eurest-Website könnte ihre Struktur geändert haben

### PWA Installation funktioniert nicht

1. **HTTPS erforderlich**: PWAs benötigen HTTPS (oder localhost)
2. **Manifest-Datei**: Stelle sicher, dass `manifest.json` korrekt geladen wird
3. **Service Worker**: Prüfe ob der Service Worker registriert wurde

### Falsche Menüs werden angezeigt

1. **Filterung prüfen**: Möglicherweise müssen die Filter-Keywords angepasst werden
2. **Cache leeren**: Lösche den Browser-Cache und lade neu
3. **Website-Update**: Die Struktur der Quell-Website könnte sich geändert haben

## 🤝 Contributing

Beiträge sind willkommen! Bitte:

1. Fork das Repository
2. Erstelle einen Feature-Branch (`git checkout -b feature/amazing-feature`)
3. Committe deine Änderungen (`git commit -m 'Add amazing feature'`)
4. Push zum Branch (`git push origin feature/amazing-feature`)
5. Öffne eine Pull Request

### Development Setup

```bash
# Repository klonen
git clone https://github.com/marcstae/lunchinator.git
cd lunchinator

# Development Server starten
python -m http.server 8000

# Änderungen testen
# Öffne http://localhost:8000 im Browser
# Developer Tools öffnen für Debugging
```

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe [LICENSE](LICENSE) für Details.

## 🙋‍♂️ Support

Bei Fragen oder Problemen:

1. **Issues**: Öffne ein [GitHub Issue](https://github.com/marcstae/lunchinator/issues)
2. **Diskussionen**: Nutze [GitHub Discussions](https://github.com/marcstae/lunchinator/discussions)
3. **Email**: Kontaktiere den Entwickler direkt

## 🎯 Roadmap

### Geplante Features

- [ ] **Push-Benachrichtigungen** für neue Menüs
- [ ] **Favoriten-System** für beliebte Gerichte
- [ ] **Nährwert-Informationen** wenn verfügbar
- [ ] **Bewertungssystem** für Gerichte
- [ ] **Mehrere Restaurants** in einer App
- [ ] **Allergene-Filter** basierend auf verfügbaren Daten

### Technische Verbesserungen

- [ ] **TypeScript-Konvertierung** für bessere Typsicherheit
- [ ] **Build-System** mit Webpack/Vite
- [ ] **Testing-Framework** für Scraping-Logik
- [ ] **CI/CD-Pipeline** für automatische Deployments
- [ ] **Error-Monitoring** mit Sentry oder ähnlich

## 📊 Analytics & Monitoring

Die App sammelt keine Nutzerdaten und verwendet keine Tracking-Tools. Alle Daten bleiben lokal auf dem Gerät des Nutzers.

## 🔒 Sicherheit

- **Keine Datensammlung**: Die App speichert keine persönlichen Daten
- **Lokale Speicherung**: Nur Menüdaten werden im Browser-Cache gespeichert
- **HTTPS-Only**: Alle externen Anfragen verwenden sichere Verbindungen
- **CSP-Headers**: Content Security Policy verhindert XSS-Angriffe

---

**Made with ❤️ in Bern, Switzerland**

*Diese App ist nicht offiziell mit Eurest oder Compass Group verbunden.*
