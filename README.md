# 🛠️ CNC Tool Parameter Calculator

A full-featured Progressive Web App (PWA) built with **Flask** and **Vanilla HTML/JS**, designed to calculate, compare, and optimize CNC machining parameters for various tools and materials. Includes advanced cutting force and power predictions, tool life estimation, surface finish metrics, and PDF export — all packaged in a clean, mobile-friendly UI.

> 💡 Perfect for machinists, manufacturing engineers, and mechanical design enthusiasts who need quick, accurate machining calculations.

---

## 🌐 Live App

🔗 [https://cnc-tool-param-calc.onrender.com](https://cnc-tool-param-calc.onrender.com)  
> *(Hosted on Render. Fully PWA-ready for mobile installability.)*

---

## ✨ Features

- 🔧 **Tool Types**: Drill, Endmill, Face Mill, Ball Mill, Corner Radius Endmill  
- 🧱 **Material Database**:  
  - Steels: EN8, EN24, Mild Steel  
  - Aluminum: 6061, 7075  
  - Others: Stainless Steel, Titanium, Inconel  
- ⚙️ **Tool Materials**: HSS, Carbide, Coated Carbide (e.g., TiN, TiAlN)  
- 📐 **Smart Calculations**:  
  - Cutting Force & Power Estimation  
  - Tool Life Prediction (Taylor’s Equation)  
  - Surface Finish (Ra) Estimator  
- 📄 **PDF Export**: Generate detailed or basic machining parameter reports  
- 🌓 **Offline-First PWA**: Works without internet once loaded  
- 🖥️ **Responsive Dark UI**: Optimized for desktop and mobile

---

## 📁 Project Structure
```
cnc_tool_param_calc/
├── app.py # Flask backend
├── templates/
│ ├── base.html # Shared HTML layout
│ └── index.html # Main frontend form
├── static/
│ ├── manifest.json # PWA manifest
│ ├── service-worker.js # Offline support
│ ├── icon-192.png # App icon (192px)
│ └── icon-512.png # App icon (512px)
├── utils/
│ ├── pdf_generator.py # PDF export logic
│ └── calculations.py # Machining formulas
├── data/
│ ├── material_data.py # Material cutting data
│ └── tool_types.py # Tool config presets
├── .well-known/
│ └── assetlinks.json # Android TWA support
├── requirements.txt # Python dependencies
└── README.md # This file!
```
---

## ⚙️ Getting Started

- Clone the repository
git clone https://github.com/Steelbot2803/cnc_tool_param_calc.git
cd cnc_tool_param_calc
- (Optional) Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
- Install dependencies
pip install -r requirements.txt
- Start the Flask app
python app.py
- Visit http://localhost:5000 in your browser.

---

## 🚀 Deployment Options
- Render (zero-config for Flask apps)
- Firebase Hosting + Cloud Run
- Docker / VPS

---

## ⚠️ GitHub Pages requires external backend

📱 Android Trusted Web Activity (TWA) Support
- Want to publish this on the Play Store? TWA makes it possible.
- Place assetlinks.json inside /.well-known/
- Use Bubblewrap or PWABuilder to generate an APK
- Replace the SHA256 certificate and package name in assetlinks.json

---

## 📄 License
This project is licensed under the MIT License. See [LICENSE](LICENSE.txt) for details.

---

## 🙌 Credits
Built with ❤️ by Siddharth Kumar Ananda Kumar
For engineers, machinists, and curious makers everywhere.
