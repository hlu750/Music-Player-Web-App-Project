from music.adapters.repository import AbstractRepository
from music.domainmodel.user import User

def get_user(user_name: str, repo: AbstractRepository):
    
    user = repo.get_user(user_name)
    return user