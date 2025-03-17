#!/usr/bin/env python3
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import time
import sys

# Database connection parameters - Using the same parameters from your db_module
DB_CONFIG = {
    'dbname': 'modax_calculator',
    'user': 'postgres',
    'password': '12345',  # Using the password from your document
    'host': 'localhost',
    'port': '5432'
}

def connect_to_postgres():
    """Connect to PostgreSQL server (not the specific database)"""
    conn_params = DB_CONFIG.copy()
    conn_params.pop('dbname')  # Remove dbname to connect to postgres default
    
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            **conn_params
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def database_exists():
    """Check if the database exists"""
    conn = connect_to_postgres()
    if not conn:
        return False
    
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_CONFIG['dbname'],))
    exists = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return exists is not None

def create_database():
    """Create the database if it doesn't exist"""
    if database_exists():
        print(f"Database '{DB_CONFIG['dbname']}' already exists.")
        return True
    
    conn = connect_to_postgres()
    if not conn:
        return False
    
    cursor = conn.cursor()
    try:
        print(f"Creating database '{DB_CONFIG['dbname']}'...")
        cursor.execute(f"CREATE DATABASE {DB_CONFIG['dbname']}")
        print(f"Database '{DB_CONFIG['dbname']}' created successfully!")
        cursor.close()
        conn.close()
        return True
    except psycopg2.Error as e:
        print(f"Error creating database: {e}")
        cursor.close()
        conn.close()
        return False

