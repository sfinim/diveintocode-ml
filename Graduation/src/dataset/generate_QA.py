from glob import glob
import MeCab
import random
from generate_vocabulary import dict_id_word, dict_spot
from pyknp import Juman

base_directory = "../../data/"
list_todofuken = ["香川", "新潟", "栃木", "愛媛", "青森",
                  "富山", "高知", "岩手", "石川", "群馬",
                  "大阪", "福井", "福岡", "佐賀", "秋田",
                  "山形", "岐阜", "埼玉", "長崎", "福島",
                  "熊本", "北海道", "茨城", "大分", "兵庫",
                  "宮城", "千葉", "鹿児島", "静岡", "奈良",
                  "和歌山", "鳥取", "島根", "愛知", "岡山",
                  "三重", "広島", "滋賀", "沖縄", "山口",
                  "徳島", "東京", "山梨", "長野", "神奈川",
                  "京都", "宮崎"]
seed_Q = [ 
          "の観光でおすすめはありますか？",
          "の旅行でオススメはありますか？",
          "でおススメの観光地はありますか？",
          "　おすすめ",
          "　観光",
          "　旅行",
          "　観光　おススメ",
          "　旅行　おすすめ",
          ]   
seed_Q_todofuken = [
                    "で観光したい。",
                    "の観光でおすすめはありますか？",
                    "　おすすめ",
                    "　観光"
                    ]
seed_Q_other = [
                "でおすすめの観光はありますか？",
                "　おすすめ",
                "　観光"
                ]
seed_A = [
          "がおすすめです。"
         ]
seed_A_spot_start = [
                     "おすすめスポットに"
                     ]
seed_A_spot_end = [
                    "があります。"
                  ]

def read_files():
    """
    ファイル一覧の読み込み
    """
    files = glob(base_directory+'*.csv')
    return files

def read_csv(csv_path):
    """
    csvの１行分を読み込み
    """
    with open(csv_path, mode="r") as f:
        csv = f.read()

    list_row = csv.split("\n")

    return list_row

def generate_QA_id(spot_exist, search_tag, user_tag, spot_names, seed_Q):
    """
    Q&AをID変換した文字列(カンマ区切り)を生成する
    構成：Question <SEP> Answer <SEP> Label
    """
    # 形態素解析器(Mecab-neologd)
    tokenizer = MeCab.Tagger('-Owakati -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')

    # 単語ID変換辞書読み込み
    dict_id2word, dict_word2id = dict_id_word("./")

    QA_text_id = ""
    tmp_list_word = tokenizer.parse(search_tag).split(" ")[:-1]
    QA_text_id += ",".join(map(str, [dict_word2id[word] for word in tmp_list_word])) + ","
    tmp_list_word = tokenizer.parse(random.choice(seed_Q)).split(" ")[:-1]
    QA_text_id += ",".join(map(str, [dict_word2id[word] for word in tmp_list_word])) + ","
    QA_text_id += str(dict_word2id["<SEP>"])+"," # <SEP>
    tmp_list_word = tokenizer.parse(user_tag).split(" ")[:-1]
    QA_text_id += ",".join(map(str, [dict_word2id[word] for word in tmp_list_word])) + ","
    tmp_list_word = tokenizer.parse(random.choice(seed_A)).split(" ")[:-1]
    QA_text_id += ",".join(map(str, [dict_word2id[word] for word in tmp_list_word]))
    if spot_exist:
        QA_text_id += ","
        tmp_list_word = tokenizer.parse(random.choice(seed_A_spot_start)).split(" ")[:-1]
        QA_text_id += ",".join(map(str, [dict_word2id[word] for word in tmp_list_word])) + ","
        for i, spot_id in enumerate([dict_word2id[word] for word in spot_names.split("\\")]):
            QA_text_id += str(spot_id) + ","
            if i+1 != len(spot_names.split("\\")):
                QA_text_id += str(dict_word2id["、"]) + ","
        tmp_list_word = tokenizer.parse(random.choice(seed_A_spot_end)).split(" ")[:-1]
        QA_text_id += ",".join(map(str, [dict_word2id[word] for word in tmp_list_word]))

    # ラベルとなる単語IDを付与
    QA_text_id += ","+str(dict_word2id["<SEP>"])+"," # <SEP>
    tmp_list_word = tokenizer.parse(user_tag).split(" ")[:-1]
    QA_text_id += ",".join(map(str, [dict_word2id[word] for word in tmp_list_word]))
    # ラベルとなる全スポットIDを付与
    if spot_exist:
        QA_text_id += ","+str(dict_word2id["<SEP>"])+"," # <SEP>
        for i, spot_id in enumerate([dict_word2id[word] for word in spot_names.split("\\")]):
            QA_text_id += str(spot_id)
            if i+1 != len(spot_names.split("\\")):
                QA_text_id += ","

    return QA_text_id

