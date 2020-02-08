import numpy as np
import matplotlib.pyplot as plt
from globals import *

def plotStuff():
	X = np.array(timeStamps)
	Y = np.array(rabbitPop)
	
	plt.scatter(X, Y)
	
	plt.title('Rabbit Population vs Time')
	plt.xlabel('Time')
	plt.ylabel('Rabbit Population')

	plt.ylim(0, 40)
	plt.xlim(0, maxTime)
	
	plt.show()

# def plotStuff():
# 	X = np.array(rabbitPop)
# 	Y = np.array(timeStamps)
	
# 	#print(timeStamps[len(timeStamps) - 1])
# 	plt.scatter(X, Y)

# 	plt.xlim(0, maxTime)
# 	#plt.ylim(0, 20)
	
# 	#
# 	
# 	#
	
# 	plt.show()
