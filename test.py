import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

#データの読み込み
dataset = load_breast_cancer()
X, y = dataset.data, dataset.target

# データセットを学習用と検証用に分割する
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=True, random_state=0, stratify=y)

# 学習
svc = SVC(kernel='linear', random_state=0)
svc.fit(X_train, y_train)

# 評価
y_train_pred = svc.predict(X_train)
train_acc = accuracy_score(y_train, y_train_pred)
print('train score :',train_acc)
 
y_test_pred = svc.predict(X_test)
test_acc = accuracy_score(y_test, y_test_pred)
print('test score :',test_acc)