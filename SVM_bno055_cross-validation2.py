import numpy as np
import matplotlib.pyplot as pyplot
from sklearn import svm
from sklearn.metrics import confusion_matrix
from mlxtend.plotting import plot_decision_regions
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold

# ４つのデータに対してクロスバリデーション法を実施する

# 教師データの読み込み
"""
for i in range(4):
    input_pass = 'C:/Users/inaga/OneDrive/ドキュメント/Python_files/csv/bno055/bno055_data_v' + str(i+1) + '.csv'     #ファイルパス
    input_data = np.loadtxt(input_pass, delimiter=',')
"""

data1 = np.loadtxt('C:/Users/inaga/OneDrive/ドキュメント/Python_files/csv/bno055/bno055_data_v1.csv', delimiter=',')
x1 = data1[:,1:3]             #特徴ベクトル
y1 = data1[:,0].astype(int)   #正解ラベル

data2 = np.loadtxt('C:/Users/inaga/OneDrive/ドキュメント/Python_files/csv/bno055/bno055_data_v2.csv', delimiter=',')
x2 = data2[:,1:3]             #特徴ベクトル
y2 = data2[:,0].astype(int)   #正解ラベル

data3 = np.loadtxt('C:/Users/inaga/OneDrive/ドキュメント/Python_files/csv/bno055/bno055_data_v3.csv', delimiter=',')
x3 = data3[:,1:3]             #特徴ベクトル
y3 = data3[:,0].astype(int)   #正解ラベル

data4 = np.loadtxt('C:/Users/inaga/OneDrive/ドキュメント/Python_files/csv/bno055/bno055_data_v4.csv', delimiter=',')
x4 = data4[:,1:3]             #特徴ベクトル
y4 = data4[:,0].astype(int)   #正解ラベル


# 学習モデルの設定
#clf = svm.SVC(kernel='linear')
#clf = svm.SVC(gamma="auto")
# 学習モデルの設定
clf1 = svm.SVC(C=10, kernel='rbf', gamma=0.1)
clf2 = svm.SVC(C=10, kernel='rbf', gamma=0.1)
clf3 = svm.SVC(C=10, kernel='rbf', gamma=0.1)
clf4 = svm.SVC(C=10, kernel='rbf', gamma=0.1)

# クロスバリデーション
temp = 0
# 1がテストデータ，2,3,4が学習データ
x_test1 = x1
y_test1 = y1
x_train1 = np.vstack((x2,x3,x4))
y_train1 = np.hstack((y2,y3,y4))
clf1.fit(x_train1, y_train1)
score = clf1.score(x_test1, y_test1)
print("score1:", score)
temp += score

# 2がテストデータ，1,3,4が学習データ
x_test2 = x2
y_test2 = y2
x_train2 = np.vstack((x1,x3,x4))
y_train2 = np.hstack((y1,y3,y4))
clf2.fit(x_train2, y_train2)
score = clf2.score(x_test2, y_test2)
print("score2:", score)
temp += score

# 3がテストデータ，1,2,4が学習データ
x_test3 = x3
y_test3 = y3
x_train3 = np.vstack((x1,x2,x4))
y_train3 = np.hstack((y1,y2,y4))
clf3.fit(x_train3, y_train3)
score = clf3.score(x_test3, y_test3)
print("score3:", score)
temp += score

# 4がテストデータ，1,2,3が学習データ
x_test4 = x4
y_test4 = y4
x_train4 = np.vstack((x1,x2,x3))
y_train4 = np.hstack((y1,y2,y3))
clf4.fit(x_train4, y_train4)
score = clf4.score(x_test4, y_test4)
print("score4:", score)
temp += score

#平均値
print("average score",temp/4.0)


