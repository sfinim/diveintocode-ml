from dataset.generate_vocabulary import dict_id_word, dict_spot

def load_data(path="dataset/QA_label.csv"):
    """
    学習できる形式のデータを返却する
    """
    maxlen = 20

    dict_id2word, dict_word2id = dict_id_word()

    with open(path, mode="r") as f:
        QA_label = f.read()

    sequences = []
    label_words = []
    label_spots = []
    for QA_text_id in QA_label.split("\n"):
        if QA_text_id == "":
            continue
        tmp_sequences = []
        tmp_label_words = [0] * (len(dict_word2id)+1)
        tmp_label_spots = [0] * (len(dict_word2id)+1)
        id_sep_cnt = 0
        for id_ in QA_text_id.split(","):
            if int(id_) == dict_word2id["<SEP>"]:
                id_sep_cnt += 1
                
#            if id_sep_cnt < 2:      # Q&A文章
            if id_sep_cnt == 0:      # Q文章
                tmp_sequences.append(int(id_))
            #elif id_sep_cnt == 2:   # 出力単語
            #    if id_ != "3":
            #        tmp_label_words[int(id_)] = 1
#            elif id_sep_cnt == 2:   # 出力スポット(Q&A文章)
            elif id_sep_cnt == 1:   # 出力スポット(Q文章)
                if int(id_) != dict_word2id["<SEP>"]:
                    tmp_label_spots[int(id_)] = 1
                
        for i in range(maxlen-len(tmp_sequences)):
            tmp_sequences.append(dict_word2id["<PAD>"])
            
        sequences.append(tmp_sequences)
        label_words.append(tmp_label_words)
        label_spots.append(tmp_label_spots)

    return sequences, label_words, label_spots

def load_data_2(path="dataset/id_label.csv"):
    """
    学習できる形式のデータを返却する
    """
    maxlen = 10

    dict_id2word, dict_word2id = dict_id_word()
    _, dict_id2spot, dict_spot2id = dict_spot()

    with open(path, mode="r") as f:
        id_label = f.read()

    sequences = []
    label_spots = []
    for list_id in id_label.split("\n"):
        if list_id == "":
            continue
#        tmp_sequences = [0] * (len(dict_word2id)+1)
        tmp_sequences = []
        tmp_label_spots = [0] * (len(dict_spot2id)+1)
        id_sep_cnt = 0
        for id_ in list_id.split(","):
            if id_ == "_":
                id_sep_cnt += 1
                
            if id_sep_cnt == 0:      # 検索ワード
                if len(tmp_sequences) == maxlen:
                    continue
                tmp_sequences.append(int(id_))
#                tmp_sequences[int(id_)] = 1
            elif id_sep_cnt == 1:   # 出力スポット
                if id_ != "_":
                    tmp_label_spots[int(id_)] = 1
                
        for i in range(maxlen-len(tmp_sequences)):
            tmp_sequences.append(dict_word2id["<PAD>"])
            
        sequences.append(tmp_sequences)
        label_spots.append(tmp_label_spots)

    return sequences, label_spots

