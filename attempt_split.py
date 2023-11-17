import re
def cut_article(para):
    para = re.sub('[。！？【】“”‘’]', r"\1\n\2", para)
    para = re.sub()
