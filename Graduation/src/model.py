from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input, Embedding, LSTM, Flatten, GRU
from tensorflow.keras.layers import Bidirectional

from dataset.generate_vocabulary import dict_id_word, dict_spot


# 単語辞書読み込み
dict_id2word, dict_word2id = dict_id_word(path="dataset/")
dict_spot2url, dict_id2spot, dict_spot2id = dict_spot(path="dataset/")

# モデル定義
def make_model_BiLSTM():
    # ハイパーパラメータ設定
    vocabulary = len(dict_id2word)+1
    hid_dim = 400
    emb_dim = 200
    length=20

    input_ = Input(shape=(length), name='input')
    embedding = Embedding(input_dim=vocabulary,
                           output_dim=emb_dim,
                           mask_zero=True,
                           name='embedding',
                           input_length=length)
    lstm = LSTM(hid_dim,
                 return_sequences=True,
                 name='lstm')
    bilstm = Bidirectional(lstm, name='bilstm')
    flatten = Flatten()
    fc = Dense(vocabulary, activation='softmax')

    x = input_
    embedding = embedding(x)
    lstm = bilstm(embedding)
    y = flatten(lstm)
    y = fc(y)
    model = Model(inputs=x, outputs=y)
    model.compile(optimizer='adam', loss='categorical_crossentropy')
    print(model.summary())

    return model

def make_model_UniLSTM():
    # ハイパーパラメータ設定
    vocabulary = len(dict_id2word)+1
    hid_dim = 400
    emb_dim = 200
    length=20

    input_ = Input(shape=(length), name='input')
    embedding = Embedding(input_dim=vocabulary,
                           output_dim=emb_dim,
                           mask_zero=True,
                           name='embedding',
                           input_length=length)
    lstm = LSTM(hid_dim,
                 return_sequences=True,
                 name='lstm')
    flatten = Flatten()
    fc = Dense(vocabulary, activation='softmax')

    x = input_
    embedding = embedding(x)
    lstm = lstm(embedding)
    y = flatten(lstm)
    y = fc(y)
    model = Model(inputs=x, outputs=y)
    model.compile(optimizer='adam', loss='categorical_crossentropy')
    print(model.summary())

    return model

def make_model_UniGRU():
    # ハイパーパラメータ設定
    vocabulary = len(dict_id2word)+1
    hid_dim = 400
    emb_dim = 200
    length=20

    input_ = Input(shape=(length), name='input')
    embedding = Embedding(input_dim=vocabulary,
                           output_dim=emb_dim,
                           mask_zero=True,
                           name='embedding',
                           input_length=length)
    gru = GRU(hid_dim,
              return_sequences=True,
              name='gru')
    flatten = Flatten()
    fc = Dense(vocabulary, activation='softmax')

    x = input_
    embedding = embedding(x)
    g = gru(embedding)
    y = flatten(g)
    y = fc(y)
    model = Model(inputs=x, outputs=y)
    model.compile(optimizer='adam', loss='categorical_crossentropy')
    print(model.summary())

    return model

