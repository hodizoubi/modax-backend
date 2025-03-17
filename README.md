# RTL Hebrew Calculator API

This is a Flask backend for a Hebrew calculator chatbot application with PostgreSQL database integration. It provides API endpoints for user registration, calculation selection, question flow, and result generation.

## Features

- User registration and session management
- Multiple calculation types (Mortgage, Investment, Savings)
- Dynamic question flow based on calculation type
- Calculation logic for different financial scenarios
- Email delivery of calculation results
- Full RTL and Hebrew language support

<!-- ## Project Structure

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
``` -->

## Database Schema

Table calcuation_type {
  Calcuation_type_id integer [primary key]
  Calcuation_type varchar
  total_questions_number integer
}

Table questions {
  id integer [primary key]
  Calcuation_type_id int
  question varchar
  question_type varchar
}

Table answers {
  id integer [primary key]
  text varchar
  question_id varchar 
}
Table users{
  id integer [primary key, increment]
  email varchar 
  username varchar
}

Table user_answer{
  id integer [primary key , increment]
  user_id integer
  question_id varchar
  answer varchar

}

Ref questions: questions.Calcuation_type_id > calcuation_type.Calcuation_type_id
Ref answers: answers.question_id > questions.id

Ref userAns: user_answer.user_id > users.id
Ref userAnsQuestion: user_answer.question_id > questions.id

// Ref: users.id < follows.following_user_id

// Ref: users.id < follows.followed_user_id

## Setup and Installation

### Prerequisites

- Python 3.8+
- docker

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
```bash
chmod 777 run.sh
./run.sh
```

now you ahve a data base server and you can access it using the output creds

5. create the database and insert the dummy daya

```bash
python3 init_db.py
```

now start emplementing the flask code please :3

## happy coding OwIse
