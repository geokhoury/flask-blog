
# models package

print(f'Invoking __init__.py for {__name__}')

from .user import User
from .post  import Post, TextPost, LinkPost
from .comment import Comment