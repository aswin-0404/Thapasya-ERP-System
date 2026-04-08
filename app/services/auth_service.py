from app.repositories.user_repository import get_user_by_username
from app.core.security import verify_password,create_access_token
from app.models.role import Role

def login_user(db,data):
    user=get_user_by_username(db,data.username)

    role= db.query(Role).filter(Role.id==user.role_id).first()

    if not user:
        raise Exception("Invalid Username")
    
    if not verify_password(data.password,user.password):
        raise Exception("Invalid Password")
    
    token = create_access_token({
        "sub":user.username,
        "user_id":user.id,
        "role_id":user.role_id
    })

    return {
        "access_token":token,
        "token_type": "bearer",
        "role":role.name
    }