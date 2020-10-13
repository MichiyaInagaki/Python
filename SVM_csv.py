import numpy as np
import matplotlib.pyplot as pyplot
from sklearn import svm
from sklearn.metrics import confusion_matrix
from mlxtend.plotting import plot_decision_regions

# 教師データの読み込み
data = np.loadtxt('C:/Users/inaga/OneDrive/ドキュメント/Python_files/csv/data.csv', delimiter=',')
y = data[:,0].astype(int)   #正解ラベル
x = data[:,1:3]             #特徴ベクトル

# 学習モデルの設定
clf = svm.SVC(kernel='linear')
#clf = svm.SVC(gamma="auto")
# 学習させる
clf.fit(x, y)

# テストデータの読み込み
data_test = np.loadtxt('C:/Users/inaga/OneDrive/ドキュメント/Python_files/csv/data_test.csv', delimiter=',') 
test_y = data_test[:,0].astype(int)     #正解ラベル
test_x = data_test[:,1:3]               #特徴ベクトル

# 学習したデータと比較して推測する
print('テストデータの正解ラベル',test_y)
print('予測した結果',clf.predict(test_x))
print('予測した結果の正解率',clf.score(test_x, test_y))

# プロット
pyplot.style.use('ggplot')
# 教師データとテストデータの結合
x_bind = np.vstack((test_x,x))
y_bind = np.hstack((test_y,y))
# 境界線のプロット
plot_decision_regions(x_bind, y_bind, clf=clf,  res=0.02)
pyplot.show()