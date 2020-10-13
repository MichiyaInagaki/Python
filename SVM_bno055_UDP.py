import numpy as np
import serial
import socket
import msvcrt
import matplotlib.pyplot as pyplot
from sklearn import svm
from sklearn.metrics import confusion_matrix
from mlxtend.plotting import plot_decision_regions

# --- UDP通信設定 --- #
HOST = '127.0.0.1'
PORT = 50007
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# --- 学習フェーズ --- #
# 教師データの読み込み
data = np.loadtxt('C:/Users/inaga/OneDrive/ドキュメント/Python_files/csv/sample.csv', delimiter=',')
y = data[:,0].astype(int)   #正解ラベル
x = data[:,1:3]             #特徴ベクトル

# 学習モデルの設定
clf = svm.SVC(C=10, kernel='rbf', gamma=0.1)
# 学習させる
clf.fit(x, y)

# --- 予測フェーズ --- #
ser = serial.Serial('COM3', 115200)     #シリアル通信の設定
flag_start = False  #予測開始フラグ

while True:
    line = ser.readline().decode('sjis')    #シリアルデータの読み込み　※decode('sjis')⇒bytes型からstring型への変換
    data = line.rstrip("\n").split("\t")    #"\n"を削除, \t区切り #特徴ベクトル
    if data==['\r']:                        #['\r']の行をパスする
        continue
    if flag_start == True:                  #予測開始したら予測の処理に入る
        data_f = [float(s) for s in data]           #floatに変換
        data2_f=np.reshape(data_f,(1,2)).tolist()   #2次元配列に変換　※.tolist()で二次元配列になる
        #print(data2_f)
        result = clf.predict(data2_f)               #予測＋結果の格納（リスト型）
        #print('予測した結果',result)  
        UDP_data = str(result[0]) + "," + str(data_f[1]) + "," +str(data_f[0]) #送信用データ（正解ラベル，yaw角，Pitch角）
        print(UDP_data)
        client.sendto(UDP_data.encode('utf-8'),(HOST,PORT))   #UDP送信 to Unity
    if msvcrt.kbhit():
        kb = msvcrt.getch()
        if kb.decode() == 'q' :             #qを入力したらbreak
            break
        elif kb.decode() == 'r' :           #rを入力したら角度初期化（arduino側に0を送る）,データ予測開始
            ser.write(b"0")
            flag_start = True


