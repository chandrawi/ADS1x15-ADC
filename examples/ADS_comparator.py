"""
FILE    : ADS_comparator.py
AUTHOR  : Chandra.Wijaya
VERSION : 1.2.0
PURPOSE : read analog input

test
connect 1 potmeter 

GND ---[   x   ]------ 3.3V
           |

measure at x (connect to AIN0).

GND ---[LED]---[ALERT_PIN]---[ R ]--- 3.3V

Connect a LED (+ resistor) to ALERT PIN
and see it trigger at configured way by the comparator.
"""

import os
import time
import ADS1x15

ADS = ADS1x15.ADS1115(1, 0x48)

print(os.path.basename(__file__))
print("ADS1X15_LIB_VERSION: {}".format(ADS1x15.LIB_VERSION))

# set gain to 4.096V max
ADS.setGain(ADS.PGA_4_096V)

# set comparator to traditional mode, active high, latch, and trigger alert after 1 conversion
ADS.setComparatorMode(ADS.COMP_MODE_TRADITIONAL)
ADS.setComparatorPolarity(ADS.COMP_POL_ACTIV_HIGH)
ADS.setComparatorLatch(ADS.COMP_LATCH)
ADS.setComparatorQueue(ADS.COMP_QUE_1_CONV)
# set threshold
f = ADS.toVoltage()
ADS.setComparatorThresholdLow(int(1.5 / f))    # 1.5V
ADS.setComparatorThresholdHigh(int(2.5 / f))   # 2.5V
thsL = ADS.getComparatorThresholdLow() * f
thsH = ADS.getComparatorThresholdHigh() * f
print("Threshlod: {0:.3f}V <-> {1:.3f}V".format(thsL, thsH))
# LED will be on when voltage exceed 2.5V and only off when voltage drop to 1.5V

while True :
    val_0 = ADS.readADC(0)
    volt_0 = val_0 * f
    print("Analog0: {0:d}\t{1:.3f}V".format(val_0, volt_0))
    time.sleep(1)
