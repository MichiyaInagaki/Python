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
    if len(str_data[0])>5 or len(str_data[0])<4:  #バグ数値を飛ばす
        continue
    f_data = [float(s) for s in str_data]         #floatに変換
    data_list_0.append(f_data[0])
    data_list_1.append(f_data[1])
    print(f_data)   
    #キー入力部
    if msvcrt.kbhit():
        kb = msvcrt.getch()
        if kb.decode() == 'q' :             #qを入力したらbreak
            break

ser.close()

x = np.arange(0, len(data_list_0)/10.0, 0.1)     #グラフのx軸

plt.figure(1)
plt.plot(x, data_list_0)
plt.plot(x, data_list_1)

#FFT
#N = len(data_list_0)    #サンプリング数
#dt = 0.1                #サンプリング間隔
#fft_data_0 = np.fft.fft(data_list_0)    #fft実行
#F_abs = np.abs(fft_data_0)  #絶対値
#F_abs_amp = F_abs / N * 2   #交流成分はデータ数で割って2倍
#F_abs_amp[0] = F_abs_amp[0] / 2 #直流成分は2倍不要
#fq = np.linspace(0, 1.0/dt, N) # 周波数軸　linspace(開始,終了,分割数)
#plt.figure(2)
#plt.plot(fq, F_abs_amp)

#plt.figure(2)
#plt.hist(data_list_0)

#plt.figure(3)
#plt.hist(data_list_1)

plt.show()

