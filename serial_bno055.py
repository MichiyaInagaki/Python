#使い方
#"r"キーでデータ書き込み開始
#"a"キー，"s"キーでラベル分け
#"q"キーで終了

import serial
import csv
import msvcrt
import numpy as np
import time

ser = serial.Serial('COM3', 115200)     #シリアル通信の設定
data_list = []      #書き出し用リスト
label = [0]         #正解ラベル格納用 + データ配列格納用 = 一行分
flag_label = 0      #ラベル分け用フラグ
flag_start = False  #データ書き込み開始フラグ
num = 0             #データの行数
time.sleep(1.0)     #遅延入れる

while True:
    #正解ラベルデータ格納部
    if flag_label==0:
        label=['0']
    elif flag_label==1:
        label=['1']
    #シリアルデータ格納部
    line = ser.readline().decode('sjis')    #シリアルデータの読み込み　※decode('sjis')⇒bytes型からstring型への変換
    data = line.rstrip("\n").split("\t")    #"\n"を削除, \t区切り
    if data==['\r']:                        #['\r']の行をパスする
        continue
    label.extend(data)                      #labelは，[正解ラベル，シリアルデータ（特徴ベクトル）]の配列 = 一行分
    print(label)   
    if flag_start == True:                  #スタートフラグが立ってからデータの格納開始       
        data_list.extend(label)             #書き出し用配列にデータを格納　※extendはリストの追加（appendは要素の追加なのでNG）
        num+=1
    #キー入力部
    if msvcrt.kbhit():
        kb = msvcrt.getch()
        if kb.decode() == 'a' :               #aを入力したらラベル切り替え0
            flag_label=0
        elif kb.decode() == 's' :             #sを入力したらラベル切り替え1
            flag_label=1
        elif kb.decode() == 'r' :             #rを入力したら角度初期化（arduino側に0を送る）,データ書き込み開始
            ser.write(b"0")
            flag_start = True
        elif kb.decode() == 'q' :             #qを入力したらbreak
            break

#---csv書き込み用にデータを変換---#
#data_list_f=[float(s) for s in data_list]    #float型に変換（なんかバグるときあるので使わない）
#データの欠損対応（不要？」）
if len(data_list)%3==1:                       #1行目のデータに1個しか値がないときは1つデータを削除し，一行目を消す
    del data_list[0]                                   
    num = num-1
elif len(data_list)%3==2:                     #1行目のデータに2個しか値がないときは2つデータを削除し，一行目を消す
    del data_list[0]
    del data_list[0]                                   
    num = num-1

data_list_csv=np.reshape(data_list,(num,3)).tolist()    #2次元配列に変換　※.tolist()で二次元配列になる

#---csv書き出し--#
with open('C:/Users/inaga/OneDrive/ドキュメント/Python_files/csv/hoge.csv', 'w', encoding="Shift_jis") as f:
    csvWriter = csv.writer(f, lineterminator='\n')  
    csvWriter.writerows(data_list_csv)          #rowsを使うことで二次元配列のまま書き出し

ser.close()