# Study Burnout Tracker

A Python Flask + PostgreSQL web application for tracking student study habits and predicting burnout risk.

## Features
- Register and login
- Add daily burnout records
- Track sleep hours, study hours, stress level, mood level, and breaks
- Calculate burnout score
- Calculate productivity score
- Show weekly analytics with a built-in chart
- Store data in PostgreSQL

## How to Run

### 1. Install packages
```bash
pip install -r requirements.txt
```

### 2. Create PostgreSQL database
Create a database named:
```text
smart_planner
```

### 3. Configure `.env`
Open `.env` and set your PostgreSQL password:
```env
DB_NAME=smart_planner
DB_USER=postgres
DB_PASSWORD=your_password
```

### 4. Create tables
Open pgAdmin → smart_planner → Query Tool.
Paste and run the code from `schema.sql`.

### 5. Start app
```bash
python app.py
```

Open in browser:
```text
http://127.0.0.1:5000
```

## Main Files
- `app.py` - Flask routes and main application
- `db.py` - PostgreSQL connection functions
- `burnout.py` - OOP class for burnout and productivity algorithms
- `schema.sql` - PostgreSQL database tables
- `templates/` - HTML pages
- `static/style.css` - UI design
