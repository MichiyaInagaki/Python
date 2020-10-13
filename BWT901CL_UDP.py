import socket
import random
import time
import BWT_class
from multiprocessing import Manager,Value, Process

def sign(x):
    val = 0
    if x>0:
        val = 1
    elif x<0:
        val = -1
    return val

def angle_to_pos(yaw, pitch):
    x = -yaw*10+872
    y = pitch*10-720
    return x, y

def data_receiver(_yaw, _pitch):
    #センサデータ取得
    jy_sensor =  BWT_class.BWT901("COM5")
    #初期化
    roll, pitch, yaw = jy_sensor.getAngle2()
    initial_pitch = pitch
    initial_yaw = yaw
    #
    while True:
        roll, pitch, yaw = jy_sensor.getAngle2()
        # 角度補正 
        yaw -= initial_yaw
        pitch -= initial_pitch
        while abs(pitch)>180:
            pitch -= sign(pitch)*360
        while abs(yaw)>180:
            yaw -= sign(yaw)*360  
        # 角度の格納
        _yaw.value = yaw
        _pitch.value = pitch    

def udp_sender(_yaw, _pitch):
    # UDP通信の設定
    HOST = '127.0.0.1'
    PORT = 50007
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
    while True:
        # 送信データ
        result = str(_yaw.value) + "," + str(_pitch.value)
        print(result)
        client.sendto(result.encode('utf-8'),(HOST,PORT))
        time.sleep(0.1)

if __name__ == "__main__":
    # Managerオブジェクトの作成
    with Manager() as manager:
        # マネージャーからValueクラスを作成
        _yaw = manager.Value('i', 0)
        _pitch = manager.Value('i', 0)
        # サブプロセスの作成
        process_data_receive = Process(target=data_receiver, args=[_yaw, _pitch])
        process_udp_send = Process(target=udp_sender, args=[_yaw, _pitch])
        # サブプロセスの開始
        process_data_receive.start()
        process_udp_send.start()
        # サブプロセスの終了
        process_data_receive.join()
        process_udp_send.join()
        print("process ended")

