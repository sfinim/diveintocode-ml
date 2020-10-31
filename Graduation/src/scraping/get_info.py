import requests
from bs4 import BeautifulSoup
import time
import re
import mojimoji


def get_travel_url(base_url, is_todofuken=False):
    url_4travel = "https://4travel.jp"
    url = base_url
    list_travel_url = []
    
    while (True):
        time.sleep(1)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        travelList = soup.select("li.travelList_cardBlock")
        
        for travel in travelList:
            # 最初のaタグ
            a = travel.find("a")
     
            # ページのどこかでNoneになることがある
            if a is None:
                continue
     
            travel_url = a.get("href")
            if is_todofuken:
                list_travel_url.append(travel_url)
            else:
                list_travel_url.append(url_4travel + travel_url)
        
        # 次のページを処理する
        next_page = soup.select("li.u_pagination_list_item")
        
        # 1ページしか無い場合
        if len(next_page) == 0:
            break
        
        next_page_url = next_page[-1].find("a").get("href")
        # 最後のページ
        if next_page[-1].find("a").text != "":
            break
        
        url = url_4travel + next_page_url
        
    return list_travel_url

def get_travel_info(travel_url, search_tag):
    """
    csv保存まで実施する
    """
    time.sleep(1)
    r = requests.get(travel_url)
    soup = BeautifulSoup(r.content, "html.parser")

    # travel_id
    travel_id = re.search(r"/1[\d]+", travel_url).group()[1:]

    # date_start, date_end
    duration = re.sub(r"[\n ]", "", soup.select("p.day")[0].text)
    date_start, date_end = duration.split("-")

    # user_tag
    user_tag = ""
    tmp_list_user_tag = soup.select("ul.u_tagListWrap")[0]  # ページ内にul.u_tagListWrapがいくつかある
    tmp_list_user_tag = tmp_list_user_tag.find_all("a")
    for tag in tmp_list_user_tag:
        user_tag += re.sub(r"[\n# ]", "", tag.text) + "\\"
    user_tag = user_tag[:-1]
    # 全角文字を半角に変換(かな文字は除く)
    user_tag = mojimoji.zen_to_han(user_tag, kana=False)
    # 大文字を小文字に変換
    user_tag = user_tag.lower()

    # spot_names, spot_urls
    spot_names = ""
    spot_urls = ""
    tmp_list = []
    tmp_list_spotItem = soup.select("a.travelogue_spotItem")
    for spotItem in tmp_list_spotItem:
        tmp_name = re.sub(r"(<p class=\"spotTitle\">)|(<span[\s\S]*</p>)|([\n][ ]{6})", "", str(spotItem.p))
        if tmp_name not in tmp_list:
            tmp_list.append(tmp_name)
            spot_names += tmp_name + "\\"
            spot_urls += re.sub(r"\?[ -~]+", "", spotItem.get("href")) + "\\"
    spot_urls = spot_urls[:-1]
    spot_names = spot_names[:-1]

    # csvに書き込み
    row = travel_id + "," + \
          search_tag + "," + \
          date_start + "," + \
          date_end + "," + \
          user_tag + "," + \
          spot_names + "," + \
          spot_urls + "\n"
    filename = "../data/" + search_tag + ".csv"
    with open(filename, mode="a") as f:
        f.write(row)

