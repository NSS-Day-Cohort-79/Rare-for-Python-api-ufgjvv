from models.tag import create_tag
import json


def handle_tags_request(method, body):
    if method == "POST":
        new_tag = json.loads(body)
        return create_tag(new_tag)
