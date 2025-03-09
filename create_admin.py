from app import app, db
from models import StudentLeader
from werkzeug.security import generate_password_hash

def create_student_leader(username, email, password):
    with app.app_context():
        # Check if user already exists
        existing_user = StudentLeader.query.filter_by(email=email).first()
        if existing_user:
            print(f"User with email {email} already exists")
            return

        # Create new student leader
        leader = StudentLeader(
            username=username,
            email=email
        )
        leader.set_password(password)
        
        # Add to database
        db.session.add(leader)
        db.session.commit()
        print(f"Created student leader account for {username}")

if __name__ == "__main__":
    username = "admin"
    email = "admin@example.com"
    password = "admin123"  # You should change this password
    create_student_leader(username, email, password)
