#percolation.py

import numpy as np
import matplotlib.pyplot as plt
import math
from random import *
import random
import scipy.spatial as spatial
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pylab


p=0.7
r=3
t=5
gridSize = 20	#sert grid size


def getNeighbours(point_tree, points):
	global neighbours
	neighbours=[]
	for i in range(0,len(settings)-1):
		neighbours.append(point_tree.query_ball_point(points[i], r))


##grid initiation
def gridSetup():
	coords=[] 	#coords is list of all grid square co-ordinates
	for i in range(1,gridSize+1):
		for j in range(1,gridSize+1):
			coords.append((i,j)) 	#loops through every cell and adds to coords
	global points
	points=np.array(coords)
	global settings
	settings=[0]*len(coords) #settings is activation of each cell relevant to coords
	plotGrid(settings)
	randomIndexes=random.sample(range(1, len(coords)), int(round((gridSize**2)*p)))
	for i in range(0,len(randomIndexes)-1): 	#set random cells as potential (1) according to p value
		element=randomIndexes[i]-1
		settings[element]=1
	randomPoint=[0,0]
	while randomPoint[0]<r or randomPoint[0]>gridSize-r or randomPoint[1]<r or randomPoint[1]>gridSize-r:
		randomStart=randint(1, len(settings))-1	#find random initialise cell to activate
		randomPoint=coords[randomStart]
	global point_tree 
	point_tree = spatial.cKDTree(points)	#create array of coords for radius finding
	plotGrid(settings)
	getNeighbours(point_tree, points)
	firstNeighbours = neighbours[randomStart]
	for i in range(0,len(firstNeighbours)):
		settings[firstNeighbours[i]]=3 	#set start point and neighbours as active (3)
	plotGrid(settings)


def plotGrid(settings):
	fig1= plt.figure()
	ax1 = fig1.add_subplot(111, aspect='equal')
	for i in range(0,len(settings)):
		if settings[i]==0:
			ax1.add_patch(
		    patches.Rectangle(
		        (points[i,0]-1, points[i,1]-1), 1, 1, facecolor = "grey", edgecolor="none") )   # (x,y), width, height, colour
		elif settings[i]==1:
			ax1.add_patch(
		    patches.Rectangle(
		        (points[i,0]-1, points[i,1]-1), 1, 1, facecolor = "black", edgecolor="none") ) 
		elif settings[i]==3:
			ax1.add_patch(
		    patches.Rectangle(
		        (points[i,0]-1, points[i,1]-1), 1, 1, facecolor = "white", edgecolor="blue") ) 
	pylab.ylim([0,gridSize])
	pylab.xlim([0,gridSize])
	plt.show()


def percolate():
	origSettings=0
	while origSettings!=settings:
		origSettings=list(settings)
		for i in range(0,len(settings)-1):
			if settings[i]==1:
				nearestNeighbours = neighbours[i]
				neighbourSettings=[]
				for j in range(0,len(nearestNeighbours)):
					neighbourSettings.append(settings[nearestNeighbours[j]])
				count = neighbourSettings.count(2) + neighbourSettings.count(3)
				if count >= t:
					settings[i]=2
		plotGrid(settings)

def smoothing():
	greys=[]
	notGreys=[]
	for i in range(0,len(settings)-1):
		if settings[i]==0:
			greys.append(i)
		else:
			notGreys.append(i)
	print(notGreys)
	points2=np.array( coords[i] for i in notGreys)
	print(points2)
	point_tree2 = spatial.cKDTree(points2)
	greyNeighbours=[]
	print('test')
	for i in range(0,len(greys)-1):
		greyNeighbours.append(point_tree2.query_ball_point(greys[i], 1))
	print(greyNeighbours)


#run code
gridSetup()
percolate()
smoothing()



