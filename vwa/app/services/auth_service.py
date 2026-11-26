from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models.user import User


def register_user(username, email, password):
    username = username.strip()
    email = email.strip().lower()

    if not username or not email or not password:
        return None, "All fields are required."

    if len(username) > 50:
        return None, "Username is too long."

    if len(email) > 120:
        return None, "Email is too long."

    if len(password) < 12:
        return None, "Password must be at least 12 characters."

    existing_user = User.query.filter(
        (User.username == username) |
        (User.email == email)
    ).first()

    if existing_user:
        return None, "Username or email already exists."

    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        role="user"
    )

    db.session.add(user)
    db.session.commit()

    return user, None


def authenticate_user(username, password):
    username = username.strip()

    user = User.query.filter_by(username=username).first()

    if user is None:
        return None

    if not check_password_hash(user.password_hash, password):
        return None

    return user
