import requests
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import re
import os
from googletrans import Translator
import glob
a
def is_float(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return True


def get_text_from_pdf(pdfname):
    limit=1000
    # PDFファイル名が未指定の場合は、空文字列を返して終了
    if (pdfname == ''):
        return ''
    else:
        # 処理するPDFファイルを開く/開けなければ
        try:
            fp = open(pdfname, 'rb')
        except:
            return ''

    # PDFからテキストの抽出
    rsrcmgr = PDFResourceManager()
    out_fp = StringIO()
    la_params = LAParams()
    la_params.detect_vertical = True
    device = TextConverter(rsrcmgr, out_fp, laparams=la_params)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp, pagenos=None, maxpages=0, password=None, caching=True, check_extractable=True):
        interpreter.process_page(page)
    text = out_fp.getvalue()
    fp.close()
    device.close()
    out_fp.close()

    # 改行で分割する
    lines = text.splitlines()

    outputs = []
    output = ""

    # 除去するutf8文字
    replace_strs = [b'\x00']

    is_blank_line = False

    # 分割した行でループ
    for line in lines:

        # byte文字列に変換
        line_utf8 = line.encode('utf-8')

        # 余分な文字を除去する
        for replace_str in replace_strs:
            line_utf8 = line_utf8.replace(replace_str, b'')

        # strに戻す
        line = line_utf8.decode()

        # 連続する空白を一つにする
        line = re.sub("[ ]+", " ", line)

        # 前後の空白を除く
        line = line.strip()
        #print("aft:[" + line + "]")

        # 空行は無視
        if len(line) == 0:
            is_blank_line = True
            continue

        # 数字だけの行は無視
        if is_float(line):
            continue

        # 1単語しかなく、末尾がピリオドで終わらないものは無視
        if line.split(" ").count == 1 and not line.endswith("."):
            continue

        # 文章の切れ目の場合
        if is_blank_line or output.endswith("."):
            # 文字数がlimitを超えていたらここで一旦区切る
            if(len(output) > limit):
                outputs.append(output)
                output = ""
            else:
                output += "\r\n"
        #前の行からの続きの場合
        elif not is_blank_line and output.endswith("-"):
            output = output[:-1]
        #それ以外の場合は、単語の切れ目として半角空白を入れる
        else:
            output += " "

        #print("[" + str(line) + "]")
        output += str(line)
        is_blank_line = False

    outputs.append(output)
    return outputs


def translate(input):
    # 変更
    translator = Translator()
    result = translator.translate(str(input), dest="ja")

    return result.text

def make_files(file_pdf, file_en, file_ja):
    # pdfをテキストに変換
    inputs = get_text_from_pdf(file_pdf)

    with open(file_en, "w", encoding="utf-8") as f_text:
        with open(file_ja, "w", encoding="utf-8") as f_trans:

            # 一定文字列で分割した文章毎にAPIを叩く
            for i, input_ in enumerate(inputs):
                print("{0}/{1} is proccessing".format((i+1), len(inputs)))
                # 結果をファイルに出力
                f_text.write(input_)
                f_trans.write(translate(input_))

def main():
    path = os.getcwd()
    dir_pdf = path + "/pdf/"
    dir_en = path + "/en/"
    dir_ja = path + "/ja/"

    pdf_files = glob.glob(dir_pdf + "*")
    en_files = glob.glob(dir_en + "*")
    ja_files = glob.glob(dir_ja + "*")

    list_filename = []

    for file_pdf in pdf_files:
        flg_en = 0
        flg_ja = 0

        file_name_txt = file_pdf[len(dir_pdf):-4] + ".txt"

        for file_en in en_files:
            file_name_en = file_en[len(dir_en):]
            if "en_"+file_name_txt == file_name_en:
                flg_en = 1

        for file_ja in ja_files:
            file_name_ja = file_ja[len(dir_ja):]
            if "ja_"+file_name_txt == file_name_ja:
                flg_ja = 1

        # 変換ファイルが作成されてないファイルのみ処理する
        if flg_en == 0 and flg_ja == 0:
            list_filename.append(file_pdf)
 
    for file_pdf in list_filename:
        file_name = file_pdf[len(dir_pdf):-4]
        file_en = path + "/en/en_" + file_name + ".txt"
        file_ja = path + "/ja/ja_" + file_name + ".txt"
        
        print("proccessing file:{}".format(file_pdf[len(dir_pdf):]))
        make_files(file_pdf, file_en, file_ja)

if __name__ == "__main__":
    main()

