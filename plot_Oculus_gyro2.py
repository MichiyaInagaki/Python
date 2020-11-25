#Oculusジャイロ軌道解析用

import csv
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# ファイル読込
data = np.loadtxt('C:/Users/inaga/Documents/My_folder/progress/最適ディスプレイ設計/Horizontal_exp1_3/csv/Data2.csv', delimiter=',')
N = len(data)                   #リストの長さ
timing = data[:,0]      #計測時間
roll = data[:,1]        #360度表記
pitch = data[:,2] 
yaw = data[:,3] 
_roll = data[:,4]       #180度表記
_pitch = data[:,5] 
_yaw = data[:,6] 

# パラメータ
r = 10      #極座標のr
x = []
y = []
z = []

#yawゼロ合わせ
#yaw = yaw - yaw[0]

# 極座標用に回転角を変換
for i in range(N):
    if yaw[i]<90:
        yaw[i] = 90 - yaw[i]
    else:
        yaw[i] = 360 - yaw[i] + 90
    if pitch[i] > 270:
        pitch[i] = pitch[i] - 270
    else:
        pitch[i] = pitch[i] + 90

# 極座標計算
x = r * np.sin(np.deg2rad(pitch)) * np.cos(np.deg2rad(yaw))
y = r * np.sin(np.deg2rad(pitch)) * np.sin(np.deg2rad(yaw))
z = r * np.cos(np.deg2rad(pitch))

# プロット
# 時系列データ
fig = plt.figure(1)
ax = fig.add_subplot(1,1,1)
ax.scatter(timing,_roll, c='blue', label='roll')
ax.scatter(timing,_pitch, c='red', label='pitch')
ax.scatter(timing,_yaw, c='green', label='yaw')
ax.set_xlabel('time[s]')
ax.set_ylabel('angle[deg]')
ax.grid(True)
ax.legend(loc='upper left')

# 軌道データ
fig = plt.figure(2)
ax = Axes3D(fig)
# X,Y,Z軸にラベルを設定
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
#描画
ax.plot(x,y,z,marker="o",linestyle='None')
#表示
plt.show()
