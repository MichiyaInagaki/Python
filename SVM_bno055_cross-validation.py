import numpy as np
import matplotlib.pyplot as pyplot
from sklearn import svm
from sklearn.metrics import confusion_matrix
from mlxtend.plotting import plot_decision_regions
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold


# 教師データの読み込み
data = np.loadtxt('C:/Users/inaga/OneDrive/ドキュメント/Python_files/csv/bno055_data.csv', delimiter=',')
y = data[:,0].astype(int)   #正解ラベル
x = data[:,1:3]             #特徴ベクトル


#---ホールドアウト法---#
# 訓練用データセットとテスト用データセットへの分割
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)

# 学習モデルの設定
#clf = svm.SVC(kernel='linear')
clf = svm.SVC(gamma="auto")
# 訓練用データセットを学習させる
clf.fit(x_train, y_train)

# 学習したデータと比較して推測する
#print('予測した結果',clf.predict(test_x))
print('予測した結果の正解率',clf.score(x_test, y_test))


#---クロスバリデーション法---#
# データのシャッフル
kf = KFold(n_splits=4, shuffle=True, random_state=0)
# クロスバリデーション関数（分割とスコアの平均化を自動でやってくれる），cvは分割数
scores = cross_val_score(clf, x, y, cv=kf)
# 各分割におけるスコア
print('Cross-Validation scores: {}'.format(scores))
# スコアの平均値
print('Average score: {}'.format(np.mean(scores)))




# プロット
#pyplot.style.use('ggplot')
#plot_decision_regions(x_train, y_train, clf=clf,  res=0.02)
#pyplot.show()