#Ambient sensing 解析用

import csv
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np

# ファイル読込
data = np.loadtxt('C:/Users/inaga/OneDrive/デスクトップ/exe/csv/ambient/protect/test_reguler.csv', delimiter=',')
N=len(data)                     #リストの長さ
key = data[:,0].astype(int)     #incam：0，outcam：1
yaw = data[:,1]                 #yawの値
pitch = data[:,2]               #pitchの値
force = -data[:,3]              #forceの値（空気圧）

# プロット用リスト
incam_yaw = []      #incamのとき
incam_pitch = []
incam_force = []
outcam_yaw = []        #outcamのとき
outcam_pitch = []
outcam_force = []

# incam, outcamでデータを分類
for i in range(N):
    if key[i]==0:
        incam_yaw.append(yaw[i])
        incam_pitch.append(pitch[i])
        incam_force.append(force[i])
    elif key[i]==1:
        outcam_yaw.append(yaw[i])
        outcam_pitch.append(pitch[i])
        outcam_force.append(force[i])

# プロット
fig = plt.figure(1)
ax = fig.add_subplot(1,1,1)
ax.hist(incam_yaw, bins=30, color='blue', alpha=0.5, label=['in camera'])
ax.hist(outcam_yaw, bins=30, color='red',alpha=0.5, label=['out of camera'])
ax.set_title('gyro yaw')
ax.set_xlabel('degree')
ax.set_ylabel('freq')
ax.legend(loc='upper left')
#ax.set_xlim(-30,30)

fig = plt.figure(2)
ax = fig.add_subplot(1,1,1)
ax.hist(incam_force, bins=30, color='blue', alpha=0.5, label=['in camera'])
ax.hist(outcam_force, bins=30, color='red',alpha=0.5, label=['out of camera'])
ax.set_title('airpress force')
ax.set_xlabel('force')
ax.set_ylabel('freq')
ax.legend(loc='upper left')
plt.show()