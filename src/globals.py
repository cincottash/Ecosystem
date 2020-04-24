global time
global dt
global maxTime
import time as clock
canvasWidth = 1800
canvasHeight = 1000

time = 0.00000
dt = 0.00005
spawnRadius = 450

grassRespawnDelay = 5.0

rotationAngle = 90

minRabbitStartSize = 4

maxRabbitStartSize = 14

rabbitList = []
grassList = []
foxList = []

rabbitPop = []
averageRabbitSize = []
timeStamps = []
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BROWN = (255, 150, 104)

lastGrassPlaceTime = clock.time()