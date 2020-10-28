import csv
import msvcrt
import numpy as np
import time
import BWT_class

data_list = []      #書き出し用リスト
flag_start = False  #データ書き込み開始フラグ
num = 0             #データの行数
start_time = time.time()      #時間計測用

def sign(x):
    val = 0
    if x>0:
        val = 1
    elif x<0:
        val = -1
    return val

if __name__ == "__main__":
    #センサデータ取得
    jy_sensor =  BWT_class.BWT901("COM5")
    #初期姿勢
    roll, pitch, yaw = jy_sensor.getAngle2()
    initial_roll = roll
    initial_pitch = pitch
    initial_yaw = yaw
    #
    while True:
        roll, pitch, yaw = jy_sensor.getAngle2()
        # 初期化
        if msvcrt.kbhit():
            kb = msvcrt.getch()
            if kb.decode() == 'r' :             #rを入力したら角度初期化, データ書き込み開始
                initial_roll = roll
                initial_pitch = pitch
                initial_yaw = yaw
                flag_start = True
                start_time = time.time()
            elif kb.decode() == 'q' :             #qキーでbreak
                break
        # 角度補正 
        roll -= initial_roll
        pitch -= initial_pitch
        yaw -= initial_yaw
        while abs(roll)>180:
            roll -= sign(roll)*360
        while abs(pitch)>180:
            pitch -= sign(pitch)*360
        while abs(yaw)>180:
            yaw -= sign(yaw)*360  
        # 書き出し用
        str_output = str(time.time() - start_time) + "\t" + str(roll) + "\t" + str(pitch) + "\t" + str(yaw)
        data = str_output.split("\t")    #\t区切りでリストにする
        print(data)        
        if flag_start == True:
            data_list.extend(data)       #書き出し用配列にデータを格納
            num += 1

#---csv書き込み用にデータを変換---#
data_list_csv=np.reshape(data_list,(num,4)).tolist()    #2次元配列に変換　※.tolist()で二次元配列になる

#---csv書き出し--#
with open('C:/Users/inaga/python_files/csv/hoge.csv', 'w', encoding="Shift_jis") as f:
    csvWriter = csv.writer(f, lineterminator='\n')  
    csvWriter.writerows(data_list_csv)          #rowsを使うことで二次元配列のまま書き出し
        