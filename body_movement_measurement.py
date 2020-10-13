#Degital_airpress.ino

import serial
import msvcrt
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy import signal


# フィルタ伝達関数の分子と分母(b, a)を計算する関数
# lowcut, highcut：カットオフ周波数f1, f2，fs：サンプリング周波数，order：次数
def butter_bandpass(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs		# ナイキスト周波数
    low = lowcut / nyq		# 正規化周波数
    high = highcut / nyq		# 正規化周波数
    b, a = signal.butter(order, [low, high], btype='band')
    return b, a

# フィルタ本体部分
def butter_bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y_filter = signal.filtfilt(b, a, data)
    return y_filter


#全グラフ並べてリアルタイム描画　引数（時間軸，生データ，心拍フィルタリングデータ，呼吸フィルタリングデータ）
def realtime_graph_all(t, y_raw, y_H, y_R):
    #生データのプロット----------------------
    plt.subplot(3,1,1)
    plt.plot(t, y_raw) 
    plt.title("raw data")
    plt.ylabel("airpress")
    plt.grid()      #グリッド表示
    #心拍のプロット--------------------------
    plt.subplot(3,1,2)
    # ピーク検出
    _t = np.array(t)
    _y = np.array(y_H)
    maxid = signal.argrelmax(_y, order=1)   #ピーク（最大値）の取得
    plt.plot(_t[maxid],_y[maxid],'ro')      #ピーク点のプロット
    # 心拍数の計算（ピーク間の時間の平均＝心拍周期）
    if len(maxid[0])>1:                     #ピークが2個以上のときのみ計算
        temp = 0
        for i in range(len(maxid[0])-1):
            temp += _t[maxid[0][i+1]] - _t[maxid[0][i]]     #区間内の平均周期を計算する
        Rt = temp/(len(maxid[0])-1)                         #平均周期
        Rn = 60/Rt                                          #心拍数＝毎分何回
        str_data = "Heart rate: " + str('{:.3f}'.format(Rn))
        plt.title(str_data)     #タイトルにプロット
    plt.plot(t, y_H)    
    plt.ylabel("output")
    plt.grid()                 
    #呼吸のプロット----------------------------------
    plt.subplot(3,1,3)
    # ピーク検出
    _t = np.array(t)
    _y = np.array(y_R)
    maxid = signal.argrelmax(_y, order=1) 
    plt.plot(_t[maxid],_y[maxid],'ro')
    # 呼吸数の計算
    if len(maxid[0])>1:                            #ピークが2個以上のときのみ計算
        temp = 0
        for i in range(len(maxid[0])-1):
            temp += _t[maxid[0][i+1]] - _t[maxid[0][i]]     
        Rt = temp/(len(maxid[0])-1)                 #平均周期
        Rn = 60/Rt                                  #呼吸数＝毎分何回
        str_data = "Respiration rate: " + str('{:.3f}'.format(Rn))
        plt.title(str_data)
    plt.plot(t, y_R) 
    plt.xlabel("t[s]")
    plt.ylabel("output")
    plt.grid()          
    #プロット部分-------------------------------------------
    plt.draw()          #グラフの描画
    plt.pause(0.01)     #引数の指定時間だけ表示を継続（＝更新間隔）
    plt.clf()           #画面初期化 


#生データリアルタイム描画用
def realtime_graph_rawdata(t, y, fig_num):
    plt.figure(fig_num)
    plt.plot(t, y) #(t, y)のプロット
    plt.xlabel("t[s]")
    plt.ylabel("y")
    plt.grid()          #グリッド表示
    plt.draw()          #グラフの描画
    plt.pause(0.01)     #引数の指定時間だけ表示を継続（＝更新間隔）
    plt.clf()           #画面初期化 
 

#フィルタリングデータ区間ごと描画用
def sampling_plot_filtered(t, y, fig_num):
    plt.figure(fig_num)
    plt.clf()           #画面初期化 
    #ピーク検出
    _t = np.array(t)
    _y = np.array(y)
    maxid = signal.argrelmax(_y, order=1) #最大値
    plt.plot(_t[maxid],_y[maxid],'ro',label='ピーク値')
    #ピーク周期
    if len(maxid[0])>1:                            #ピークが2個以上のときのみ計算
        temp = 0
        for i in range(len(maxid[0])-1):
            temp += _t[maxid[0][i+1]] - _t[maxid[0][i]]     #区間内の平均周期を計算する
        Rt = temp/(len(maxid[0])-1)                 #平均周期
        Rn = 60/Rt                                  #毎分何回
        print("cycle[秒]",Rt,"rate[回/分]",Rn)
    #(t, y)のプロット
    plt.plot(t, y) 
    plt.xlabel("t[s]")
    plt.ylabel("y")
    plt.grid()          #グリッド表示
    plt.draw()          #グラフの描画   


def main():
    ser = serial.Serial('COM3', 115200)     #シリアル通信の設定
    #初期値
    y = []      #縦軸：センサ値
    t = []      #横軸：時間
    i = 0
    k = 0
    start = time.time()         #計測開始時間
    old_time = time.time()      #サンプリング間隔計測用
    #フィルタ用
    n = 128                     #フィルタ区間のデータ個数
    lowcut_heartbeat = 0.77     #カットオフ周波数[Hz]（心拍）
    highcut_heartbeat = 2.0
    lowcut_respiration = 0.1    #カットオフ周波数[Hz]（呼吸）
    highcut_respiration = 0.4 
    fs = 4.1                    ###サンプリング周波数（カットオフ周波数の2倍以上必要）
    #データ受信用
    buffer_string = ''
    last_received = ''

    while True:
        #データ受信部
        #シリアル通信に残っている最後の行（＝最新データ）を取得する
        buffer_string = buffer_string + ser.read(ser.inWaiting()).decode('sjis')
        if '\n' in buffer_string:
            lines = buffer_string.split('\n') 
            last_received = lines[-2]
            buffer_string = lines[-1]
        line = last_received
        str_data = line.rstrip("\n").split("\t")    #\nを削除, \t区切り
        if len(str_data)==1:                        #改行文字とバグ数値を飛ばす
            continue
        if len(str_data[0])==0 or len(str_data[1])==0:     #バグ数値を飛ばす
            continue
        i_data = [int(s) for s in str_data]         #int型に変換
        timing = time.time() - start                #経過時間
        t.append(timing)
        y.append(i_data[1])
        print(i_data)   
        i+=1
        k+=1
        #グラフ描画
        if i>n:
            #全グラフリアルタイム同時プロット
            y_filter_H = butter_bandpass_filter(y[i-n:i], lowcut_heartbeat, highcut_heartbeat, fs, order=4)
            y_filter_R = butter_bandpass_filter(y[i-n:i], lowcut_respiration, highcut_respiration, fs, order=4)
            realtime_graph_all(t[i-n:i], y[i-n:i], y_filter_H, y_filter_R)
            #生データのみリアルタイムプロット
            #realtime_graph_rawdata(t[i-n:i], y[i-n:i], 1)   
            Ts = time.time() - old_time                 #サンプリング間隔
            print("Ts", Ts, "Fs", 1/Ts)
            old_time = time.time()
        '''
        if k==n:
            k=0
            #フィルタリング（一定区間ごとに実行）
            y_filter_H = butter_bandpass_filter(y[i-n:i], lowcut_heartbeat, highcut_heartbeat, fs, order=4)
            y_filter_R = butter_bandpass_filter(y[i-n:i], lowcut_respiration, highcut_respiration, fs, order=4)
            sampling_plot_filtered(t[i-n:i], y_filter_H, 2)
            sampling_plot_filtered(t[i-n:i], y_filter_R, 3)
        '''

        #キー入力部
        if msvcrt.kbhit():
            kb = msvcrt.getch()
            if kb.decode() == 'q' :             #qを入力したらbreak
                break

    ser.close()


if __name__ == '__main__':
    main()
