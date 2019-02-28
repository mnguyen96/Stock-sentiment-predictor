import csv
import operator
import math
import random
# array tuple sum 5 day price change, date


def get_change(current, previous):
    if current == previous:
        return 0.0
    try:
        return ((current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0


def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        # print(length)
        # print(instance1)
        # print(instance2)
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)


def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance)-1
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors


def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = round(neighbors[x][-1] * 2)/2
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.items(),
                         key=operator.itemgetter(1), reverse=True)
    # print(sortedVotes)
    return sortedVotes


def getAccuracy(testSet, predictions):
    correct = 0
    for x in range(len(testSet)):
        if (abs(testSet[x][-1] + predictions[x]) == abs(testSet[x][-1]) + abs(predictions[x]) and abs(testSet[x][-1] - predictions[x]) <= 3.5):
            correct += 1
    return (correct/float(len(testSet))) * 100.0

def getSentiment(result, testSet):
    predictedSentiment = ""
    trueSentiment = ""
    if result > 0:
        if result < .5:
            predictedSentiment = "Barely bullish" 
        else:
            predictedSentiment = "Bullish"
    else:
        if result > -.5:
            predictedSentiment = "Barely bearish"
        else:
            predictedSentiment = "Bearish"
    if testSet > 0:
        if testSet  < .5:
            trueSentiment = "Barely bullish" 
        else:
            trueSentiment = "Bullish"
    else:
        if testSet > -.5:
            trueSentiment = "Barely bearish"
        else:
            trueSentiment = "Bearish"
    return predictedSentiment, trueSentiment
data = []
with open('QQQ.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    count = 1
    start = 0
    put = [None]*3
    reader_list = list(csv.reader(csv_file, delimiter=','))
    reader_list = reader_list[1:]
    for idx,row in enumerate(reader_list):
        if (idx < len(reader_list)-4):
            put[0] = round(get_change(float(reader_list[idx+4][4]),float(row[4])), 2)
            put[1] = row[0]
            put[2] = reader_list[idx+4][0]
            data.append(put)
            put = [None]*3
    TEST = [x[0] for x in data[len(data)-10:]]
    trainingSet = []
    testSet = []
    # turn into arrays of 5 (percent change over 5 days)
    for i in range(len(data)):
        if (len(data[i:i+10]) < 10):
            break
        if random.random() < .67:
            trainingSet.append([x[0] for x in data[i:i+10]])
        else:
            testSet.append([x[0] for x in data[i:i+10]])

    predictions = []
    k = 8
    for x in range(len(testSet)):
        neighbors = getNeighbors(trainingSet, testSet[x], k)
        result = getResponse(neighbors)[0][0]
        predictions.append(result)

        predictedSentiment, trueSentiment = getSentiment(result, testSet[x][-1])
    print(TEST)
    dd = getNeighbors(trainingSet, TEST, k)
    test_prediction = getResponse(dd)
    average = sum([x[0] for x in test_prediction])/len(test_prediction)
    sentiment = getSentiment(test_prediction[0][0], 0)[0]
    onlyValues = [x[0] for x in test_prediction]
    print(sorted(test_prediction))
    generatedMovement = round((test_prediction[0][0] + average)/2)/2
    # print(generatedMovement)
    print('Prediction for next 5 trading days: ' + '{0:+}% / '.format(test_prediction[0][0]) + sentiment +', Historic average and range: ' + repr(average)+ ', ' + repr(max(onlyValues)-min(onlyValues)))

    accuracy = getAccuracy(testSet, predictions)
    print('Accuracy: ' + repr(round(accuracy, 3)) + '%')
    cd = TEST[1:]
    cd.append(generatedMovement)
    # print(cd)
    getnew = getNeighbors(trainingSet, cd,k)
    tt = getResponse(getnew)
    # print(tt)
    print(f'Processed {len(data)} lines.')
