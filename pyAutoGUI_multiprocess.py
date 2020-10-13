import pyautogui
from serial import Serial
from multiprocessing import Manager,Value, Process
import BWT_class   
import math

def sign(x):
    val = 0
    if x>0:
        val = 1
    elif x<0:
        val = -1
    return val

def angle_to_pos(yaw, pitch):
    x = yaw*10+872
    y = -pitch*10-720
    return x, y

def data_receiver(_yaw, _pitch):
    jy_sensor =  BWT_class.BWT901("COM5")
    #初期化
    roll, pitch, yaw = jy_sensor.getAngle2()
    initial_pitch = pitch
    initial_yaw = yaw
    while True:
        roll, pitch, yaw = jy_sensor.getAngle2()
        # 角度補正 
        yaw -= initial_yaw
        pitch -= initial_pitch
        while abs(pitch)>180:
            pitch -= sign(pitch)*360
        while abs(yaw)>180:
            yaw -= sign(yaw)*360
        # 受け渡し用変数に代入       
        _yaw.value = yaw
        _pitch.value = pitch    
        print(_yaw.value, _pitch.value)    

def mouse_move(_yaw, _pitch):
    pre_x_pos = 872  
    pre_y_pos = -720
    temp_x_pos = 872
    temp_y_pos = -720
    pyautogui.sleep(2)
    pyautogui.moveTo(872, -720, duration=0.0)   #初期位置
    while True:
        # 角度から座標への変換    
        x_pos, y_pos = angle_to_pos(_yaw.value, _pitch.value)
        # ローパスフィルタ
        x_pos = pre_x_pos*0.5+x_pos*(1-0.5)
        y_pos = pre_y_pos*0.5+y_pos*(1-0.5)
        pre_x_pos = x_pos
        pre_y_pos = y_pos
        #print(x_pos, y_pos)  
        #pitchを+60度または-60度以上にすることで自動操作解除   
        if abs(_pitch.value)<60:
            ### 以下，youtube用
            pyautogui.mouseDown()
            pyautogui.moveTo(x_pos, y_pos, duration=0.0)
            ### 以下，matterport用
            #if len_point((x_pos-temp_x_pos), (y_pos-temp_y_pos)) > 100:
            #    pyautogui.dragTo(x_pos, y_pos, duration=0.5)
            #    temp_x_pos = x_pos
            #    temp_y_pos = y_pos
        else:
            pyautogui.mouseUp()    

def len_point(x, y):
    _len = math.sqrt(x * x + y * y)
    return _len

if __name__ == "__main__":
    # Managerオブジェクトの作成
    with Manager() as manager:
        # マネージャーからValueクラスを作成
        _yaw = manager.Value('i', 0)
        _pitch = manager.Value('i', 0)
        # サブプロセスの作成
        process_data_receive = Process(target=data_receiver, args=[_yaw, _pitch])
        process_mouse_move = Process(target=mouse_move, args=[_yaw, _pitch])
        # サブプロセスの開始
        process_data_receive.start()
        process_mouse_move.start()
        # サブプロセスの終了
        process_data_receive.join()
        process_mouse_move.join()
        print("process ended")
