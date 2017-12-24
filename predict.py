#!/usr/bin/python

import csv
import sys

def csvToArray(file):
	file = open(file, "r")
	arr = csv.reader(file, delimiter=',')

	for line in arr:
		if len(line) >= 2:
			th0 = float(line[0])
			th1 = float(line[1])
			return th0, th1
		else:
			print "Bad train"
			exit(1)
	return None

def estimatePrice(th0, th1, mileage):
	ret = th0 + (th1 * mileage)
	return ret

try:
	open("theta", 'r')
except IOError:
	print "Please train it ./train.py"
	exit(1)

th0, th1 = csvToArray("theta")

while True:
	try:
		try:
			mileage = raw_input("Enter a mileage: ")
			if float(mileage) < 0:
				print "Bad mileage"
			else:
					mileage = float(mileage)
					price = estimatePrice(th0, th1, mileage)
					if price < 0:
						price = 0
					print "Price: " + str(price)
		except ValueError:
			print "Bad mileage"
	except EOFError:
		print "\nGoodbye"
		exit(0)
