#使い方
#"r"キーでデータ書き込み開始
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
start_time = time.time()      #時間計測用
time_data = [0]     #計測時間格納用 + データ配列格納用 = 一行分

while True:
    time_data = [time.time() - start_time]
    #シリアルデータ格納部
    line = ser.readline().decode('sjis')    #シリアルデータの読み込み　※decode('sjis')⇒bytes型からstring型への変換
    data = line.rstrip("\n").split("\t")    #"\n"を削除, \t区切り
    if data==['\r']:                        #['\r']の行をパスする
        continue
    time_data.extend(data)
    print(time_data)   
    if flag_start == True:                  #スタートフラグが立ってからデータの格納開始       
        data_list.extend(time_data)              #書き出し用配列にデータを格納　※extendはリストの追加（appendは要素の追加なのでNG）
        num+=1
    #キー入力部
    if msvcrt.kbhit():
        kb = msvcrt.getch()
        if kb.decode() == 'r' :             #rを入力したら角度初期化（arduino側に0を送る）,データ書き込み開始
            ser.write(b"0")
            flag_start = True
            start_time = time.time()        #時間計測開始
        elif kb.decode() == 'q' :           #qを入力したらbreak
            break

#---csv書き込み用にデータを変換---#
data_list_csv=np.reshape(data_list,(num,4)).tolist()    #2次元配列に変換　※.tolist()で二次元配列になる

#---csv書き出し--#
with open('C:/Users/inaga/python_files/csv/miyatake_zai.csv', 'w', encoding="Shift_jis") as f:
    csvWriter = csv.writer(f, lineterminator='\n')  
    csvWriter.writerows(data_list_csv)          #rowsを使うことで二次元配列のまま書き出し

ser.close()