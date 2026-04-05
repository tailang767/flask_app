#renderにアップロードするコード

from flask import Flask, request
from rapidfuzz import fuzz
import unicodedata
import pickle



#pickle読込
with open("単C999円以下の単語.pkl", "rb") as f:
    tanC_999 = pickle.load(f)
with open("単C1000円以上の単語.pkl", "rb") as f:
    tanC_1000 = pickle.load(f)
with open("単C2000円以上の単語.pkl", "rb") as f:
    tanC_2000 = pickle.load(f)
with open("プロパー5000円以上の単語.pkl", "rb") as f:
    proper_5000 = pickle.load(f)
with open("プロパー10000円以上のタイトル.pkl", "rb") as f:
    proper_10000 = pickle.load(f)



#単語と文章に含まれているか判定する
#change_text関数で使う
def calc_tango_similarity(tango, bunsyou, sikiiti):
    #正規化
    tango = unicodedata.normalize("NFKC", tango).lower()
    bunsyou = unicodedata.normalize("NFKC", bunsyou).lower()

    #類似度を返す
    score = fuzz.partial_ratio(tango, bunsyou)
    score = round(score/100, 2)    #例：33.333...→0.33

    #scoreがしきい値未満（しきい値のデフォルト0.5）はスコア0
    if score < sikiiti:
        score = 0
    
    return score    
    


#テキスト加工用関数
def change_text(text, zyanru, kakaku, sikiiti):
    
    return_text = "\n"    #返り値

    #それぞれのtext（OCR取得結果）のスコア算出
    for i, t in enumerate(text.split("\n")):
        #return_text += str(i) + ":" + t + "\n"
        if kakaku == "tanC":
            return_text += " index｜  ~999｜ 1000~｜ 2000~｜   sum｜title\n" + \
                           "ーーーーーーーーーーーーーーーーーーーーーーー\n"
            
            score_list = [0,0,0]
            tango_list = [[],[],[]]
            
            if zyanru == "subete":    #ジャンル絞り込みなし
                for j in tanC_999:     #j = dictのkey
                    for k in tanC_999[j]:    #k = listの各要素（単語）
                        score = calc_tango_similarity(tango=k, bunsyou=t, sikiiti=sikiiti)
                        if score != 0:
                            score_list[0] += score
                            tango_list[0].append(k)
                for j in tanC_1000:
                    for k in tanC_1000[j]:
                        score = calc_tango_similarity(tango=k, bunsyou=t, sikiiti=sikiiti)
                        if score != 0:
                            score_list[1] += score
                            tango_list[1].append(k)
                for j in tanC_2000:
                    for k in tanC_2000[j]:
                        score = calc_tango_similarity(tango=k, bunsyou=t, sikiiti=sikiiti)
                        if score != 0:
                            score_list[2] += score
                            tango_list[2].append(k)

            else:    #ジャンル絞り込みあり
                for j in tanC_999[zyanru]:     #j = listの各要素（単語）
                    score = calc_tango_similarity(tango=j, bunsyou=t, sikiiti=sikiiti)
                    if score != 0:
                        score_list[0] += score
                        tango_list[0].append(j)
                for j in tanC_1000[zyanru]:
                    score = calc_tango_similarity(tango=j, bunsyou=t, sikiiti=sikiiti)
                    if score != 0:
                        score_list[1] += score
                        tango_list[1].append(j)
                for j in tanC_2000[zyanru]:
                    score = calc_tango_similarity(tango=j, bunsyou=t, sikiiti=sikiiti)
                    if score != 0:
                        score_list[2] += score
                        tango_list[2].append(j)

            #足し算の過程で.99999...などが出る可能性あり
            score_list[0] = round(score_list[0], 2)
            score_list[1] = round(score_list[1], 2)
            score_list[2] = round(score_list[2], 2)
            sum_score_list = round(score_list[1]+score_list[2]-score_list[0], 2)

            #良い結果の場合は背景色を変更
            if sum_score_list > 0:
                return_text += "<span style=\"background-color: lightgreen;\">"
            else:
                return_text += "<span>"
            return_text += str(i).rjust(6) + "｜" + str(score_list[0]).rjust(6) + "｜" + \
                           str(score_list[1]).rjust(6) + "｜" + str(score_list[2]).rjust(6) + "｜" + \
                           str(sum_score_list).rjust(6) + "｜" + t + "\n</span>"
            return_text += " ~999で類似と判定された単語:" + str(tango_list[0]) + "\n"
            return_text += "1000~で類似と判定された単語:" + str(tango_list[1]) + "\n"
            return_text += "2000~で類似と判定された単語:" + str(tango_list[2]) + "\n\n\n"
            
        elif kakaku == "proper":
            return_text += " index｜ 5000~｜10000~｜   sum｜title\n" + \
                           "ーーーーーーーーーーーーーーーーーーーーーーー\n"
            
            score_list = [0,0]
            tango_list = [[],[]]

            if zyanru == "subete":    #ジャンル絞り込みなし
                for j in proper_5000:     #j = dictのkey
                    for k in proper_5000[j]:    #k = listの各要素（単語）
                        score = calc_tango_similarity(tango=k, bunsyou=t, sikiiti=sikiiti)
                        if score != 0:
                            score_list[0] += score
                            tango_list[0].append(k)
                for j in proper_10000:
                    for k in proper_10000[j]:
                        score = calc_tango_similarity(tango=t, bunsyou=k, sikiiti=sikiiti)    #tとk逆（kがタイトルのため）
                        if score != 0:
                            score_list[1] += score
                            tango_list[1].append(k)
            
            else:    #ジャンル絞り込みあり
                for j in proper_5000[zyanru]:     #j = listの各要素（単語）
                    score = calc_tango_similarity(tango=j, bunsyou=t, sikiiti=sikiiti)
                    if score != 0:
                        score_list[0] += score
                        tango_list[0].append(j)
                for j in proper_10000[zyanru]:
                    score = calc_tango_similarity(tango=t, bunsyou=j, sikiiti=sikiiti)    #tとj逆（jがタイトルのため）
                    if score != 0:
                        score_list[1] += score
                        tango_list[1].append(j)

            #足し算の過程で.99999...などが出る可能性あり
            score_list[0] = round(score_list[0], 2)
            score_list[1] = round(score_list[1], 2)
            sum_score_list = round(sum(score_list), 2)
            
            #良い結果の場合は背景色を変更
            if sum_score_list > 0:
                return_text += "<span style=\"background-color: lightgreen;\">"
            else:
                return_text += "<span>"
            return_text += str(i).rjust(6) + "｜" + str(score_list[0]).rjust(6) + "｜" + \
                           str(score_list[1]).rjust(6) + "｜" + \
                           str(sum_score_list).rjust(6) + "｜" + t + "\n</span>"
            return_text += " 5000~で類似と判定された単語　　:" + str(tango_list[0]) + "\n"
            return_text += "10000~で類似と判定されたタイトル:" + str(tango_list[1]) + "\n\n\n"

    return return_text





