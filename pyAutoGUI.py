import pyautogui
import BWT_class

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

if __name__ == "__main__":

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
        # 角度から座標への変換    
        x_pos, y_pos = angle_to_pos(yaw, pitch)
        #print(x_pos, y_pos)
        print(pyautogui.position(), yaw, pitch)
