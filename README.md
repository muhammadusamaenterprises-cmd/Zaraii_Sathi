🌾 Zarai Saathi (زرعي ساتھی)

Sindh Agriculture Enterprise Platform & Cloud Command Desk

Zarai Saathi is an integrated agricultural management and marketplace platform tailored for farmers, traders, equipment suppliers, agricultural extension experts, and Sindh Government market committee officers. It features multilingual support (English, Urdu, and Sindhi), an interactive Mandi Rates & Government benchmark tracker, a Crop Profit & Precision Input Calculator, a Daily Farm Task Manager, and an AI Saathi Assistant equipped with computer vision leaf-health diagnostics.

🚀 Key Features

Multi-Role Workspace Access:

Farmer Command Center: Weather, pest alerts, crop calendar, and input planners.

Verified Buyer & Trader Hub: Direct WhatsApp negotiation and harvest listings.

Agri Equipment Supplier: Tractor, harvester, and laser-leveler sharing portal.

Extension Agri Expert: Crop disease monitoring and advisory tools.

Sindh Market Committee Officer: Official rate notifications and grievance/dispute logging.

Multilingual Interface:

Instant translation toggle between English, اردو (Urdu), and سنڌي (Sindhi) with automatic RTL formatting and Nastaliq typography.

OpenCV & AI Assistant Integration:

Online Mode: Powered by Gemini AI via secure API integration.

Offline / Standalone Mode: Built-in expert agronomic rules and color-threshold computer vision fallbacks ensuring the app is 100% workable even without an active internet connection or Python backend.

Live Weather Integration:

Real-time weather forecasting powered by the Open-Meteo REST API across major Sindh districts (Hyderabad, Sukkur, Larkana, Mirpurkhas, Nawabshah, and Karachi).

Cloud Session & Data Management:

Simulated Google OAuth profile synchronization, JSON data export/import backups, and printable farm summary reports.

🛠️ Project Structure

index.html — The complete standalone frontend workspace (Tailwind CSS, FontAwesome, JavaScript engine).

backend.py — Optional Flask & OpenCV backend server for server-side computer vision leaf analysis and structured JSON AI responses.

requirements.txt — Python dependencies for running backend.py.

⚙️ How to Run

Option A: Pure Frontend Standalone Mode (Zero Installation Required)

Because Zarai Saathi includes intelligent browser-side fallbacks, you can run the entire application without installing Python or running a backend server:

Double-click or open index.html in any modern web browser (Chrome, Firefox, Edge, Safari).

Explore the dashboards, calculate crop profits, test the AI Saathi assistant, and log farm records instantly.

Option B: Full-Stack Mode with OpenCV Backend

If you want to run the optional Flask and OpenCV backend locally for server-side image analysis:

Install Python (Python 3.10 or higher recommended).

Install the required dependencies:

pip install -r requirements.txt


Start the Flask backend server:

python backend.py


The server will run locally at http://127.0.0.1:5000.

Open index.html in your browser. The frontend will automatically connect to the local API for image diagnosis and chat.

📋 License & Compliance

Developed for agricultural empowerment in Sindh, Pakistan under regional market guidelines and open web standards.
