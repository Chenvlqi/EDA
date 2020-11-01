import joblib
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.neighbors import KNeighborsClassifier


class MyKNN:
    def __init__(self, x_train, y_train, x_test, y_test, isJoblib=False):
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.isJoblib = isJoblib
        self.knn = KNeighborsClassifier(n_neighbors=2, weights='distance', algorithm='auto', leaf_size=30, p=1,
                                        metric='minkowski', metric_params=None, n_jobs=-1)

    def train(self):
        self.knn.fit(self.x_train, self.y_train)
        joblib.dump(self.knn, 'pkls/knn.pkl')

    def show(self):
        if self.isJoblib is True:
            self.knn = joblib.load('pkls/knn.pkl')
        self.y_pred = self.knn.predict(self.x_test)
        print(confusion_matrix(self.y_test, self.y_pred))
        print(classification_report(self.y_test, self.y_pred))

    def excute(self):
        if self.isJoblib is False:
            self.train()
        self.show()

    def predict(self):
        if self.isJoblib is True:
            self.knn = joblib.load('pkls/knn.pkl')
        self.y_pred = self.knn.predict(self.x_test)
        print(self.y_pred)

        with open('knn_out.txt', 'w') as out:
            for i in self.y_pred:
                out.write(i + '\n')



    def createpage(self,file):

        x= []
        with open(file,"r") as data:
            for i in data.readlines():
                i = i.split(',',4)
                del i[-1]
                #print (i)
                x.append(i)

        with open("predict.html", 'w+') as f:
            danger = 0
            count = 0
            f.write("<h3>针对{0}的分析结果</h3>".format(file))
            f.write("<table border='1'>")
            f.write("<tr>"
                    "<td>1</td><td>2</td><td>3</td><td>4</td><td>lable</td>"
                    "</tr>")
            for i in list(zip(x,self.y_pred)):
                count +=1
                f.write("<tr>")
                for y in i:
                    if (type(y).__name__ == 'list'):
                        for k in y:
                            f.write("<td>{}</td>".format(k))
                            #print(k)
                    else :
                        if y =='danger':
                            danger +=1
                        f.write("<td>{}</td>".format(y))
                f.write('</tr>')
            f.write("</table>")
            danger_able = float(danger/count)

            f.write("<p>The proportion of hazards is {}</p>".format(danger_able))