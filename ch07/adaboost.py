from numpy import  *

def loadSimpData():
    datMat = matrix([[ 1. ,  2.1],
        [ 2. ,  1.1],
        [ 1.3,  1. ],
        [ 1. ,  1. ],
        [ 2. ,  1. ]])
    classLabels = [1.0, 1.0, -1.0, -1.0, 1.0]
    return datMat,classLabels

def loadDataSet(fileName):      #general function to parse tab -delimited floats
    numFeat = len(open(fileName).readline().split('\t')) #get number of fields
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr =[]
        curLine = line.strip().split('\t')
        for i in range(numFeat-1):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat,labelMat

def stumpClassify(dataMatrix, dimen, threshVal, threshIneq):
    retArray = ones((shape(dataMatrix)[0],1))
    if threshIneq == 'lt':
        retArray[dataMatrix[:,dimen] <= threshVal] = -1.0
    else:
        retArray[dataMatrix[:, dimen] > threshVal] = -1.0
    return retArray

def buildStump(dataArr, classLabels, D):
    dataMatrix = mat(dataArr); labelMat = mat(classLabels).T
    m,n = shape(dataMatrix)
    numSteps = 10.0; bestStump = {}; bestClasEst = mat(zeros((m, 1)))
    minError = inf
    for i in range(n):
        rangeMin = dataMatrix[:,i].min(); rangeMax = dataMatrix[:,i].max()
        stepSize = (rangeMax-rangeMin)/numSteps
        for j in range(-1,int(numSteps)+1):
            for inequal in ['lt', 'gt']:
                threshVal = rangeMin+float(j)*stepSize
                predictedVals = stumpClassify(dataMatrix,i,threshVal,inequal)
                errArr = mat(ones((m,1)))
                errArr[predictedVals==labelMat]=0
                weightedError = D.T*errArr
                #print "split: dim %d, thresh %.2f, thresh ineqal: %s, the weighted error is %.3f" \
                     # % (i, threshVal, inequal, weightedError)
                if weightedError<minError:
                    minError = weightedError
                    bestClasEst = predictedVals.copy()
                    bestStump['dim'] = i
                    bestStump['thresh'] = threshVal
                    bestStump['ineq'] = inequal
    return bestStump, minError, bestClasEst

def adaBoostTrainDS(dataArr,classLabels,numIt=40):
    m,n = shape(dataArr)
    D = mat(ones((m,1))/m)
    weakClassArr = []
    aggClassEst = mat(zeros((m, 1)))
    for i in range(numIt):
        bestStump,error,classEst = buildStump(dataArr,classLabels,D)
        #print "D:", D.T
        #print 'error:', error
        alpha = 0.5*log((1.0-error)/max(error, 1e-16))
        print alpha
        bestStump['alpha'] = alpha
        weakClassArr.append(bestStump)
        expon = multiply(mat(classLabels).T*-1*alpha, classEst)  # exponent for D calc, getting messy
        D = multiply(D, exp(expon))  # Calc New D for next iteration
        D = D / D.sum()
        aggClassEst += classEst * alpha
        #print "aggClassEst: ", aggClassEst.T
        aggErrors = multiply(sign(aggClassEst)!=mat(classLabels).T, ones((m,1)))
        errorRate = aggErrors.sum() / m
        print "total error: ", errorRate
        if errorRate == 0.0: break
    return weakClassArr, aggClassEst

def adaClassify(datToClass,classifierArr):
    dataMatrix = mat(datToClass)
    m = shape(dataMatrix)[0]
    aggClassEst = mat(zeros((m, 1)))
    for i in range(len(classifierArr)):
        classEst = stumpClassify(dataMatrix, classifierArr[i]['dim'], classifierArr[i]['thresh'], classifierArr[i]['ineq'])
        aggClassEst += classEst*classifierArr[i]['alpha']
        #print aggClassEst
    return sign(aggClassEst)



datArr,labelArr = loadDataSet('horseColicTraining2.txt')
classifierArray, aggClassEst = adaBoostTrainDS(datArr,labelArr,10)
testArr,testLabelArr = loadDataSet('horseColicTest2.txt')
pre = adaClassify(testArr, classifierArray)
m,n = shape(testArr)
precision = mat(zeros((m,1)))
precision[pre!=mat(testLabelArr).transpose()] = 1

rate = precision.sum()/float(m)
print precision.sum()
print 'rate:', rate