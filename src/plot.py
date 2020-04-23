import numpy as np
import matplotlib.pyplot as plt
from globals import *

def plotStuff(xLim, maxRabbits):

	X = np.array(timeStamps)
	Y = np.array(rabbitPop)
	
	plt.figure()

	plt.subplot(221)
	plt.scatter(X, Y, s = 2.0)
	plt.title('Rabbit Population vs Time')
	plt.xlim(0, xLim)

	#Make the graph go 10% higher than the max rabbits
	plt.ylim(0, maxRabbits + maxRabbits*0.1)
	plt.grid(True)

	X = np.array(timeStamps)
	Y = np.array(averageRabbitSize)
	
	plt.subplot(222)
	plt.scatter(X, Y, s = 3.0)
	plt.title('Average Rabbit Size vs Time')
	plt.xlim(0, xLim)
	plt.ylim(0, 12)
	plt.grid(True)
	
	plt.show()
