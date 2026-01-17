"""
Database initialization script for Render PostgreSQL
This script will create the necessary tables and structure for the quiz application
"""

import psycopg2
import os
from psycopg2.extras import RealDictCursor
from app.configAndAuth import get_password_hash
from datetime import datetime

def create_tables():
    """Create all necessary tables for the quiz application"""
    
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL environment variable not found")
        return False
    
    try:
        # Parse database URL
        import urllib.parse
        parsed = urllib.parse.urlparse(database_url)
        
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            database=parsed.path[1:],  # Remove leading slash
            user=parsed.username,
            password=parsed.password
        )
        
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        print("🔧 Creating database tables...")
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                user_email VARCHAR(255) UNIQUE NOT NULL,
                hashed_password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create quizzes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quizzes (
                quiz_id SERIAL PRIMARY KEY,
                quiz_title VARCHAR(200) NOT NULL,
                created_by VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users(user_email)
            );
        """)
        
        # Create questions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                question_id SERIAL PRIMARY KEY,
                quiz_id INTEGER NOT NULL,
                question_text TEXT NOT NULL,
                FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id) ON DELETE CASCADE
            );
        """)
        
        # Create answers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS answers (
                answer_id SERIAL PRIMARY KEY,
                question_id INTEGER NOT NULL,
                answer_text TEXT NOT NULL,
                is_correct BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE
            );
        """)
        
        # Create submissions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                submission_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                quiz_id INTEGER NOT NULL,
                score INTEGER DEFAULT 0,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id)
            );
        """)
        
        # Create user_answers table for storing user responses
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_answers (
                user_answer_id SERIAL PRIMARY KEY,
                submission_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                answer_id INTEGER NOT NULL,
                FOREIGN KEY (submission_id) REFERENCES submissions(submission_id) ON DELETE CASCADE,
                FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE,
                FOREIGN KEY (answer_id) REFERENCES answers(answer_id) ON DELETE CASCADE
            );
        """)
        
        # Create indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(user_email);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_quizzes_created_by ON quizzes(created_by);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_questions_quiz_id ON questions(quiz_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_answers_question_id ON answers(question_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_submissions_user_quiz ON submissions(user_id, quiz_id);")
        
        conn.commit()
        
        # Create a default admin user (use the same credentials as your local setup)
        admin_email = "jay65@gmail.com"
        admin_password = "J@ys19"  # Your existing password
        
        # Check if admin user already exists
        cursor.execute("SELECT * FROM users WHERE user_email = %s", (admin_email,))
        if cursor.fetchone() is None:
            hashed_password = get_password_hash(admin_password)
            cursor.execute(
                "INSERT INTO users (user_email, hashed_password, created_at) VALUES (%s, %s, %s)",
                (admin_email, hashed_password, datetime.now())
            )
            conn.commit()
            print(f"✅ Created admin user: {admin_email}")
        else:
            print("ℹ️ Admin user already exists")
        
        cursor.close()
        conn.close()
        
        print("✅ Database tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Initializing Render PostgreSQL Database...")
    success = create_tables()
    if success:
        print("🎉 Database initialization complete!")
    else:
        print("💥 Database initialization failed!")
