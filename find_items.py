import parsingPage

def find_item(list,item):
    bad_links = []
    num = 0
    for i in list:
        try:
            if item in i:
                bad_links.append(list[num+1])
                num += 1
            else:
                num += 1
        except:
            pass
    return bad_links

# print(find_item(parsingPage.making_list("channel_messages.json",'https://t.me/bazabazon'),'гики'))