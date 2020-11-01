# -*- coding:utf-8 -*-
# author: dzhhey

import joblib
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.neural_network import MLPClassifier


class MyMLP:
    def __init__(self, x_train, y_train, x_test, y_test, isJoblib=False):
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.isJoblib = isJoblib
        self.mlp = MLPClassifier(solver='lbfgs', alpha=1e-5,
                                 hidden_layer_sizes=(5, 2), random_state=1)

    def train(self):
        self.mlp.fit(self.x_train, self.y_train)
        joblib.dump(self.mlp, 'pkls/mlp.pkl')

    def show(self):
        if self.isJoblib is True:
            self.mlp = joblib.load('pkls/mlp.pkl')
        y_pred = self.mlp.predict(self.x_test)
        print(confusion_matrix(self.y_test, y_pred))
        print(classification_report(self.y_test, y_pred))

    def excute(self):
        if self.isJoblib is False:
            self.train()
        self.show()

    def predict(self):
        if self.isJoblib is True:
            self.mlp = joblib.load('pkls/mlp.pkl')
        y_pred = self.mlp.predict(self.x_test)
        print(y_pred)
        with open('mlp_out.txt', 'w') as out:
            for i in y_pred:
                out.write(i + '\n')
