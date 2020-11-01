import joblib
from sklearn import svm
from sklearn.metrics import confusion_matrix, classification_report
import warnings

class mySVC:

    def __init__(self, x_train, y_train, x_test, y_test, isJoblib=False):
        self.study = svm.SVC(kernel="poly")
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test
        self.isJoblib = isJoblib

    def train(self):
        self.study.fit(self.x_train, self.y_train)
        joblib.dump(self.study, 'pkls/svc.pkl')

    def show(self):
        if self.isJoblib is True:
            self.study = joblib.load('pkls/svc.pkl')
        y_pred = self.study.predict(self.x_test)
        print(confusion_matrix(self.y_test, y_pred))
        print(classification_report(self.y_test, y_pred))
        # print(y_pred)

    def excute(self):
        if self.isJoblib is False:
            self.train()
        self.show()

    def predict(self):
        if self.isJoblib is True:
            self.study = joblib.load('pkls/svc.pkl')
        y_pred = self.study.predict(self.x_test)
        print(y_pred)
        with open('svc_out.txt', 'w') as out:
            for i in y_pred:
                out.write(i+'\n')