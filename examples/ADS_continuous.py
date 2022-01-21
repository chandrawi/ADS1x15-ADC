"""
FILE    : ADS_continuous.py
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
print("ADS1X15_LIB_VERSION: {}".format(ADS1x15.LIB_VERSION))

ADS.setGain(ADS.PGA_4_096V)
ADS.setDataRate(ADS.DR_ADS111X_128)
ADS.setMode(ADS.MODE_CONTINUOUS)
ADS.requestADC(0)                          # First read to trigger

while True :
    raw = ADS.getValue()
    print("{0:.3f} V".format(ADS.toVoltage(raw)))
    time.sleep(1)
