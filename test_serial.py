import time
import serial
import pyautogui

#serport = '/dev/tty.SLAB_USBtoUART'
ser = serial.Serial('COM5', 57600, bytesize = serial.EIGHTBITS, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE)

ser.dtr = True #reset
time.sleep(0.1)
ser.dtr = False

time.sleep(0.1)
ser.write('m'.encode('utf-8'))
ser.read() # dummy recv 0xff
time.sleep(0.1)

try:
	data = [ 0, 0, 0, 0 ] # 10bit date: CH1, CH4, CH2, CH3
	while True:
		ser.write(0x6d.to_bytes(1, 'big'))
		ser.flush()
		sum = 0
		for i in range(4):
			n = int.from_bytes(ser.read(2), 'big')
			data[i] = n
			sum += n
		print(data)

		# drive Shokkaku pot!
		if sum / 4 > 40:
			pyautogui.click()
		else:
			dx = (data[3] - data[0]) / 2
			dy = (data[1] - data[2]) / 2
			dx = dx * abs(dx)
			dy = dy * abs(dy)
			pyautogui.move(dx, dy)
		
except KeyboardInterrupt:
	ser.close()