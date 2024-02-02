from flask import Flask
from .views import main_bp
from db.database import db_cursor
import psycopg2
import logging
app = Flask(__name__)
app.register_blueprint(main_bp)


def create_accounts_table():
    queries = [
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            firstname VARCHAR(255) NOT NULL,
            lastname VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS password_reset_tokens (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL,
            token VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS user_tasks (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL,
            title VARCHAR(255) NOT NULL,
            body VARCHAR(255) NOT NULL,
            due_date DATE NOT NULL,
            completed BOOLEAN DEFAULT FALSE
        )
        """
    ]
    try:
        with db_cursor(True) as cursor:
            for query in queries:
                cursor.execute(query)
            print(f"Table created successfully")
    except (Exception, psycopg2.DatabaseError) as e:
        print(f"Error creating table: {e}")


def create_tables():
    create_accounts_table()


def initialize_logging():
    logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


with app.app_context():
    initialize_logging()
    create_tables()

if __name__ == "__main__":
    app.run(debug=True)
