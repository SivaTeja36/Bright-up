from sqlalchemy.orm import Session

from app.utils.db_queries import get_users


def get_all_users_dict(db: Session) -> dict:
    """
    Get all users from the database and return them as a dictionary.
    """
    users = get_users(db)
    return {user.id: user for user in users}