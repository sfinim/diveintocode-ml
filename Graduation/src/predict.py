import numpy as np
from dataset.generate_vocabulary import dict_id_word, dict_spot
from model import *
from pyknp import Juman
import mojimoji

# 単語辞書読み込み
dict_id2word, dict_word2id = dict_id_word(path="dataset/")

# URL辞書の読み込み
dict_spot2url, dict_id2spot, dict_spot2id = dict_spot(path="dataset/")

# モデル読み込み
#model = make_model_BiLSTM()
model = make_model_UniLSTM()
model.load_weights("models/model_final.h5")

while True:

    # 入力
    sequence = input("テスト：")

    ## Q&A形式用処理
    # 形態素解析
    tokenizer = Juman()
    result = tokenizer.analysis(sequence)
    tmp_list_word = [mrph.midasi for mrph in result.mrph_list()]

#    # 単語羅列用処理
#    sequence = mojimoji.zen_to_han(sequence, kana=False)
#    sequence = sequence.lower()
#    tmp_list_word = sequence.split(" ")

    # IDに変換
    maxlen = 20
    list_id = []
    for word in tmp_list_word:
        if word not in list(dict_word2id.keys()):
            list_id.append(int(dict_word2id["<UNK>"]))
        else:
            list_id.append(int(dict_word2id[word]))
#    list_id.append(int(dict_word2id["<SEP>"]))
    num_iter = maxlen-len(list_id)
    for i in range(num_iter):
        list_id.append(int(dict_word2id["<PAD>"]))
    inputs = np.array(list_id).reshape(1, maxlen)

    # 推定
    pred = model.predict(inputs).reshape(len(dict_word2id)+1)
    print(np.sort(pred)[::-1][:10])
    pred = np.argsort(-pred)[:10]
    print(pred)

    # テスト表示用
    for index in pred:
        spot = dict_id2word[index]
        print(spot, dict_spot2url[spot])

    print()
