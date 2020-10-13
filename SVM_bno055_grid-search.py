import numpy as np
import matplotlib.pyplot as pyplot
from sklearn import svm
from sklearn.metrics import confusion_matrix
from mlxtend.plotting import plot_decision_regions
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV


# 教師データの読み込み
data = np.loadtxt('C:/Users/inaga/OneDrive/ドキュメント/Python_files/csv/bno055_data.csv', delimiter=',')
y = data[:,0].astype(int)   #正解ラベル
x = data[:,1:3]             #特徴ベクトル

# 学習モデルの設定
clf = svm.SVC(kernel='rbf')
# データのシャッフル
kf = KFold(n_splits=4, shuffle=True, random_state=0)
# パラメータの候補を dict 型で指定
param_grid = {'C': [0.001, 0.01, 0.1, 1, 10, 100],  'gamma' : [0.001, 0.01, 0.1, 1, 10, 100]}
# validation set は GridSearchCV が自動で作成してくれるため，
# training set と test set の分割のみを実行すればよい
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)
# グリッドサーチ
grid_search = GridSearchCV(clf, param_grid, cv=kf)
# fit 関数を呼ぶことで交差検証とグリッドサーチがどちらも実行される
grid_search.fit(x_train, y_train)

print('Test set score: {}'.format(grid_search.score(x_test, y_test)))	#テストデータのスコア
print('Best parameters: {}'.format(grid_search.best_params_))	#最良パラメタ
print('Best cross-validation: {}'.format(grid_search.best_score_))	#最良スコア


# プロット
#pyplot.style.use('ggplot')
#plot_decision_regions(x_train, y_train, clf=clf,  res=0.02)
#pyplot.show()