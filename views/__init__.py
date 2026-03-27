"""Views package for Rare Python API.

Contains modules for users, registration, posts, categories, and tags.
"""

from .user import create_user, login_user
from .register import handle_register
from .category import (
    get_categories,
    create_category,
    get_category,
    update_category,
    delete_category,
)
from .tags import get_tags, get_tag, create_tag, update_tag, delete_tag
from .posts import post_post, get_posts, get_single_post, get_user_posts
