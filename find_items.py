import parsingPage

def find_item(list,item):
    bad_links = []
    num = 0
    for i in list:
            if item in i:
                bad_links.append(list[num+1])
                num += 1
            else:
                num += 1
    return bad_links

