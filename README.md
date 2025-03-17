# RTL Hebrew Calculator API

This is a Flask backend for a Hebrew calculator chatbot application with PostgreSQL database integration. It provides API endpoints for user registration, calculation selection, question flow, and result generation.

## Features

- User registration and session management
- Multiple calculation types (Mortgage, Investment, Savings)
- Dynamic question flow based on calculation type
- Calculation logic for different financial scenarios
- Email delivery of calculation results
- Full RTL and Hebrew language support

## Project Structure

```
/
├── app.py                     # Main Flask application
├── models.py                  # Database models
├── init_db.py                 # Database initialization script
├── .env                       # Environment variables
├── requirements.txt           # Python dependencies
├── routes/
│   ├── user_routes.py         # User API endpoints
│   ├── calculation_routes.py  # Calculation type API endpoints
│   └── answer_routes.py       # User answers API endpoints
└── services/
    ├── calculation_service.py # Calculation logic
    └── email_service.py       # Email formatting and delivery
```

## Database Schema

- **users**: Store user information (name, email)
- **calculation_types**: Different types of calculations available
- **questions**: Questions for each calculation type
- **user_answers**: User responses to questions
- **calculation_results**: Results of calculations

## Setup and Installation

### Prerequisites

- Python 3.8+
- PostgreSQL database

### Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up PostgreSQL database
5. Copy `.env.example` to `.env` and update with your configuration
6. Initialize the database:
   ```
   flask shell
   >>> from app import app
   >>> from init_db import init_default_data
   >>> with app.app_context():
   ...     init_default_data()
   >>> exit()
   ```

### Running the Application

```
flask run --host=0.0.0.0 --port=5001
```

## API Endpoints

### User Management

- `