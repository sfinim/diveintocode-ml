from glob import glob
import MeCab
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

def vocabulary_write_Mecab(sentence, tokenizer, filename="vocab.txt"):
    # 読み込みモード
    with open("vocab.txt", mode="r") as f:
        vocab_txt = f.read()
    vocabulary = vocab_txt.split("\n")[:-1]
    # 書き込みモード
    with open("vocab.txt", mode="a") as f:
        list_token = tokenizer.parse(sentence).split(" ")
        for token in list_token:
            if token not in vocabulary and \
                token != "\n":
                f.write(token+"\n")

def vocabulary_write_Juman(sentence, tokenizer, filename="vocab.txt"):
    # 読み込みモード
    with open("vocab.txt", mode="r") as f:
        vocab_txt = f.read()
    vocabulary = vocab_txt.split("\n")[:-1]
    # 書き込みモード
    with open("vocab.txt", mode="a") as f:
        result = tokenizer.analysis(sentence)
        list_token = [mrph.midasi for mrph in result.mrph_list()]
        for token in list_token:
            if token not in vocabulary:
                f.write(token+"\n")

def generate_vocabulary_original(row):
    """
    csvの１行からボキャブラリを作成する
    """
    try:
        travel_id, \
        search_tag, \
        date_start, date_end, \
        user_tags, spot_names, spot_urls = row.split(",")
    except ValueError:  # 固有名詞にカンマが含まれていることがある。今回は無視。
        return

    spot_exist = True
    if spot_names == "" and spot_urls == "":
        spot_exist = False
    
    # 形態素解析器(Mecab-neologd)
    tokenizer = MeCab.Tagger('-Owakati -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')

    # 分割,未知語,パディングトークン
    # 読み込みモード
    with open("vocab.txt", mode="r") as f:
        vocab_txt = f.read()
    vocabulary = vocab_txt.split("\n")[:-1]
    # 書き込みモード
    with open("vocab.txt", mode="a") as f:
        if "<PAD>" not in vocabulary:
            f.write("<PAD>"+"\n")
        if "<UNK>" not in vocabulary:
            f.write("<UNK>"+"\n")
        if "<SEP>" not in vocabulary:
            f.write("<SEP>"+"\n")

    # 都道府県
    # 読み込みモード
    with open("vocab.txt", mode="r") as f:
        vocab_txt = f.read()
    vocabulary = vocab_txt.split("\n")[:-1]
    # 書き込みモード
    with open("vocab.txt", mode="a") as f:
        for todofuken in list_todofuken:
            if todofuken not in vocabulary:
                f.write(todofuken+"\n")

    # 文章シード
    # seed_Q_todofuken
    for seed in seed_Q_todofuken:
        vocabulary_write_Mecab(seed, tokenizer)
    # seed_Q_other
    for seed in seed_Q_other:
        vocabulary_write_Mecab(seed, tokenizer)
    # seed_A
    for seed in seed_A:
        vocabulary_write_Mecab(seed, tokenizer)
    # seed_A_spot_start
    for seed in seed_A_spot_start:
        vocabulary_write_Mecab(seed, tokenizer)
    # seed_A_spot_end
    for seed in seed_A_spot_end:
        vocabulary_write_Mecab(seed, tokenizer)
 
    # search_tagをvocab.txtに追加(解析器有) 
    vocabulary_write_Mecab(search_tag, tokenizer)

    # user_tagをvocab.txtに追加(解析器有) 
    for user_tag in user_tags.split("\\"):
        vocabulary_write_Mecab(user_tag, tokenizer)

    if spot_exist:
        # spot_nameをvocab.txtに追加(解析器無)
        spot_names = spot_names.split("\\")
        spot_urls = spot_urls.split("\\")
        for (spot_name, spot_url) in zip(spot_names, spot_urls):
            # 読み込みモード
            with open("vocab.txt", mode="r") as f:
                vocab_txt = f.read()
            vocabulary = vocab_txt.split("\n")[:-1]
            # 書き込みモード
            with open("vocab.txt", mode="a") as f:
                if spot_name not in vocabulary and \
                    spot_name != "\n":
                    f.write(spot_name+"\n")
 
            # spot.csvの作成
            # 読み込みモード
            with open("spot.csv", mode="r") as f:
                spot_csv = f.read()
            list_spot = spot_csv.split("\n")[:-1]
            # 書き込みモード
            with open("spot.csv", mode="a") as f:
                spot_info = spot_name+","+spot_url
                if spot_info not in list_spot:
                    f.write(spot_info+"\n")

