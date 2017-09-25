from numpy import *

def loadDataSet():
    dataMat=[]; labelMat=[]
    fr = open('testSet.txt')
    for line in fr:
        lineArr = line.strip().split('\t')
        x0=float(lineArr[0].strip()); x1=float(lineArr[1].strip())
        dataMat.append([1.0, x0, x1])
        labelMat.append(int(lineArr[2]))
    return dataMat, labelMat

def sigmoid(inX):
    return 1.0/(1+exp(-inX))

def gradAscent(dataMatIn, classLabels):
    dataMatrix = mat(dataMatIn)
    labelMat = mat(classLabels).transpose()
    m,n = shape(dataMatrix)
    alpha = 0.001
    maxCycles = 500
    weights = ones((n,1))
    for k in range(maxCycles):
        h=sigmoid(dataMatrix*weights)
        error = labelMat-h
        weights = weights + alpha * dataMatrix.transpose()*error
    return weights

def stocGradAscent0(dataMatrix, classLabels):
    m,n = shape(dataMatrix)
    alpha = 0.01
    weights = ones(n)   #initialize to all ones
    for i in range(m):
        h = sigmoid(sum(dataMatrix[i]*weights))
        error = classLabels[i] - h
        weights = weights + alpha * error * dataMatrix[i]
    return weights

def stocGradAscent1(dataMatrix, classLabels, numIter=150):
    m, n = shape(dataMatrix)
    weights = ones(n)
    for j in range(numIter):
        dataIndex = range(m)
        for i in range(m):
            alpha = 4/(1.0+i+j)+0.0001
            randIndex = int(random.uniform(0,len(dataIndex)))
            h=sigmoid(sum(dataMatrix[randIndex]*weights))
            error = classLabels[randIndex] - h
            weights = weights + alpha * error * dataMatrix[randIndex]
            del(dataIndex[randIndex])
    return weights

def plotBestFit(weights):
    import matplotlib.pyplot as plt
    dataMat,labelMat=loadDataSet()
    dataArr = array(dataMat)
    n = shape(dataArr)[0]
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in range(n):
        if int(labelMat[i])== 1:
            xcord1.append(dataArr[i,1]); ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1]); ycord2.append(dataArr[i,2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = arange(-3.0, 3.0, 0.1)
    y = (-weights[0]-weights[1]*x)/weights[2]
    ax.plot(x, y)
    plt.xlabel('X1'); plt.ylabel('X2');
    plt.show()

def classifyVector(inX, weights):
    prob = sigmoid(sum(inX*weights))
    if prob>0.5: return 1
    else: return 0

def colicTest():
    frTrain = open('horseColicTraining.txt'); frTest = open('horseColicTest.txt')
    trainSet=[]; trainLabel=[]
    for line in frTrain:
        currLine = line.strip().split('\t')
        lineArr=[]
        for i in range(21):
            lineArr.append(float(currLine[i]))
        trainSet.append(lineArr)
        trainLabel.append(float(currLine[21]))
    trainweights = stocGradAscent1(array(trainSet), trainLabel, 1000)
    numTest=0.0; errorcount=0
    for line in frTest:
        numTest+=1.0
        currLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(currLine[i]))
        if int(classifyVector(array(lineArr), trainweights))!=int(currLine[21]):
            errorcount+=1.0
    errorRate = float(errorcount)/numTest
    print 'error rate is %f'%errorRate
    return errorRate

colicTest()
# dataArr, labelMat = loadDataSet()
# weights = stocGradAscent1(array(dataArr), labelMat)
# print weights
# # weights = gradAscent(dataArr, labelMat)
# # print weights
# plotBestFit(weights)