#####ここから先いじらない、いじるとしたら#####
#####<select>タブの中身（ジャンル名）のみ#####
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""

    if request.method == "POST":
        text = request.form.get("user_input")
        zyanru = request.form.get("zyanru")
        kakaku = request.form.get("kakaku")
        sikiiti = request.form.get("sikiiti")

        print("入力:", text)
        print("ジャンル:", zyanru)
        print("価格:", kakaku)
        print("しきい値:", sikiiti)

        #しきい値の値チェック
        try:
            sikiiti = float(sikiiti)
        except:
            sikiiti = 0.5

        text = change_text(text, zyanru, kakaku, sikiiti)

        result = f"""
        <pre>
実行結果:
{text}
        </pre>
        """

    return f"""
    <html>
    <head>
        <style>
            body {{ background-color: #f0f0f0; font-family: sans-serif; }}
            textarea {{ width: 300px; height: 150px; padding: 8px; }}
            select {{ padding: 8px; }}
            input {{ padding: 8px; }}
            button {{ padding: 8px; }}
        </style>
    </head>
    <body>
        <h1>フォーム + プルダウン</h1>

        <form method="POST">
            <textarea name="user_input" placeholder="OCR結果を貼付"></textarea><br><br>


            <p style="font-size: 12px;">ジャンル</p>
            <select name="zyanru">
                <option value="subete">ジャンル：すべて</option>
                <option value="zyanru1">ジャンル1</option>
                <option value="zyanru2">ジャンル2</option>
            </select><br><br>

            <p style="font-size: 12px;">価格</p>
            <select name="kakaku">
                <option value="tanC">単C</option>
                <option value="proper">プロパー</option>
            </select><br><br>

            <p style="font-size: 12px;">しきい値（単語と文章の類似度いくつから拾うか）</p>
            <input type="text" name="sikiiti" placeholder="しきい値（0~1）" value="0.5"><br><br>

            

            <button type="submit">実行</button>
            <hr>
        </form>

        {result}
    </body>
    </html>
    """
    
if __name__ == "__main__":
    app.run()