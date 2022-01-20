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



# def making_posts_list(file):
#     with open(file , encoding='utf-8') as f:
#         templates = json.load(f)
#     posts = []


#     tag = "message"
  
#     for i in templates:
#         message = i.get(tag)
#         posts.append(message)
#     return  posts



# def making_links_list(file):
#     with open(file , encoding='utf-8') as f:
#         templates = json.load(f)
#     urls= []
#     tag = "entities"
#     for i in templates:
#         url_tag = i.get(tag)
#         urls.append(url_tag)

#     url_tag_name = "MessageEntityTextUrl"
#     test = urls
#     url_list = []
#     test = list(filter(None, test))
#     for i in test:
#         if i[0]['_'] == url_tag_name:
#             url_list.append(i[0]['url'])
#     true_url_list = []
#     start_link= url_list[0]
#     clear_link = start_link.replace('https://t.me/', '')
#     real_link = re.sub(r"\d", '', clear_link)
#     link = 'https://t.me/' + real_link
#     for i in url_list:
#         if link in i:
#             true_url_list.append(i)
#     return true_url_list
    
# print(making_posts_list("channel_messages.json"))
#print(making_links_list('channel_messages.json'))


