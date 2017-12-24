#!/usr/bin/python

import numpy as np
import csv
# import time

import matplotlib.pyplot as plt

def showPlot(th0, th1):

	font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }

	plt.title(r'$\theta$0 = ' + str(th0) + "		" + r'$\theta$1 = ' + str(th1), fontdict=font)
	max1 = np.amax(np.array(X).astype(np.float))
	res = th0 + (max1 * th1)

	plt.plot(X, Y, 'mo')
	plt.plot([0, max1], [th0, res])
	plt.ylabel('Price')
	plt.xlabel('Mileage')

	plt.show()

def estimatePrice(mileage):
	ret = th0 + (th1 * mileage)
	return ret

def sigmaTh0():
	# sum sigma
	i = 0
	sigma = 0
	while i < m:
		sigma = sigma + estimatePrice(float(X[i])) - float(Y[i])
		i+=1
	return sigma

def sigmaTh1():
	# sum sigma
	i = 0
	sigma = 0
	while i < m:
		sigma = sigma + (estimatePrice(float(X[i])) - float(Y[i])) * float(X[i])
		i+=1
	return sigma

def updateLr(th, loss, lr):
	if loss > 0:
		th = th - lr
	else:
		th = th + lr
	return th

def printScores(th0, th1, tmpTh0, tmpTh1, epoch):	
	lossTh0 = round(abs(tmpTh0), 5)
	lossTh1 = round(abs(tmpTh1), 5)

	print("Th0: {0:<15.5g} Th1: {1:<15.5g} Loss Th0: {2:<15.5g} Th1: {3:<15.5g} Epoch: {4:}" \
		.format(th0, th1, lossTh0, lossTh1, epoch))

	with open('theta', 'w') as file:
		file.write(str(th0) + "," + str(th1) + "\n")

def csvToArray(file):
	file = open(file, "r")
	arr = csv.reader(file, delimiter=',')

	X = [] # Mileage
	Y = [] # Price

	i = 0
	for line in arr:
		i+=1
		if i!=1:
			X.append(line[0])
			Y.append(line[1])
	
	if len(X) != len(Y):
		print "Error"
		exit(1)
	
	return (X, Y)

##############################
############ MAIN ############
##############################

th0 = 0 	# 8498
th1 = 0		# -0.02142
lr0 = 1.0
lr1 = 1.0
PRECISION = 1e-07 # Learning rate minimal.
X, Y = csvToArray("data.csv")
m = len(X)

def main():

	# print "ESTIMATED " + str(estimatePrice(10000))

	global lr0
	global lr1
	global th0
	global th1

	epoch = 0
	oldth0 = 0
	oldth1 = 0
	while True:
		epoch+=1

		tmpTh0 = lr0 * sigmaTh0() / m
		tmpTh1 = lr1 * sigmaTh1() / m

		th0 = updateLr(th0, tmpTh0, lr0)
		th1 = updateLr(th1, tmpTh1, lr1)
		
		if epoch % 50 == 0:
			if oldth0 >= th0 and oldth1 >= th1:
				if lr1 > PRECISION:
					lr1 = lr1 / 10
					# print " --- LEARNING RATE Th1 SET TO " + str(lr1) 
				elif lr0 > PRECISION:
					lr0 = lr0 / 10
					# print " --- LEARNING RATE Th0 SET TO " + str(lr0)
				else:
					printScores(th0, th1, tmpTh0, tmpTh1, epoch)
					break
			if epoch % 3000 == 0:
				printScores(th0, th1, tmpTh0, tmpTh1, epoch)

			oldth0 = th0
			oldth1 = th1

	showPlot(th0, th1)

	# time.sleep(0.01)

main()
