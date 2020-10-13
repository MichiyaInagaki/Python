import csv
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score

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

# incam，outcamで分類
for i in range(N):
    if key[i]==0:
        incam_yaw.append(yaw[i])
        incam_pitch.append(pitch[i])
        incam_force.append(force[i])
    elif key[i]==1:
        outcam_yaw.append(yaw[i])
        outcam_pitch.append(pitch[i])
        outcam_force.append(force[i])


# plot
fig = plt.figure(1)
ax = fig.add_subplot(1,1,1)
ax.scatter(incam_force,incam_yaw, c='blue', label='in camera')
ax.scatter(outcam_force,outcam_yaw, c='red', label='out of camera')
ax.set_xlabel('force')
ax.set_ylabel('yaw')
ax.grid(True)
ax.legend(loc='upper left')

# =============================================================================
# fig = plt.figure(2)
# ax = fig.add_subplot(1,1,1)
# ax.scatter(incam_force,incam_yaw, c='blue', label='in camera')
# ax.set_xlabel('force')
# ax.set_ylabel('yaw')
# ax.grid(True)
# ax.legend(loc='upper left')
# 
# fig = plt.figure(3)
# ax = fig.add_subplot(1,1,1)
# ax.scatter(outcam_force,outcam_yaw, c='red', label='out of camera')
# ax.set_xlabel('force')
# ax.set_ylabel('yaw')
# ax.grid(True)
# ax.legend(loc='upper left')
# =============================================================================


plt.show()