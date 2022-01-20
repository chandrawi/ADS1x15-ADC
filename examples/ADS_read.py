"""
FILE    : ADS_read.py
AUTHOR  : Chandra.Wijaya
VERSION : 1.2.0
PURPOSE : read analog input

test
connect 1 potmeter 

GND ---[   x   ]------ 5V
           |

measure at x (connect to AIN0).
"""

import os
import time
import ADS1x15

# choose your sensor
# ADS = ADS1x15.ADS1013(1, 0x48)
# ADS = ADS1x15.ADS1014(1, 0x48)
# ADS = ADS1x15.ADS1015(1, 0x48)
# ADS = ADS1x15.ADS1113(1, 0x48)
# ADS = ADS1x15.ADS1114(1, 0x48)

ADS = ADS1x15.ADS1115(1, 0x48)

print(os.path.basename(__file__))
print("ADS1X15_LIB_VERSION: {}".format(ADS1x15.LIB_VERSION))

# set gain to 6.144V max
ADS.setGain(ADS.PGA_6_144V)
f = ADS.toVoltage()

while True :
    val_0 = ADS.readADC(0)
    val_1 = ADS.readADC(1)
    val_2 = ADS.readADC(2)
    val_3 = ADS.readADC(3)
    print("Analog0: {0:d}\t{1:.3f} V".format(val_0, val_0 * f))
    print("Analog1: {0:d}\t{1:.3f} V".format(val_1, val_1 * f))
    print("Analog2: {0:d}\t{1:.3f} V".format(val_2, val_2 * f))
    print("Analog3: {0:d}\t{1:.3f} V".format(val_3, val_3 * f))
    time.sleep(1)