def generate_QA_original(row):
    """
    csvの１行からQ&A(ID変換)とラベルの組を作成する
    全てのユーザータグ・スポットの情報で作成する
    """
    try:
        travel_id, \
        search_tag, \
        date_start, date_end, \
        user_tags, spot_names, spot_urls = row.split(",")
    except ValueError:
        return

    spot_exist = True
    if spot_names == "" and spot_urls == "":
        spot_exist = False
    
    # user_tagを回答に含める文章を作成
    for user_tag in user_tags.split("\\"):
        if user_tag == search_tag or \
           user_tag == "その他":
            continue

        if search_tag in list_todofuken:
            QA_text_id = generate_QA_id(spot_exist, search_tag, user_tag, spot_names, seed_Q_todofuken)
        else:
            QA_text_id = generate_QA_id(spot_exist, search_tag, user_tag, spot_names, seed_Q_other)

        # 書き込みモード
        with open("QA_label.csv", mode="a") as f:
            f.write(QA_text_id+"\n")

        # Debug用
        #dict_id2word, dict_word2id = dict_id_word("dataset/")
        #print([dict_id2word[id_] for id_ in list(map(int, QA_text_id.split(",")))])
        #print(len(QA_text_id.split(",")))

def generate_QA_spot(row):
    """
    csvの１行からQ&A(ID変換)とラベルの組を作成する
    上位件数で絞ったスポットのみで作成する
    """
    tokenizer = Juman()

    with open("spot.tsv", mode="r") as f:
        tsv = f.read()

    tsv_spots = tsv.split("\n")[:-1]
    tsv_spots_name = [spots.split("\t")[0] for spots in tsv_spots]

    # 単語ID変換辞書読み込み
    dict_id2word, dict_word2id = dict_id_word("./")

    try:
        travel_id, \
        search_tag, \
        date_start, date_end, \
        user_tags, spot_names, spot_urls = row.split(",")
    except ValueError:
        return

    if spot_names == "" and spot_urls == "":
        return

    for spot_name in spot_names.split("\\"):
        if spot_name in tsv_spots_name:
            QA_text_id = ""
            result = tokenizer.analysis(search_tag)
            tmp_list_word = [mrph.midasi for mrph in result.mrph_list()]
            QA_text_id += ",".join(map(str, [dict_word2id[word] for word in tmp_list_word])) + ","
            if search_tag in list_todofuken:
                result = tokenizer.analysis(random.choice(seed_Q_todofuken))
            else:
                result = tokenizer.analysis(random.choice(seed_Q_other))
            tmp_list_word = [mrph.midasi for mrph in result.mrph_list()]
            QA_text_id += ",".join(map(str, [dict_word2id[word] for word in tmp_list_word])) + ","
            QA_text_id += str(dict_word2id["<SEP>"])+"," # <SEP>
            result = tokenizer.analysis(random.choice(seed_A_spot_start))
            tmp_list_word = [mrph.midasi for mrph in result.mrph_list()]
            QA_text_id += ",".join(map(str, [dict_word2id[word] for word in tmp_list_word])) + ","
            QA_text_id += str(dict_word2id[spot_name]) + ","
            result = tokenizer.analysis(random.choice(seed_A_spot_end))
            tmp_list_word = [mrph.midasi for mrph in result.mrph_list()]
            QA_text_id += ",".join(map(str, [dict_word2id[word] for word in tmp_list_word]))
            # ラベルとなるスポットIDを付与
            QA_text_id += ","+str(dict_word2id["<SEP>"])+"," # <SEP>
            QA_text_id += str(dict_word2id[spot_name])

            with open("QA_label.csv", mode="a") as f:
                f.write(QA_text_id+"\n")

