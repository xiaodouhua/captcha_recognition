# -*- coding: utf-8 -*-
"""
Created on Tue Jul 04 18:10:50 2017

@author: dou
"""
from pylab import array
import numpy as np
import os
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.externals import joblib
from time import time
from sklearn.metrics import hamming_loss


def load_data(path):
    '''
    每个文件夹下是一种图片
    :param path:种类文件夹路径
    :return: 图片路径列表和标签列表
    '''

    img_pathes = []
    labels = []
    for path, dirs, files in os.walk(path):
        img_pathes.extend([os.path.join(path, file) for file in files])
        # sprint path
        if len(files) > 0:
            labels.extend([path.split('/')[-1]] * len(files))
    # print len(img_pathes),img_pathes
    # print len(labels),labels
    return img_pathes, labels


a, b = load_data('D:\py\EdiScrapy\captcha_recognition\dataset/')
label = np.array(b)
data = []
for img in a:
    im = np.array(array(Image.open(img)))
    # im=im.reshape((-1,1))
    data.append(im)
data = np.array(data)
data = data.reshape((910, -1))
X_train, X_test, y_train, y_test = train_test_split(
    data, label, test_size=0.25, random_state=42)

n_components = 50
t0 = time()
print("start pca")
pca = PCA(n_components=n_components, svd_solver='randomized',
          whiten=True).fit(X_train)
print("done in %0.3fs" % (time() - t0))
joblib.dump(pca, 'pca.model')

t0 = time()
X_train_pca = pca.transform(X_train)
X_test_pca = pca.transform(X_test)

###############################################################################
# Train a SVM classification model

print("Fitting the classifier to the training set")
t0 = time()
param_grid = {'C': [1e3, 5e3, 1e4, 5e4, 1e5],
              'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1], }
clf = GridSearchCV(SVC(kernel='rbf', class_weight='balanced'), param_grid)
clf = clf.fit(X_train_pca, y_train)
print("done in %0.3fs" % (time() - t0))
# print("Best estimator found by grid search:")
# print(clf.best_estimator_)
joblib.dump(clf, 'clf.model')

###############################################################################
# Quantitative evaluation of the model quality on the test set

print("Predicting data on the test set")
t0 = time()
y_pred = clf.predict(X_test_pca)
print("done in %0.3fs" % (time() - t0))

# print(classification_report(y_test, y_pred))
# print(confusion_matrix(y_test, y_pred))
print(hamming_loss(y_test, y_pred))
