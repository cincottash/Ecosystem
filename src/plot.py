import numpy as np
import matplotlib.pyplot as plt
from globals import *

def plotStuff():

	X = np.array(timeStamps)
	Y = np.array(rabbitPop)
	
	plt.figure()

	plt.subplot(221)
	plt.scatter(X, Y, s = 2.0)
	plt.title('Rabbit Population vs Time')
	plt.xlim(0, maxTime)
	plt.ylim(0, 75)
	plt.grid(True)

	X = np.array(timeStamps)
	Y = np.array(averageRabbitSize)
	
	plt.subplot(222)
	plt.scatter(X, Y, s = 3.0)
	plt.title('Average Rabbit Size vs Time')
	plt.xlim(0, maxTime)
	plt.ylim(0, 12)
	plt.grid(True)
	
	plt.show()
