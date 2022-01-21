import json
import re

def making_list(file,channel_link):
    with open(file , encoding='utf-8') as f:
        templates = json.load(f)
    posts = []


    tag = "message"
    tag_id = 'id'
    for i in templates:
        message = i.get(tag)
        url = f'{channel_link}/{i.get(tag_id)}'
        posts.append(message)
        posts.append(url)
    posts = list(filter(None, posts))
    return  posts


