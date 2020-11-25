#Oculusジャイロ軌道解析用

import csv
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# ファイル読込
data = np.loadtxt('C:/Users/inaga/Documents/My_folder/progress/最適ディスプレイ設計/Horizontal_exp1_Oculus/csv/watanabe_45.csv', delimiter=',')
N = len(data)                   #リストの長さ
condition_angle = data[:,0].astype(int)     #条件角度
trial_num = data[:,1]                       #試行回数
ajust_num = data[:,2]                       #調整角度
roll = data[:,3] 
pitch = data[:,4] 
yaw = data[:,5] 

# パラメータ
r = 30      #極座標のr
x = []
y = []
z = []
x0 = []
y0 = []
z0 = []
x10 = []
y10 = []
z10 = []
x20 = []
y20 = []
z20 = []
x30 = []
y30 = []
z30 = []
x40 = []
y40 = []
z40 = []
x50 = []
y50 = []
z50 = []

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

print(pitch)

#分類
for i in range(N):
    if condition_angle[i]==0:
        x0.append(x[i])
        y0.append(y[i])
        z0.append(z[i])
    elif condition_angle[i]==10:
        x10.append(x[i])
        y10.append(y[i])
        z10.append(z[i])
    elif condition_angle[i]==20:
        x20.append(x[i])
        y20.append(y[i])
        z20.append(z[i])
    elif condition_angle[i]==30:
        x30.append(x[i])
        y30.append(y[i])
        z30.append(z[i])
    elif condition_angle[i]==40:
        x40.append(x[i])
        y40.append(y[i])
        z40.append(z[i])
    elif condition_angle[i]==50:
        x50.append(x[i])
        y50.append(y[i])
        z50.append(z[i])

# プロット
fig = plt.figure()
ax = Axes3D(fig)
# X,Y,Z軸にラベルを設定
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
#描画
ax.plot(x0,y0,z0,color="k",marker="o",linestyle='None')
ax.plot(x10,y10,z10,color="r",marker="o",linestyle='None')
ax.plot(x20,y20,z20,color="g",marker="o",linestyle='None')
ax.plot(x30,y30,z30,color="b",marker="o",linestyle='None')
ax.plot(x40,y40,z40,color="c",marker="o",linestyle='None')
ax.plot(x50,y50,z50,color="m",marker="o",linestyle='None')
#表示
plt.show()
