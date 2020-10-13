from multiprocessing import Manager,Value, Process
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
def realtime_graph_rawdata(t, y):
    plt.plot(t, y) #(t, y)のプロット
    plt.xlabel("t[s]")
    plt.ylabel("y")
    plt.grid()          #グリッド表示
    plt.draw()          #グラフの描画
    plt.pause(0.01)     #引数の指定時間だけ表示を継続（＝更新間隔）
    plt.clf()           #画面初期化 


# 周波数解析のリアルタイムプロット
def graph_FFT(t, y, N, dt):
    # 生データ
    plt.subplot(2,1,1)
    plt.plot(t, y) #(t, y)のプロット
    plt.xlabel("t[s]")
    plt.ylabel("y")
    plt.grid()          #グリッド表示
    # 周波数解析
    plt.subplot(2,1,2)
    F = np.fft.fft(y) # FFT結果
    freq = np.fft.fftfreq(N, d=dt)  # 周波数
    Amp = np.abs(F/(N/2))           #振幅
    # ピーク検出
    _freq = np.array(freq[55:75])
    _Amp = np.array(Amp[55:75])
    maxid = signal.argrelmax(_Amp, order=3) 
    plt.plot(_freq[maxid],_Amp[maxid],'ro')
    str_temp = "Heart rate: "
    for i in range(len(maxid[0])):
        str_temp += str('{:.1f}'.format(60*_freq[maxid[0][i]]))+ " "   
        plt.title(str_temp)
    #
    plt.plot(freq[1:int(N/2)], Amp[1:int(N/2)])     #プロット
    plt.xlabel("freq")
    plt.ylabel("Amp")
    plt.grid()          #グリッド表示
    plt.draw()          #グラフの描画
    plt.pause(0.01)     #引数の指定時間だけ表示を継続（＝更新間隔）
    plt.clf()           #画面初期化 


# サブプロセス：センサデータの取得
def data_receiver(count, data_array, time_array):
    ser = serial.Serial('COM3', 115200)     #シリアル通信の設定
    start = time.time()                     #計測開始時間
    while True:
        #データ受信部
        line = ser.readline().decode('sjis')        #シリアルデータの読み込み　※decode('sjis')⇒bytes型からstring型への変換
        str_data = line.rstrip("\n").split("\t")    #\nを削除, \t区切り
        if len(str_data)==1:                        #改行文字とバグ数値を飛ばす
            continue
        if len(str_data[0])==0 or len(str_data[1])==0:                     #バグ数値を飛ばす
            continue
        i_data = [int(s) for s in str_data]         #int型に変換
        timing = time.time() - start                #経過時間
        data_array.append(i_data[0])
        time_array.append(timing)
        print(i_data)
        count.value += 1
        #キー入力部
        if msvcrt.kbhit():
            kb = msvcrt.getch()
            if kb.decode() == 'q' :             #qを入力しらbreak
                break
    ser.close()


# サブプロセス：データのフィルタリング処理
def data_filtering(count, data_array, time_array):
    #フィルタ用
    n = 128                     #フィルタ区間のデータ個数
    lowcut_heartbeat = 0.77     #カットオフ周波数[Hz]（心拍）
    highcut_heartbeat = 2.0
    lowcut_respiration = 0.1    #カットオフ周波数[Hz]（呼吸）
    highcut_respiration = 0.4 
    #fs = 10.0                  ###サンプリング周波数（カットオフ周波数の2倍以上必要）
    #フィルタリング処理
    while True:
        if count.value>n-1:
            # フィルタリング処理を行うフレームの情報
            i = count.value     #データ番号
            window_time_array = time_array[i-n:i]   #時間フレームの抽出
            window_time = window_time_array[n-1]-window_time_array[0]   #フレーム時間
            Ts = window_time/n  #サンプリング間隔
            fs = 1/Ts           #サンプリング周波数
            #print("fs", 1/Ts)
            ### 全グラフリアルタイム同時プロット
            y_filter_H = butter_bandpass_filter(data_array[i-n:i], lowcut_heartbeat, highcut_heartbeat, fs, order=4)        #心拍フィルタリング
            y_filter_R = butter_bandpass_filter(data_array[i-n:i], lowcut_respiration, highcut_respiration, fs, order=4)    #呼吸フィルタリング
            realtime_graph_all(time_array[i-n:i], data_array[i-n:i], y_filter_H, y_filter_R)      
            ### 生データのみリアルタイムプロット
            #realtime_graph_rawdata(time_array[i-n:i], data_array[i-n:i]) 
        #キー入力部
        if msvcrt.kbhit():
            kb = msvcrt.getch()
            if kb.decode() == 'q' :             #qを入力したらbreak
                break


# サブプロセス：周波数解析
def data_FFT(count, data_array, time_array):
    n = 512                     #フィルタ区間のデータ個数
    while True:
        if count.value>n-1:
            # 処理を行うフレームの情報
            i = count.value     #データ番号
            window_time_array = time_array[i-n:i]   #時間フレームの抽出
            window_time = window_time_array[n-1]-window_time_array[0]   #フレーム時間
            Ts = window_time/n  #サンプリング間隔
            ### 周波数解析リアルタイムプロット
            graph_FFT(time_array[i-n:i], data_array[i-n:i], n, Ts) 
        #キー入力部
        if msvcrt.kbhit():
            kb = msvcrt.getch()
            if kb.decode() == 'q' :             #qを入力したらbreak
                break


if __name__ == '__main__':
    # Managerオブジェクトの作成
    with Manager() as manager:
        # マネージャーからValueクラスを作成
        count = manager.Value('i', 0)
        # マネージャーからListを作成
        data_array = manager.list()
        time_array = manager.list()
        # サブプロセスの作成
        process_data_receive = Process(target=data_receiver, args=[count, data_array, time_array])
        #process_data_filter = Process(target=data_filtering, args=[count, data_array, time_array])
        process_data_FFT = Process(target=data_FFT, args=[count, data_array, time_array])
        # サブプロセスの開始
        process_data_receive.start()
        #process_data_filter.start()
        process_data_FFT.start()
        # サブプロセスの終了
        process_data_receive.join()
        #process_data_filter.join()
        process_data_FFT.join()
        print("process ended")