# 🚆 Bio-Toilet Inspection System

An AI-assisted railway inspection platform for Indian Railways that automates bio-toilet inspection by integrating AI detection, NTES coach composition, and intelligent coach mapping.

The system receives AI-generated bio-toilet inspection results, synchronizes the official train composition from NTES, maps detected tanks to the correct coaches, and provides inspection reports for railway inspectors.

---

# 📖 Overview

Traditional railway bio-toilet inspection is manual, time-consuming, and prone to human error.

This project automates the workflow by combining:

- AI-based bio-toilet defect detection
- NTES coach composition synchronization
- Automatic tank-to-coach mapping
- Inspection history
- Report generation
- Flutter mobile application for inspectors

---

# 🏗 Architecture

```
                AI Service
                     │
                     │
         POST /api/v1/ai/results
                     │
                     ▼
             AI_RESULT_RAW
                     │
                     │
Inspector             │
      │               │
      ▼               │
Fetch Train           │
      │               │
      ▼               │
NTES Synchronization  │
      │               │
      ▼               │
NTES Coach Composition
      │
      ▼
Mapping Workflow
      │
      ▼
Coach
Tank
TankDefect
      │
      ▼
Flutter Application
```

---

# 🚀 Features

## AI Integration

- Immutable AI payload persistence
- AI contract validation
- Duplicate request protection
- AI acknowledgement API

---

## NTES Integration

- Playwright-powered NTES client
- Automatic coach composition retrieval
- HTML parsing
- Coach normalization
- Composition synchronization

---

## Mapping Engine

- Reverse coach composition
- AI tank mapping
- Tank persistence
- Defect translation
- Inspection summary generation

---

## Inspection Management

- Inspection creation
- Live inspection synchronization
- Inspection statistics
- Inspection history

---

## Reports

- Inspection reports
- Dashboard statistics
- PDF export

---

# 🛠 Tech Stack

## Backend

- Python 3.14
- Django
- Django REST Framework

## Database

- PostgreSQL

## Browser Automation

- Playwright

## AI

- External AI Service

## Mobile

- Flutter

---

# 📂 Project Structure

```
backend/

├── apps/
│   ├── ai/
│   ├── common/
│   ├── inspection/
│   ├── mapping/
│   ├── ntes/
│   ├── reports/
│   └── users/
│
├── config/
│
├── media/
│
├── static/
│
└── manage.py
```

---

# 🔄 Inspection Workflow

```
AI
 │
 ▼
Upload Inspection Results
 │
 ▼
AI_RESULT_RAW
 │
 ▼
Inspector Opens App
 │
 ▼
Fetch Train
 │
 ▼
NTES Synchronization
 │
 ▼
Coach Mapping
 │
 ▼
Coach Details
 │
 ▼
Inspection Report
```

---

# 🧠 Mapping Workflow

1. Receive AI payload
2. Store immutable AI result
3. Synchronize NTES composition
4. Reverse coach order
5. Map AI tanks to NTES coaches
6. Persist Coach
7. Persist Tank
8. Persist TankDefect
9. Update inspection statistics

---

# 📡 API Modules

## AI

- POST AI Results

## Inspection

- Create Inspection

## NTES

- Fetch Train

## Mapping

- Automatic Mapping Workflow

## Reports

- Dashboard
- Export PDF

---

# 🧪 Testing

The project uses:

- pytest
- pytest-django

Run all tests

```bash
pytest
```

Run specific app

```bash
pytest apps/ai
```

---

# ⚙ Installation

Clone repository

```bash
git clone https://github.com/<username>/Bio-Toilet-Inspection-System.git
```

Create virtual environment

```bash
python -m venv .venv
```

Activate environment

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run migrations

```bash
python manage.py migrate
```

Run server

```bash
python manage.py runserver
```

---

# 📸 Screens

Flutter application includes

- Splash Screen
- Home
- Inspection
- Coach List
- Coach Details
- Inspection History
- Dashboard
- Reports
- Settings

---

# 🔒 Design Principles

- Clean Architecture
- Repository Pattern
- Service Layer
- Immutable AI Storage
- Domain-driven module separation
- Comprehensive unit testing

---

# 📄 License

This project was developed as an AI-powered railway inspection system for educational and research purposes.
