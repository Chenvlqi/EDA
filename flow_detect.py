import time
import pandas as pd
from sklearn.model_selection import train_test_split
from flowdetect import MyKNN, mySVC, MyLogiRe, myRf, MyBYS, MyMLP, myVoting, myStacking, vis




print('------------------Welcome--------------------')
while (True):
    print('选择要进行的操作：')
    print('\t1.训练模型')
    print('\t2.用已有模型进行测试')
    print('\t3.预测流量类型')
    print('\tany other.退出')
    choice = int(input())


    print('请选择数据集：')
    file_path = str(input())
    file = pd.read_csv(file_path)

    print('选择要使用的模型：')
    print('\t1.KNN算法')
    print('\t2.支持向量机算法')
    print('\t3.逻辑回归算法')
    print('\t4.随机森林算法')
    print('\t5.贝叶斯算法')
    print('\t6.多层感知器算法')
    print('\t7.投票器')
    print('\t8.堆叠')

    choice2 = int(input())

    # 训练模型
    if choice == 1:
        data_feature = file.iloc[:, 0:4]
        data_label = file.iloc[:, 4]
        x_train, x_test, y_train, y_test = train_test_split(data_feature, data_label, test_size=0.2)
        if choice2 == 1:
            study = MyKNN.MyKNN(x_train, y_train, x_test, y_test, False)
        elif choice2 == 2:
            study = mySVC.mySVC(x_train, y_train, x_test, y_test, 'sigmoid', False)
        elif choice2 == 3:
            study = MyLogiRe.MyLogiRe(x_train, y_train, x_test, y_test, False)
        elif choice2 == 4:
            study = myRf.myRf(x_train, y_train, x_test, y_test, False)
        elif choice2 == 5:
            study = MyBYS.MyBYS(x_train, y_train, x_test, y_test, False)
        elif choice2 == 6:
            study = MyMLP.MyMLP(x_train, y_train, x_test, y_test, False)
        elif choice2 == 7:
            study = myVoting.myVoting(x_train, y_train, x_test, y_test, True)
        elif choice2 == 8:
            study = myStacking.myStacking(x_train, y_train, x_test, y_test, True)
        else:
            print("bad choice,exit")
            exit(1)

        start_time = time.time()
        study.excute()
        end_time = time.time()
        print("total time:%.2fs" % (end_time - start_time))

    # 用已有模型进行测试
    elif choice == 2:
        x_test = file.iloc[:, 0:4]
        y_test = file.iloc[:, 4]

        if choice2 == 1:
            study = MyKNN.MyKNN(None, None, x_test, y_test, True)
        elif choice2 == 2:
            study = mySVC.mySVC(None, None, x_test, y_test, 'sigmoid', True)
        elif choice2 == 3:
            study = MyLogiRe.MyLogiRe(None, None, x_test, y_test, True)
        elif choice2 == 4:
            study = myRf.myRf(None, None, x_test, y_test, True)
        elif choice2 == 5:
            study = MyBYS.MyBYS(None, None, x_test, y_test, True)
        elif choice2 == 6:
            study = MyMLP.MyMLP(None, None, x_test, y_test, True)
        elif choice2 == 7:
            study = myVoting.myVoting(None, None, x_test, y_test, True)
        elif choice2 == 8:
            study = myStacking.myStacking(None, None, x_test, y_test, True)

        else:
            print("bad choice,exit")
            exit(1)

        study.excute()
    # 用已有模型预测数据包类型
    elif choice == 3:
        x_test = file.iloc[:, 0:4]
        print(x_test)
        if choice2 == 1:
            study = MyKNN.MyKNN(None, None, x_test, None, True)
        elif choice2 == 2:
            study = mySVC.mySVC(None, None, x_test, None, True)
        elif choice2 == 3:
            study = MyLogiRe.MyLogiRe(None, None, x_test, None, True)
        elif choice2 == 4:
            study = myRf.myRf(None, None, x_test, None, True)
        elif choice2 == 5:
            study = MyBYS.MyBYS(None, None, x_test, None, True)
        elif choice2 == 6:
            study = MyMLP.MyMLP(None, None, x_test, None, True)
        elif choice2 == 7:
            study = myVoting.myVoting(None, None, x_test, None, True)
        elif choice2 == 8:
            study = myStacking.myStacking(None, None, x_test, None, True)
        else:
            print("bad choice,exit")
            exit(1)

        study.predict()
        # study.createpage(file_path)


