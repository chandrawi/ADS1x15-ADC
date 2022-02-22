"""
FILE    : ADS_read_async.py
AUTHOR  : Chandra.Wijaya
VERSION : 1.2.0
PURPOSE : read analog input

test
connect 1 potmeter 

GND ---[   x   ]------ 3.3V
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
print("ADS1X15_LIB_VERSION: {}".format(ADS1x15.__version__))

# set gain to 4.096V max
ADS.setGain(ADS.PGA_4_096V)
f = ADS.toVoltage()
ADS.requestADC(0)

while True :
    if ADS.isReady() :
        val_0 = ADS.getValue()
        ADS.requestADC(0)
        print("Analog0: {0:d}\t{1:.3f} V".format(val_0, val_0 * f))
    time.sleep(1)
