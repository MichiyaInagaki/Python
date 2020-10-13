import csv
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np

# ファイル読込
data = np.loadtxt('C:/Users/inaga/OneDrive/デスクトップ/exe/csv/protect/inagaki_F3.csv', delimiter=',')
N=len(data)                     #リストの長さ
key = data[:,0].astype(int)     #キーボード番号
yaw = data[:,1]                 #yawの値
pitch = data[:,2]               #pitchの値
force = -data[:,3]              #forceの値（空気圧）

# プロット用リスト
ns_yaw = []         #押さない or スペース
ns_pitch = []
ns_force = []
non_yaw = []        #押さない
non_pitch = []
non_force = []
space_yaw = []      #スペースキー
space_pitch = []
space_force = []
left_yaw = []       #左キー
left_pitch = []
left_force =[]
right_yaw = []      #右キー
right_pitch = []
right_force =[]

# キーボード番号ごとにデータを分類
for i in range(N):
    if key[i]==0 or key[i]==1:
        ns_yaw.append(yaw[i])
        ns_pitch.append(pitch[i])
        ns_force.append(force[i])
    if key[i]==0:
        non_yaw.append(yaw[i])
        non_pitch.append(pitch[i])
        non_force.append(force[i])
    elif key[i]==1:
        space_yaw.append(yaw[i])
        space_pitch.append(pitch[i])
        space_force.append(force[i])
    elif key[i]==2:
        left_yaw.append(yaw[i])
        left_pitch.append(pitch[i])
        left_force.append(force[i])
    elif key[i]==3:
        right_yaw.append(yaw[i])
        right_pitch.append(pitch[i])
        right_force.append(force[i])

# プロット
fig = plt.figure(1)
ax = fig.add_subplot(1,1,1)
#plt.hist([non_yaw, space_yaw, left_yaw, right_yaw], bins=10, color=['red', 'blue', 'green', 'yellow'], label=['non', 'space', 'left', 'right'])    
ax.hist(ns_yaw, bins=30, color='red', alpha=0.5, label=['no press or press space'])
ax.hist(right_yaw, bins=30, color='blue',alpha=0.5, label=['press right'])
ax.set_title('gyro yaw')
ax.set_xlabel('degree')
ax.set_ylabel('freq')
ax.legend(loc='upper left')
#ax.set_xlim(-30,30)

fig = plt.figure(2)
ax = fig.add_subplot(1,1,1)
#plt.hist([non_force, space_force, left_force, right_force], bins=10, color=['red', 'blue', 'green', 'yellow'], label=['non', 'space', 'left', 'right'])    
ax.hist(ns_force, bins=30, color='red', alpha=0.5, label=['no press or press space'])
ax.hist(right_force, bins=30, color='blue',alpha=0.5, label=['press right'])
ax.set_title('airpress force')
ax.set_xlabel('force')
ax.set_ylabel('freq')
ax.legend(loc='upper left')
plt.show()