def dict_id_word(path="dataset/"):
    """
    単語_IDの変換用辞書を返す
    """
    with open(path+"vocab.txt", mode="r") as f:
        vocab_txt = f.read()
    vocabulary = vocab_txt.split("\n")[:-1]
    vocabulary = list(dict.fromkeys(vocabulary))

    dict_id2word = {}
    dict_word2id = {}
    for i, word in enumerate(vocabulary):
        dict_id2word[i+1] = word
        dict_word2id[word] = i+1

    return dict_id2word, dict_word2id

def dict_spot(path="dataset/"):
    """
    スポット_URLと、スポット_IDの変換用辞書を返す
    """
    with open(path+"spot.tsv", mode="r") as f:
        tsv = f.read()
    dict_spot2url = {}
    dict_id2spot = {}
    dict_spot2id = {}
    list_row = tsv.split("\n")
    for i, row in enumerate(list_row):
        if row == "": 
            continue
        spot = row.split("\t")[0]
        url = row.split("\t")[1]
        dict_spot2url[spot] = url 
        dict_id2spot[i+1] = spot
        dict_spot2id[spot] = i+1

    # Padding用
    dict_id2spot[len(dict_id2spot)+1] = "<PAD>"
    dict_spot2id["<PAD>"] = len(dict_id2spot)+1

    return dict_spot2url, dict_id2spot, dict_spot2id

def vocabulary_count(files, cnt_vocab, cnt_spot):
    """
    スポットの件数上位cnt番目までの要素をボキャブラリとして書き込む
    """
    # 形態素解析器
    #tokenizer = MeCab.Tagger('-Owakati -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
    tokenizer = Juman()

    # 分割,未知語,パディングトークン
    # 読み込みモード
    with open("vocab.txt", mode="r") as f:
        vocab_txt = f.read()
    vocabulary = vocab_txt.split("\n")[:-1]
    # 書き込みモード
    with open("vocab.txt", mode="a") as f:
        if "<PAD>" not in vocabulary:
            f.write("<PAD>"+"\n")
        if "<UNK>" not in vocabulary:
            f.write("<UNK>"+"\n")
        if "<SEP>" not in vocabulary:
            f.write("<SEP>"+"\n")

    # 都道府県
    # 読み込みモード
    with open("vocab.txt", mode="r") as f:
        vocab_txt = f.read()
    vocabulary = vocab_txt.split("\n")[:-1]
    # 書き込みモード
    with open("vocab.txt", mode="a") as f:
        for todofuken in list_todofuken:
            if todofuken not in vocabulary:
                f.write(todofuken+"\n")

#    # 文章シード
    # seed_Q
    for seed in seed_Q:
        vocabulary_write_Juman(seed, tokenizer)
#    # seed_Q_todofuken
#    for seed in seed_Q_todofuken:
#        vocabulary_write_Juman(seed, tokenizer)
#    # seed_Q_other
#    for seed in seed_Q_other:
#        vocabulary_write_Juman(seed, tokenizer)
#    # seed_A
#    for seed in seed_A:
#        vocabulary_write_Juman(seed, tokenizer)
#    # seed_A_spot_start
#    for seed in seed_A_spot_start:
#        vocabulary_write_Juman(seed, tokenizer)
#    # seed_A_spot_end
#    for seed in seed_A_spot_end:
#        vocabulary_write_Juman(seed, tokenizer)
 
    dict_count_spot = {}
#    dict_count_vocab = {}
    for csv_path in files:
        list_row = read_csv(csv_path)

        for row in list_row:
            try:
                travel_id, \
                search_tag, \
                date_start, date_end, \
                user_tags, spot_names, spot_urls = row.split(",")
