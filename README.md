# RFID Tracker Prototype

A real-time RFID-based tracking system prototype built with Flask and SQLite.

It tracks individual valve parts through workflow zones — Receiving, Warehouse, Machine Shop, and Shipping — with live updates via a web dashboard.

## ✨ Features

- Live dashboard with part locations
- Scan simulation and manual entry forms
- Zone and job ID filters
- Color-coded idle alerts (yellow/red)
- Per-part scan history with timestamps
- Average time in each zone (with Chart.js visualization)
- CSV export for reporting and audits
- Simple delete/archive flow ("Done" button)

## 🛠 Tech Stack

- Python (Flask)
- SQLite
- HTML + JavaScript (Vanilla + Chart.js)
- Minimal CSS styling

## 🚀 Getting Started

pip install -r requirements.txt  
python app.py

Then open your browser to:  
http://127.0.0.1:5000

## 📁 Project Structure

RFID/
├── app.py                # Flask app and routes  
├── templates/            # HTML dashboard, forms, history  
│   ├── dashboard.html  
│   ├── simulate.html  
│   ├── new_part.html  
│   └── history.html  
├── seed_test_data.py     # Optional script to seed test scans  
├── requirements.txt  
├── .gitignore  
└── rfid.db               # SQLite database (excluded from git)

## 📤 Export + Reporting

- Use the "Download CSV" button on the dashboard to export filtered results
- Use the "Scan History" link to audit part-level movement

## 📈 Dashboard Insights

- Summary of parts per zone
- Average time per zone (text + chart)
- Real-time refresh every 10 seconds

## 📜 License

MIT License — free for personal, academic, or commercial use. Attribution appreciated but not required.
