from app import app
from models import db, User
from werkzeug.security import generate_password_hash

students = [
    ("12211", "12211"),
    ("22211", "22211"),
    ("30333", "30333"),
    ("44044", "44044"),
    ("55255", "55255"),
    ("67667", "67667"),
]

with app.app_context():
    for sid, password in students:
        user = User(
            sid=sid,
            password=generate_password_hash(password),
            role="student"
        )
        db.session.add(user)

    db.session.commit()

print("Students created successfully")