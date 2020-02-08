import numpy as np
import matplotlib.pyplot as plt

rabbitPop = []
timeStamps = []

def plotStuff():
	X = np.array(timeStamps)
	Y = np.array(rabbitPop)
	plt.scatter(X,Y)
	plt.show()