def connect_to_db():
    """Connect to the application database"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error connecting to database: {e}")
        return None

def create_tables():
    """Create tables in the database"""
    conn = connect_to_db()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    # Create tables
    try:
        print("Creating tables...")
        
        # Create calculation_type table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS calculation_type (
            calculation_type_id SERIAL PRIMARY KEY,
            calculation_type VARCHAR(255) NOT NULL,
            total_questions_number INTEGER NOT NULL
        )
        """)
        
        # Create questions table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id SERIAL PRIMARY KEY,
            calculation_type_id INTEGER NOT NULL,
            question VARCHAR(255) NOT NULL,
            question_type VARCHAR(50) NOT NULL,
            FOREIGN KEY (calculation_type_id) REFERENCES calculation_type(calculation_type_id)
        )
        """)
        
        # Create answers table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS answers (
            id SERIAL PRIMARY KEY,
            text VARCHAR(255) NOT NULL,
            question_id INTEGER NOT NULL,
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
        """)
        
        # Create users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            username VARCHAR(100) NOT NULL
        )
        """)
        
        # Create user_answer table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_answer (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            answer VARCHAR(255) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_questions_calculation_type ON questions(calculation_type_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_answers_question ON answers(question_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_answer_user ON user_answer(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_answer_question ON user_answer(question_id)")
        
        conn.commit()
        print("Tables created successfully!")
        return conn, cursor
    except psycopg2.Error as e:
        print(f"Error creating tables: {e}")
        conn.rollback()
        cursor.close()
        conn.close()
        return False

def insert_initial_data(conn, cursor):
    """Insert initial data into tables"""
    try:
        # Clear existing data (optional)
        print("Clearing existing data...")
        cursor.execute("TRUNCATE TABLE user_answer CASCADE")
        cursor.execute("TRUNCATE TABLE answers CASCADE")
        cursor.execute("TRUNCATE TABLE questions CASCADE")
        cursor.execute("TRUNCATE TABLE calculation_type CASCADE")
        conn.commit()
        
        # Insert calculation types
        calculation_types = [
            ('Basic Calculator', 3),
            ('Interest Calculator', 3),
            ('User Engagement', 4),
            ('Conversation Metrics', 4)
        ]
        
        print("Inserting calculation types...")
        for calc_type, total_questions in calculation_types:
            cursor.execute(
                "INSERT INTO calculation_type (calculation_type, total_questions_number) VALUES (%s, %s) RETURNING calculation_type_id",
                (calc_type, total_questions)
            )
            # Get the ID of the inserted calculation type
            calc_type_id = cursor.fetchone()[0]
            
            # Insert questions for this calculation type
            if calc_type == 'Basic Calculator':
                questions = [
                    ('Enter the first value:', 'number'),
                    ('Enter the second value:', 'number'),
                    ('Choose an operation:', 'select')
                ]
                
                for question, question_type in questions:
                    cursor.execute(
                        "INSERT INTO questions (calculation_type_id, question, question_type) VALUES (%s, %s, %s) RETURNING id",
                        (calc_type_id, question, question_type)
                    )
                    question_id = cursor.fetchone()[0]
                    
                    # If it's the operation question, add possible answers
                    if 'operation' in question.lower():
                        operations = ['add', 'subtract', 'multiply', 'divide']
                        for op in operations:
                            cursor.execute(
                                "INSERT INTO answers (question_id, text) VALUES (%s, %s)",
                                (question_id, op)
                            )
            
            elif calc_type == 'Interest Calculator':
                questions = [
                    ('Enter the principal amount:', 'number'),
                    ('Enter the interest rate (%):', 'number'),
                    ('Enter time period (years):', 'number')
                ]
                
                for question, question_type in questions:
                    cursor.execute(
                        "INSERT INTO questions (calculation_type_id, question, question_type) VALUES (%s, %s, %s)",
                        (calc_type_id, question, question_type)
                    )
            
            elif calc_type == 'User Engagement':
                questions = [
                    ('Total number of registered users:', 'number'),
                    ('Daily active users:', 'number'),
                    ('Average session time (minutes):', 'number'),
                    ('Average messages per user per day:', 'number')
                ]
                
                for question, question_type in questions:
                    cursor.execute(
                        "INSERT INTO questions (calculation_type_id, question, question_type) VALUES (%s, %s, %s)",
                        (calc_type_id, question, question_type)
                    )
            
            elif calc_type == 'Conversation Metrics':
                questions = [
                    ('Total number of conversations:', 'number'),
                    ('Average conversation length (messages):', 'number'),
                    ('Average response time (seconds):', 'number'),
                    ('Conversation completion rate (%):', 'number')
                ]
                
                for question, question_type in questions:
                    cursor.execute(
                        "INSERT INTO questions (calculation_type_id, question, question_type) VALUES (%s, %s, %s)",
                        (calc_type_id, question, question_type)
                    )
        
        conn.commit()
        print("Initial data inserted successfully!")
        return True
    except psycopg2.Error as e:
        print(f"Error inserting initial data: {e}")
        conn.rollback()
        return False

def test_connection():
    """Test the connection to the database and verify tables exist"""
    from db_module import get_all_calculation_types
    
    try:
        calc_types = get_all_calculation_types()
        print("\nTesting connection and database setup...")
        if calc_types and len(calc_types) > 0:
            print(f"Success! Found {len(calc_types)} calculation types:")
            for ct in calc_types:
                print(f"  - {ct['calculation_type']}")
        else:
            print("Connected to database, but no calculation types found.")
        return True
    except Exception as e:
        print(f"Error testing connection: {e}")
        return False

def main():
    print("Starting database initialization...")
    
    # Create database if it doesn't exist
    if not create_database():
        print("Failed to create database. Exiting.")
        sys.exit(1)
    
    # Create tables
    result = create_tables()
    if not result:
        print("Failed to create tables. Exiting.")
        sys.exit(1)
    
    conn, cursor = result
    
    # Insert initial data
    if not insert_initial_data(conn, cursor):
        print("Failed to insert initial data. Exiting.")
        cursor.close()
        conn.close()
        sys.exit(1)
    
    # Close connection
    cursor.close()
    conn.close()
    
    # Test connection with the db_module
    try:
        import db_module
        test_connection()
    except ImportError:
        print("\nNote: Could not import db_module to test connection.")
        print("Database setup appears successful, but connection not verified.")
    
    print("\nDatabase initialization completed successfully!")
    print(f"Database '{DB_CONFIG['dbname']}' is ready to use with your application.")
    print(f"Connection parameters: {DB_CONFIG}")

if __name__ == "__main__":
    main()