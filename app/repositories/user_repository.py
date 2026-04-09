from app.models.user import User

def create_user(db,username,email,password,role_id):
    user=User(
        username=username,
        email=email,
        password=password,
        role_id=role_id
    )
    db.add(user)
    return user

def get_user_by_username(db,username):
    return db.query(User).filter(User.username==username).first()