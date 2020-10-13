import BWT_class
from websocket_server import WebsocketServer
import time

jy_sensor =  BWT_class.BWT901("COM5")

def sign(x):
    val = 0
    if x>0:
        val = 1
    elif x<0:
        val = -1
    return val

def get_angle():
    roll, pitch, yaw = jy_sensor.getAngle2()
    yaw = yaw
    while abs(pitch)>180:
        pitch -= sign(pitch)*360
    while abs(yaw)>180:
        yaw -= sign(yaw)*360  
    return yaw, pitch

def new_client(client, server):
    print ("new_client:", client['address'])

def message_received(client, server, message):
    #受信
    print ("message_received:", message)    
    #データ処理
    yaw, pitch = get_angle()
    result = str(yaw) + ", " + str(pitch)
    print("send:", result)
    #送信
    #time.sleep(0.1)
    server.send_message(client, result.encode('utf-8'))


if __name__ == '__main__':
    server = WebsocketServer(port=5001, host='127.0.0.1')
    server.set_fn_new_client(new_client)
    server.set_fn_message_received(message_received)
    server.run_forever()
