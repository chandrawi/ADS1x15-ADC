"""
FILE    : ADS_differential.py
AUTHOR  : Chandra.Wijaya
VERSION : 1.2.1
PURPOSE : read differential

test 1
connect 2 potmeters in series

GND ---[   x   ]------[   y   ]---- 5V
           |              |

measure at x and y  (connect to AIN0 and AIN1). 
x should be lower or equal to y

test 2
connect 2 potmeters parallel

GND ---[   x   ]------ 5V
           |

GND ---[   y   ]------ 5V
           |

measure at x and y  (connect to AIN0 and AIN1).
range from -VDD .. +VDD are possible
"""

import os
import time
import ADS1x15

ADS = ADS1x15.ADS1115(1, 0x48)

print(os.path.basename(__file__))
print("ADS1X15_LIB_VERSION: {}".format(ADS1x15.LIB_VERSION))

# set gain to 4.096V max
ADS.setGain(ADS.PGA_4_096V)

while True :
    val_01 = ADS.readADC_Differential_0_1()
    volts_01 = ADS.toVoltage(val_01)
    print("Analog_0-1: {0:d}\t{1:.3f} V".format(val_01, volts_01))
    time.sleep(1)
