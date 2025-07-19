# CNC Tool Parameter Calculator

A Progressive Web App (PWA) for calculating and comparing CNC machining parameters across tool types and materials. Includes tool life estimation, force and power predictions, export to PDF, and beginner-to-expert profiles.

## 🌐 Live App

[https://your-app-url.com](https://your-app-url.com)

## 📦 Features

* Tool selection: Drill, Endmill, Ball mill, Face mill, Corner mill
* Material support: Steel (EN24, EN8, etc.), Aluminum (6061, 7075), Titanium, Stainless, Inconel, and more
* Tool material options: Carbide, HSS, Coated variants
* Force & power estimation
* Tool life calculator with safety constraints
* User Profiles: Beginner → Expert
* PDF report export (basic & detailed)
* PWA: Mobile installable, offline-first
* Fully responsive dark UI

## 📁 Project Structure

```
├── app.py                  # Flask app logic
├── templates/
│   ├── base.html           # Shared layout
│   └── index.html          # UI form
├── static/
│   ├── manifest.json       # PWA manifest
│   ├── service-worker.js   # PWA offline support
│   ├── icon-192.png        # App icon (192px)
│   └── icon-512.png        # App icon (512px)
├── utils/
│   ├── pdf_generator.py    # PDF export logic
│   └── calculations.py     # Core formulas
├── data/
│   ├── material_data.py    # Material Vc and fz presets
│   └── tool_types.py       # Tool type config
├── .well-known/
│   └── assetlinks.json     # Android TWA support
├── requirements.txt        # Python dependencies
└── README.md
```

## ⚙️ Setup & Run

```bash
# Clone the repo
$ git clone https://github.com/yourname/cnc-tool-param-calc
$ cd cnc-tool-param-calc

# (Optional) Create virtual env
$ python -m venv venv && source venv/bin/activate

# Install dependencies
$ pip install -r requirements.txt

# Run the app
$ python app.py
```

## 🚀 Deployment

* PWA ready — no extra setup needed
* Host on Render, GitHub Pages + Flask backend, or Firebase Hosting + Cloud Run

## 📱 TWA / Android Support

* Host `assetlinks.json` under `/.well-known/`
* Package via [Bubblewrap](https://github.com/GoogleChromeLabs/bubblewrap) or TWA Builder
* Replace package name and SHA key in assetlinks

## 📃 License

MIT

---

Built with ❤️ for machinists, engineers, and curious learners.
