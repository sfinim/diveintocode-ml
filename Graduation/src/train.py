from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.backend import clear_session
import numpy as np

from dataset.preprocessing import *
from model import *


# ハイパーパラメータ設定
batch_size = 32
epoch=10

if __name__ == "__main__":

    num_data_divide = 6
    iter_ = 3
    cnt = 0
    for i in range(iter_):
        for j in range(num_data_divide):
            print("[{}/{}]".format(cnt+1, num_data_divide*iter_))
            # データセット読み込み
            print("loading dataset...")
            filepath_csv = "dataset/QA_label_{}.csv".format(j+1)
            sequences, label_words, label_spots = load_data(path=filepath_csv)
#            sequences, label_spots = load_data_2(path=filepath_csv)
            sequences = np.array(sequences)
#            label_words = np.array(label_words)
            label_spots = np.array(label_spots)

            # モデル定義
#            model = make_model_BiLSTM()
#            model = make_model_UniLSTM()
            model = make_model_UniGRU()
 
            # 重み読み込み
            if cnt != 0:
                model.load_weights("models/model_{}.h5".format(cnt))
  
            # コールバック設定
            if cnt != num_data_divide*iter_-1:
                filepath_h5 = "models/model_{}.h5".format(cnt+1)
            else:
                filepath_h5 = "models/model_final.h5"
            callbacks = [EarlyStopping(patience=3),
                         ModelCheckpoint(filepath=filepath_h5,
                                         save_best_only=True)]
  
            # 学習
            model.fit(x=sequences,
                      y=label_spots,
                      batch_size=batch_size,
                      epochs=epoch,
                      validation_split=0.1,
                      callbacks=callbacks,
                      shuffle=True)
 
            # リソース確保 
            clear_session()
            del sequences
            del label_spots
            del model
            del callbacks

            cnt += 1
 
