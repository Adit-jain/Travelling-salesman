import sys
import math
import random
import numpy as np
import copy
import tsp_visualize

start=[]
startNew=[]
tempStart=[]


def initial_tour(nodes):
    #initial tour from [0, 1, 2, ... , n-1]
    init=[]
    for i in range(nodes):
        init.append(i)
    return init

def cost(start,distances):
    length = len(start)-1;
    distCost = 0.0;
    for i in range(length):
            distCost += distances[start[i]][start[i+1]]
    distCost += distances[start[length ]][start[0]]

    return distCost

def initialTemperature():
    return 100

def newTemperature(temperature,constant):
    temperature = temperature * constant
    return temperature

def prob_acceptance(oldCost, newCost, temperature):
    #choose random
    prob = np.exp ( -(newCost - oldCost) / temperature)
    randomProb = random.uniform(0, 1)
    if (randomProb < prob):
        return 1
    else:
        return 0

def randomNextState(tempStart):
    length=len(tempStart)-1
    next1=randomNumber(0,length)%length
    next2=randomNumber(0,length)%length
    if(next1 != next2):
        temp=tempStart[next1]
        tempStart[next1]=tempStart[next2]
        tempStart[next2]=temp
    else:
        randomNextState(tempStart)

    return tempStart

def randomNumber(a,b):
    #generates random number between start and end inclusively
    r=random.randint(a,b)
    return r

def simulatedAnneling(nodes,distances):

    epsilon = nodes * (5000)
    constant = 0.99

    #initial tour
    init = initial_tour(nodes)
    start=init[:]
    minCost = cost(start,distances)
    minTour = start[:]

    #initial temperature
    temperature = initialTemperature()

    for i in range(epsilon):
        #random neighbores
        tempStart=start[:]
        startNew = randomNextState(tempStart)

        #if best
        oldCost = cost(start,distances)
        newCost = cost(startNew,distances)
        if (newCost < oldCost):
            start = startNew[:]

            if (newCost < minCost):
                minCost = newCost
                minTour = startNew[:]

        elif (prob_acceptance(oldCost, newCost, temperature)):
            start = startNew[:]

        temperature = newTemperature(temperature,constant)

    return minTour,minCost


def insertDistance(nodes):
    i=0
    while(i<nodes):
        distances.append(list(map(float,input("Dist").strip().split(' '))))
        i = i+1
    return distances


def calculateDistance(nodes,x,y):
    n=nodes
    temp=[]

    for i in range(n):
        for j in range(n):
            val=math.sqrt(((x[i]-x[j])**2) + ((y[i]-y[j])**2))
            temp.append(val)

    distances = [ temp[i*n:(i+1)*n] for i in range(n) ]
    return distances


if __name__ == "__main__":

    points=[]
    x=[]
    y=[]
    distances=[]
    sys.setrecursionlimit(5000)

    cityCnt = int(input("No. of Cities: \n  1. 131 | 2. 237 | 3. 343 | 4. 379 | 5. 380 | 6. 20 Cities of Rajasthan \n "))

    if(cityCnt<1 or cityCnt>6):
        print("Invalid Input")
        quit()

    files = ["xqf131.txt","xqg237.txt","pma343.txt","pka379.txt","bcl380.txt","rajasthan.txt"]

    with open(f"./inputFiles/{files[cityCnt-1]}") as file:
        data, *coord = file.readlines()

    nodes = int(data)

    for out in coord:
        if(out=='EOF\n'):
            break
        out = out.split(' ')
        x.append(float(out[1]))
        y.append(float(out[2]))

    distances = calculateDistance(nodes,x,y)
    minTour, minCost = simulatedAnneling(nodes,distances)
    print(f"\nTotal Cost is: {minCost}\n")
    tsp_visualize.plotTSP(minTour, x, y)
