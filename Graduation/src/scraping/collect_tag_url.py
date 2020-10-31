import requests
from bs4 import BeautifulSoup
import time
import re
import os

URL = "https://4travel.jp/dm_travelogue_tag_category.html"
base_url = "https://4travel.jp"

r = requests.get(URL)
soup = BeautifulSoup(r.content, "html.parser")
list_tag = soup.select("div.travelTagList_tagBox")

for i, tag in enumerate(list_tag):
    if i == 0:
        continue
    tag_wrap = tag.select("li")
    for a in tag_wrap:
        tag_name = re.sub(r"[ #\n]", "", a.text)
        tag_url = base_url + a.find("a").get("href")
        
        with open("tag_url.csv", mode="a") as f:
            f.write(tag_name+","+tag_url+"\n")

