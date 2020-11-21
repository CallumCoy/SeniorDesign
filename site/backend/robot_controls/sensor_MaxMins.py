import FaBo9Axis_MPU9250
import time
import sys

mpu9250 = FaBo9Axis_MPU9250.MPU9250()

xMax = 0
yMax = 0
zMax = 0

xMin = 0
yMin = 0
zMin = 0

try:
    startTime = time.time()
    while (startTime - time.time() < (60 * 5)):
        mag = mpu9250.readMagnet()

        x = mag["x"]
        y = mag["y"]
        z = mag["z"]

        xMax = max(x, xMax)
        yMax = max(y, yMax)
        zMax = max(z, zMax)

        xMin = min(x, xMin)
        yMin = min(y, yMin)
        zMin = min(z, zMin)
except:
    print("cancelled early.")
else:
    print("5 minutes are up")
finally:
    print(" \t x \t y \t z")
    print("Max \t %6f \t %6f \t %6f" % (xMax, yMax, zMax))
    print("Min \t %6f \t %6f \t %6f" % (xMin, yMin, zMin))
