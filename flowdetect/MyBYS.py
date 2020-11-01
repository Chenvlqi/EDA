# -*- coding:utf-8 -*-
# author: dzhhey

import joblib
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.naive_bayes import BernoulliNB


class MyBYS:
    def __init__(self, x_train, y_train, x_test, y_test, isJoblib=False):
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.isJoblib = isJoblib
        self.bys = BernoulliNB(alpha=1.0, binarize=0.0, class_prior=None, fit_prior=True)

    def train(self):
        self.bys.fit(self.x_train, self.y_train)
        joblib.dump(self.bys, 'pkls/bys.pkl')

    def show(self):
        if self.isJoblib is True:
            self.bys = joblib.load('pkls/bys.pkl')
        y_pred = self.bys.predict(self.x_test)
        print(confusion_matrix(self.y_test, y_pred))
        print(classification_report(self.y_test, y_pred))

    def excute(self):
        if self.isJoblib is False:
            self.train()
        self.show()

    def predict(self):
        if self.isJoblib is True:
            self.bys = joblib.load('pkls/bys.pkl')
        y_pred = self.bys.predict(self.x_test)
        print(y_pred)
        with open('bys_out.txt', 'w') as out:
            for i in y_pred:
                out.write(i + '\n')
