import csv
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score

#y=axで線形回帰
def lr_1(x, y):
    a = np.dot(x, y)/(x**2).sum()
    return a

# ファイル読込
limit_angle = 92.57456
#limit_angle_gyro = -39.15
data = np.loadtxt('C:/Users/inaga/OneDrive/デスクトップ/exe/csv/shoulder/test.csv', delimiter=',')
N=len(data)                     #リストの長さ
yaw = -data[:,0]                #yawの値
pitch = data[:,1]               #pitchの値
force = -data[:,2]              #forceの値（空気圧）
phi = data[:,3]                 #蝶々位置

# 分類用リスト
in_yaw = []
out_yaw = []
in_force = []
out_force = []
in_phi = []
out_phi = []

for i in range(N-1):
    if phi[i] < limit_angle:   #限界角まで
        in_yaw.append(yaw[i])
        in_force.append(force[i])
        in_phi.append(phi[i])
    else:
        out_yaw.append(yaw[i])
        out_force.append(force[i])
        out_phi.append(phi[i])

# plot
fig = plt.figure(1)
plt.title("Position + Force")
ax = fig.add_subplot(1,1,1)
#ax.scatter(force, yaw)
ax.scatter(in_phi,in_force, c='blue', label='in limit angle')
ax.scatter(out_phi,out_force, c='red', label='out limit angle')
ax.set_xlabel('position')
ax.set_ylabel('force')
ax.grid(True)
ax.legend(loc='upper left')

fig = plt.figure(2)
plt.title("Position + Angle")
ax = fig.add_subplot(1,1,1)
#ax.scatter(force, yaw)
ax.scatter(in_phi,in_yaw, c='blue', label='in limit angle')
ax.scatter(out_phi,out_yaw, c='red', label='out limit angle')
ax.set_xlabel('position')
ax.set_ylabel('yaw')
ax.grid(True)
ax.legend(loc='upper left')

fig = plt.figure(3)
plt.title("Angle + Force")
ax = fig.add_subplot(1,1,1)
#ax.scatter(force, yaw)
ax.scatter(in_force,in_yaw, c='blue', label='in limit angle')
ax.scatter(out_force,out_yaw, c='red', label='out limit angle')
ax.set_xlabel('force')
ax.set_ylabel('angle')
ax.grid(True)
ax.legend(loc='upper left')

plt.show()