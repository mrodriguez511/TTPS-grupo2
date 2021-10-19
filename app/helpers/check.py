from app.models.user import User


def check_permission(user_id, permission):
    return User.has_permission(user_id, permission)
