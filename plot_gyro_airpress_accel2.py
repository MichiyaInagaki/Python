import csv
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np

# ファイルパス
# input_pass = 'C:/Users/inaga/OneDrive/デスクトップ/exe/csv/accel/hoge/reguler.csv'
# output_pass = 'C:/Users/inaga/OneDrive/ドキュメント/My_folder/progress/accel/hoge/reguler'
input_pass = 'C:/Users/inaga/OneDrive/デスクトップ/exe/csv/accel/yoshida/reguler.csv'
output_pass = 'C:/Users/inaga/OneDrive/ドキュメント/My_folder/progress/accel/yoshida/reguler'

# ファイル読込
data = np.loadtxt(input_pass, delimiter=',')
N=len(data)                     #リストの長さ
time = data[:,0]                #経過時間
key = data[:,1].astype(int)     #キーボード番号
yaw = data[:,2]                 #yawの値
pitch = data[:,3]               #pitchの値
force = -data[:,4]              #forceの値（空気圧）
velocity = data[:,5]            #角速度（yaw）
accel = data[:,6]               #角加速度（yaw）

# プロット用リスト
incam_time = []         #incamのとき
incam_yaw = []      
incam_pitch = []
incam_force = []
incam_velocity = []
incam_accel = []
outcam_time = []        #outcamのとき
outcam_yaw = []        
outcam_pitch = []
outcam_force = []
outcam_velocity = []
outcam_accel = []

incam_len = len(incam_time)
outcam_len = len(outcam_time)

# incam，outcamで分類
for i in range(N):
    if key[i]==0:
        incam_time.append(time[i])
        incam_yaw.append(yaw[i])
        incam_pitch.append(pitch[i])
        incam_force.append(force[i])
        incam_velocity.append(velocity[i])
        incam_accel.append(accel[i])
    elif key[i]==1:
        outcam_time.append(time[i])
        outcam_yaw.append(yaw[i])
        outcam_pitch.append(pitch[i])
        outcam_force.append(force[i])
        outcam_velocity.append(velocity[i])
        outcam_accel.append(accel[i])

# outcamの時間範囲を求める
for i in range(N):
    if time[i]<25:
        if key[i]==1:
            min_time1 = time[i]
            break

for i in range(N):
    if time[i]>25:
        if key[i]==1:
            min_time2 = time[i]
            break

for i in range(N):
    if time[i]<25:
        if key[i]==1:
            max_time1 = time[i]
    else:
        if key[i]==1:
            max_time2 = time[i]

# plot ------------------------------------------
# angle + force 散布図
fig = plt.figure(1)
ax = fig.add_subplot(1,1,1)
ax.scatter(incam_force,incam_yaw, c='blue', label='in camera')
ax.scatter(outcam_force,outcam_yaw, c='red', label='out of camera')
ax.set_xlabel('force')
ax.set_ylabel('yaw')
ax.grid(True)
ax.legend(loc='upper left')
#直線y=0.4x
# x = np.arange(-100, 100)
# y = 0.4*x
# plt.plot(x, y, c='indianred')
plt.savefig(output_pass + '_AF_S.png')


# angle + force 折れ線
fig = plt.figure(2)
ax = fig.add_subplot(111)
p1 = plt.plot(time, yaw)
p2 = plt.plot(time, force)
plt.title("Angle + Force")
plt.xlabel("time[s]")
plt.legend((p1[0], p2[0]), ("Angle", "Force"), loc=2)
plt.grid(True)
ax.axvspan(min_time1, max_time1, color = "0.9")
ax.axvspan(min_time2, max_time2, color = "0.9")
plt.savefig(output_pass + '_AF.png')

# angle + velocity 折れ線
fig = plt.figure(3)
ax = fig.add_subplot(111)
p1 = plt.plot(time, yaw)
p2 = plt.plot(time, velocity)
plt.title("Angle + Velocity")
plt.xlabel("time[s]")
plt.legend((p1[0], p2[0]), ("Angle", "Velocity"), loc=2)
plt.grid(True)
ax.axvspan(min_time1, max_time1, color = "0.9")
ax.axvspan(min_time2, max_time2, color = "0.9")
plt.savefig(output_pass + '_AV.png')

# angle + accel 折れ線
fig = plt.figure(4)
ax = fig.add_subplot(111)
p1 = plt.plot(time, yaw)
p2 = plt.plot(time, velocity)
p3 = plt.plot(time, accel)
plt.title("Angle + Velocity + Accel")
plt.xlabel("time[s]")
plt.legend((p1[0], p2[0], p3[0]), ("Angle", "Velocity", "Accel"), loc=2)
plt.grid(True)
ax.axvspan(min_time1, max_time1, color = "0.9")
ax.axvspan(min_time2, max_time2, color = "0.9")
plt.savefig(output_pass + '_AVA.png')

plt.show()