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
data = np.loadtxt('C:/Users/inaga/OneDrive/デスクトップ/exe/csv/angle/protect/new_cal2.csv', delimiter=',')
N=len(data)                     #リストの長さ
key = data[:,0].astype(int)     #キーボード番号
yaw = data[:,1]                 #yawの値
pitch = data[:,2]               #pitchの値
force = -data[:,3]              #forceの値（空気圧）

# 分類用リスト
to_right = []
from_right = []
to_left = []
from_left = []
to_right_f = []
from_right_f = []
to_left_f = []
from_left_f = []
#
y_obs = []    #実測値：ジャイロyaw
y_pred = []   #予測値：y=a*空気圧

#y=axの近似式を求める
a = lr_1(force, yaw)
print(a)
y_ = a*force

for i in range(N-1):
    y_obs.append(yaw[i])
    y_pred.append(a*force[i])
    if yaw[i] >= 0 and yaw[i+1] > yaw[i]:   #中央から右
        to_right.append(yaw[i])
        to_right_f.append(force[i])
    elif yaw[i] >= 0 and yaw[i] > yaw[i+1]: #右から中央
        from_right.append(yaw[i])
        from_right_f.append(force[i])
    elif yaw[i] < 0 and yaw[i] > yaw[i+1]:  #中央から左
        to_left.append(yaw[i])
        to_left_f.append(force[i])
    elif yaw[i] < 0 and yaw[i+1] > yaw[i]:  #左から中央
        from_left.append(yaw[i])
        from_left_f.append(force[i])

'''
for i in range(N-1):
    if force[i] >= 0 and force[i+1] > force[i]:   #中央から右
        to_right.append(yaw[i])
        to_right_f.append(force[i])
    elif force[i] >= 0 and force[i] > force[i+1]: #右から中央
        from_right.append(yaw[i])
        from_right_f.append(force[i])
    elif force[i] < 0 and force[i] > force[i+1]:  #中央から左
        to_left.append(yaw[i])
        to_left_f.append(force[i])
    elif force[i] < 0 and force[i+1] > force[i]:  #左から中央
        from_left.append(yaw[i])
        from_left_f.append(force[i])
'''

print(len(to_right),len(from_right),len(to_left),len(from_left_f))



#決定係数の計算
r2 = r2_score(y_obs, y_pred)
print(r2)

# plot
fig = plt.figure(1)
ax = fig.add_subplot(1,1,1)
#ax.scatter(force, yaw)
ax.scatter(to_right_f,to_right, c='red', label='center to right')
ax.scatter(from_right_f,from_right, c='blue', label='center from right')
ax.scatter(to_left_f,to_left, c='green', label='center to left')
ax.scatter(from_left_f,from_left, c='yellow', label='center from left')
ax.set_xlabel('force')
ax.set_ylabel('yaw')
ax.grid(True)
ax.legend(loc='upper left')


#方向で分類
to_right.extend(from_left)
to_right_f.extend(from_left_f)
to_left.extend(from_right)
to_left_f.extend(from_right_f)
#
fig = plt.figure(2)
ax = fig.add_subplot(1,1,1)
ax.scatter(to_right_f,to_right, c='red', label='left to right')
ax.scatter(to_left_f,to_left, c='blue', label='right to left')
ax.set_xlabel('force')
ax.set_ylabel('yaw')
ax.grid(True)
ax.legend(loc='upper left')
#y=ax近似
plt.plot(force, y_, c='indianred')

plt.show()