import csv
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np

# ファイルパス
# input_pass = 'C:/Users/inaga/OneDrive/デスクトップ/exe/csv/accel/hoge/'
# output_pass = 'C:/Users/inaga/OneDrive/ドキュメント/My_folder/progress/accel/hoge/'
input_pass = 'C:/Users/inaga/OneDrive/デスクトップ/exe/csv/accel/yoshida/'
output_pass = 'C:/Users/inaga/OneDrive/ドキュメント/My_folder/progress/accel/yoshida/'
str_num = '315'

# ファイル読込
data = np.loadtxt(input_pass + str_num + '.csv', delimiter=',')
N=len(data)                     #リストの長さ
time = data[:,0]                #経過時間
yaw = data[:,1]                 #yawの値
pitch = data[:,2]               #pitchの値
force = -data[:,3]              #forceの値（空気圧）
velocity = data[:,4]            #角速度（yaw）
accel = data[:,5]               #角加速度（yaw）


# plot ------------------------------------------
# angle + force 散布図
fig = plt.figure(1)
plt.scatter(force, yaw, c=time, cmap='plasma')
plt.title("Angle + Force")
plt.xlabel("force")
plt.ylabel("angle")
plt.colorbar()
plt.grid(True)
#直線y=0.4x
# x = np.arange(-100, 100)
# y = 0.4*x
# plt.plot(x, y, c='indianred')
plt.savefig(output_pass + str_num + '_AF_S.png')

# angle + force 折れ線
fig = plt.figure(2)
p1 = plt.plot(time, yaw)
p2 = plt.plot(time, force)
plt.title("Angle + Force")
plt.xlabel("time[s]")
plt.legend((p1[0], p2[0]), ("Angle", "Force"), loc=2)
plt.grid(True)
plt.savefig(output_pass + str_num + '_AF.png')

# angle + velocity 折れ線
fig = plt.figure(3)
p1 = plt.plot(time, yaw)
p2 = plt.plot(time, velocity)
plt.title("Angle + Velocity")
plt.xlabel("time[s]")
plt.legend((p1[0], p2[0]), ("Angle", "Velocity"), loc=2)
plt.grid(True)
plt.savefig(output_pass + str_num + '_AV.png')

# angle + accel 折れ線
fig = plt.figure(4)
p1 = plt.plot(time, yaw)
p2 = plt.plot(time, velocity)
p3 = plt.plot(time, accel)
plt.title("Angle + Velocity + Accel")
plt.xlabel("time[s]")
plt.legend((p1[0], p2[0], p3[0]), ("Angle", "Velocity", "Accel"), loc=2)
plt.grid(True)
plt.savefig(output_pass + str_num + '_AVA.png')

plt.show()