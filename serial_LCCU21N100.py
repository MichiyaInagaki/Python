import serial
import csv
import msvcrt
import numpy as np

ser = serial.Serial('COM6', 38400, parity=serial.PARITY_EVEN)     #シリアル通信の設定

# 読み込み用コマンド送信部
while True:
    ser.write(b"RCLM\r\n")	 #RCLM：固定小数点型計測値連続読出しのコマンド
    if ser.readline().decode('sjis') == "?":    #エラーのときはもう一度コマンド送信
        continue
    else:
        break

# データ受信部
while True:
    line = ser.readline().decode('sjis')        #シリアルデータの読み込み　※decode('sjis')⇒bytes型からstring型への変換
    str_data = line.rstrip("\r\n").split()      #"\r\n"を削除, 空白区切り（"N"を分離）
    str_data2 = str_data[0].split(",")          #","区切り（"US"）を分離
    f_data = float(str_data2[1])                #float型にキャスト
    print(f_data)   
    #キー入力部
    if msvcrt.kbhit():
        kb = msvcrt.getch()
        if kb.decode() == 'q' :             #qを入力したらbreak
            break

ser.close()