def generate_id_label(row):
    """
    csvの１行から検索単語(ID変換)とラベルの組を作成する
    上位件数で絞ったスポットのみで作成する
    """
    with open("spot.tsv", mode="r") as f:
        tsv = f.read()

    tsv_spots = tsv.split("\n")[:-1]
    tsv_spots_name = [spots.split("\t")[0] for spots in tsv_spots]

    # 単語ID変換辞書読み込み
    dict_id2word, dict_word2id = dict_id_word("./")
    dict_spot2url, dict_id2spot, dict_spot2id = dict_spot("./")
    vocabulary = [word for word in list(dict_word2id.keys())]
    spots = [spot for spot in list(dict_spot2id.keys())]

    try:
        travel_id, \
        search_tag, \
        date_start, date_end, \
        user_tags, spot_names, spot_urls = row.split(",")
    except ValueError:
        return

    if spot_names == "" and spot_urls == "":
        return

    text = str(dict_word2id[search_tag]) + ","
    for user_tag in user_tags.split("\\"):
        if user_tag == search_tag or \
           user_tag == "その他":
            continue
        if user_tag not in vocabulary:
            continue
        text += str(dict_word2id[user_tag]) + ","

    # 区切り
    text += "_,"

    for spot_name in spot_names.split("\\"):
        if spot_name in tsv_spots_name and \
           spot_name in spots:
            text += str(dict_spot2id[spot_name]) + ","
    # spotが何も書き込まれなかった場合
    if text[-2] == "_":
        return

    with open("id_label.csv", mode="a") as f:
        f.write(text[:-1]+"\n")

def generate_Q_spot(row):
    """
    csvの１行からQuestion(ID変換)とラベルの組を作成する
    上位件数で絞ったスポットのみで作成する
    """
    tokenizer = Juman()

    with open("spot.tsv", mode="r") as f:
        tsv = f.read()

    tsv_spots = tsv.split("\n")[:-1]
    tsv_spots_name = [spots.split("\t")[0] for spots in tsv_spots]

    # 単語ID変換辞書読み込み
    dict_id2word, dict_word2id = dict_id_word("./")

    try:
        travel_id, \
        search_tag, \
        date_start, date_end, \
        user_tags, spot_names, spot_urls = row.split(",")
    except ValueError:
        return

    if spot_names == "" and spot_urls == "":
        return

    for spot_name in spot_names.split("\\"):
        if spot_name in tsv_spots_name:
            text_id = ""
            text_id += str(dict_word2id[search_tag]) + ","
            result = tokenizer.analysis(random.choice(seed_Q))
            tmp_list_word = [mrph.midasi for mrph in result.mrph_list()]
            text_id += ",".join(map(str, [dict_word2id[word] for word in tmp_list_word])) + ","
            text_id += str(dict_word2id["<SEP>"])+"," # <SEP>
            text_id += str(dict_word2id[spot_name])

            with open("QA_label.csv", mode="a") as f:
                f.write(text_id+"\n")

if __name__ == "__main__":
    files = read_files()

    for csv_path in files:
        list_row = read_csv(csv_path)

        for row in list_row:
            if row == "":
                continue
#            generate_QA_original(row)
#            generate_QA_spot(row)
#            generate_id_label(row)
            generate_Q_spot(row)