#                # search_tagをvocab.txtに追加(解析器有) 
#                vocabulary_write_Juman(search_tag, tokenizer)
                # search_tagをvocab.txtに追加(解析器無)
                # dict_count_vocabにはカウントしない
                with open("vocab.txt", mode="r") as f:
                    vocab_txt = f.read()
                vocabulary = vocab_txt.split("\n")[:-1]
                with open("vocab.txt", mode="a") as f:
                    if search_tag not in vocabulary:
                        f.write(search_tag+"\n")

            except ValueError:  # 固有名詞にカンマが含まれていることがある。今回は無視。
                continue
            if row == "":
                continue
            if row.count(",") != 6:
                continue
           
            # user_tag(解析器無)
#            for user_tag in user_tags.split("\\"):
#                if user_tag == "":
#                    continue
#                if user_tag not in dict_count_vocab.keys():
#                    dict_count_vocab[user_tag] = 1
#                else:
#                    dict_count_vocab[user_tag] += 1

            # spot
            spots = row.split(",")[5].split("\\")
            urls = row.split(",")[6].split("\\")
            for spot, url in zip(spots, urls):
                if spot == "":
                    continue
                if "駅" in spot or "空港" in spot:
                    if "道の駅" not in spot:
                        continue
                if spot+"\\"+url not in dict_count_spot.keys():
                    dict_count_spot[spot+"\\"+url] = 1
                else:
                    dict_count_spot[spot+"\\"+url] += 1

#    dict_count_vocab = sorted(dict_count_vocab.items(), key=lambda x:x[1], reverse=True)[:cnt_vocab]
    dict_count_spot = sorted(dict_count_spot.items(), key=lambda x:x[1], reverse=True)[:cnt_spot]

#    for vocab in dict_count_vocab:
#        # vocab.txt読み込みモード
#        with open("vocab.txt", mode="r") as f:
#            vocab_txt = f.read()
#        vocabulary = vocab_txt.split("\n")[:-1]
#        # vocab.txt書き込みモード
#        with open("vocab.txt", mode="a") as f:
#            if vocab[0] not in vocabulary:
#                f.write(vocab[0]+"\n")

    for spot in dict_count_spot:
        spot_name = spot[0].split("\\")[0]
        url = spot[0].split("\\")[1]
        spot_add = ""
        # vocab.txt読み込みモード
        with open("vocab.txt", mode="r") as f:
            vocab_txt = f.read()
        vocabulary = vocab_txt.split("\n")[:-1]
        # tsv読み込みモード
        with open("spot.tsv", mode="r") as f:
            spot_csv = f.read()
        list_spot = spot_csv.split("\n")[:-1]
        # tsv書き込みモード
        with open("spot.tsv", mode="a") as f:
            spot_info = spot_name+"\t"+url
            if spot_info not in list_spot:
                # スポット名の被りを考慮
#                cnt = 0
#                for name in [spot.split("\t")[0] for spot in list_spot]:
#                    if spot_name in name:
#                        cnt += 1
#                if cnt == 0:
#                    spot_add += spot_name
#                else:
#                    spot_add += spot_name+"_"+str(cnt+1)
#                f.write(spot_add+"\t"+url+"\n")

                if spot_name in vocabulary: 
                    cnt = 0
                    for name in vocabulary:
                        if spot_name in name:
                            cnt += 1
                    spot_add += spot_name+"_"+str(cnt+1)
                    f.write(spot_add+"\t"+url+"\n")
                else:
                    spot_add += spot_name
                    f.write(spot_info+"\n")
        # vocab.txt書き込みモード
        with open("vocab.txt", mode="a") as f:
            if spot_info not in list_spot:
                f.write(spot_add+"\n")

def vocabulary_original(files):
    """
    user_tagを形態素解析し、全ての要素をボキャブラリとして追加する。
    """
    for csv_path in files:
        list_row = read_csv(csv_path)

        for row in list_row:
            if row == "":
                continue
            generate_vocabulary_original(row)

if __name__ == "__main__":
    files = read_files()

    #vocabulary_original(files)

    cnt_vocab = 2000
    cnt_spot = 2000
    vocabulary_count(files, cnt_vocab, cnt_spot)

