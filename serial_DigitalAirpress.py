import serial
import csv
import msvcrt
import numpy as np
import matplotlib.pyplot as plt
import time

ser = serial.Serial('COM3', 9600)     #シリアル通信の設定
data_list_0 = []      #書き出し用リスト
data_list_1 = []      #書き出し用リスト
time.sleep(1.0)     #遅延入れる

# データ受信部
while True:
    line = ser.readline().decode('sjis')        #シリアルデータの読み込み　※decode('sjis')⇒bytes型からstring型への変換
    str_data = line.rstrip("\n").split("\t")    #\nを削除, \t区切り
    if len(str_data)==1:                        #改行文字とバグ数値を飛ばす
        continue
    if len(str_data[0])==0 or len(str_data[1])==0:                     #バグ数値を飛ばす
        continue
    i_data = [int(s) for s in str_data]         #floatに変換
    data_list_0.append(i_data[0])
    data_list_1.append(i_data[1])
    print(i_data)   
    #キー入力部
    if msvcrt.kbhit():
        kb = msvcrt.getch()
        if kb.decode() == 'q' :             #qを入力したらbreak
            break

ser.close()

#--- plot ---#
x = np.arange(0, len(data_list_0)/10.0, 0.1)     #グラフのx軸

plt.figure(1)
plt.plot(x, data_list_0)
plt.plot(x, data_list_1)
plt.show()

