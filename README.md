<!-- PROJECT SHIELDS -->
[![PyPI - Downloads](https://img.shields.io/pypi/dm/ADS1x15-ADC)](https://pypi.org/project/ADS1x15-ADC/)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/chandrawi/ADS1x15-ADC)](https://github.com/chandrawi/ADS1x15-ADC/releases)
[![GitHub license](https://img.shields.io/github/license/chandrawi/ADS1x15-ADC)](https://github.com/chandrawi/ADS1x15-ADC/blob/main/LICENCE)

# ADS1X15

Python library for I2C ADC ADS1015, ADS1115, and similar analog to digital converter. Works using I2C bus under Linux kernel.


## Description

This library should work for the devices mentioned below,
although not all sensors support all functionality.

| Device  | Channels | Resolution | Max sps | Comparator | ProgGainAMP | Notes  |
|:-------:|:--------:|:----------:|:-------:|:----------:|:-----------:|:-------|
| ADS1013 |    1     |     12     |  3300   |     N      |      N      |        |
| ADS1014 |    1     |     12     |  3300   |     Y      |      Y      |        |
| ADS1015 |    4     |     12     |  3300   |     Y      |      Y      |        |
| ADS1113 |    1     |     16     |  860    |     N      |      N      |        |
| ADS1114 |    1     |     16     |  860    |     Y      |      Y      |        |
| ADS1115 |    4     |     16     |  860    |     Y      |      Y      | Tested |

As the 1015 and the 1115 are both 4 channels these are the most
interesting from functionality point of view as these can also do
differential measurement.


## Initializing

The address of the ADS1113/4/5 is determined by to which pin the **ADDR**
is connected to:

| ADDR pin connected to | Address | Notes   |
|:---------------------:|:-------:|:-------:|
|      GND              |   0x48  | default |
|      VDD              |   0x49  |         |
|      SDA              |   0x4A  |         |
|      SCL              |   0x4B  |         |

- **ADS1x15()** base constructor, should not be used.
- **ADS1013(I2C_busId, I2C_address)** Constructor with I2C bus id, 
and optional device address as parameter.
- **ADS1014(I2C_busId, I2C_address)** Constructor with I2C bus id, 
and optional device address as parameter.
- **ADS1015(I2C_busId, I2C_address)** Constructor with I2C bus id, 
and optional device address as parameter.
- **ADS1113(I2C_busId, I2C_address)** Constructor with I2C bus id, 
and optional device address as parameter.
- **ADS1114(I2C_busId, I2C_address)** Constructor with I2C bus id, 
and optional device address as parameter.
- **ADS1115(I2C_busId, I2C_address)** Constructor with I2C bus id, 
and optional device address as parameter.

```python
import ADS1x15

# initialize ADS1115 on I2C bus 1 with default address 0x48
ADS = ADS1x15.ADS1115(1)
```


## Configuration

### Programmable Gain

- **setGain(gain: int)** set the gain value, indicating the maxVoltage that can be measured. Adjusting the gain allows one to make more precise measurements.
Note: the gain is not set in the device until an explicit read/request of the ADC (any read call will do).
See table below.
- **getGain()** returns the gain value (index).

| PGA value | Max Voltage | Constant   | Notes   |
|:---------:|:-----------:| :---------:|:-------:|
|      0    |   ±6.144V   | PGA_6_144V | default |
|      1    |   ±4.096V   | PGA_4_096V |         |
|      2    |   ±2.048V   | PGA_2_048V |         |
|      4    |   ±1.024V   | PGA_1_024V |         |
|      8    |   ±0.512V   | PGA_0_512V |         |
|      16   |   ±0.256V   | PGA_0_256V |         |

- **getMaxVoltage()** returns the max voltage with the current gain.
- **toVoltage(raw: int)** converts a raw measurement to a voltage.
Can be used for normal and differential measurements.
The default value of 1 returns the conversion factor for any raw number.

The voltage factor can also be used to set HIGH and LOW threshold registers 
with a voltage in the comparator mode.
Check the examples.

```python
  f = ADS.toVoltage()
  ADS.setComparatorThresholdLow( 3.0 / f )
  ADS.setComparatorThresholdLow( 4.3 / f )
```


### Operational mode

The ADS sensor can operate in single shot or continuous mode. 
Depending on how often one needs a conversion one can tune the mode.
- **setMode(mode: int)** 0 = MODE_CONTINUOUS, 1 = MODE_SINGLE (default)
Note: the mode is not set in the device until an explicit read/request of the ADC (any read call will do).
- **getMode()** returns current mode 0 or 1, or INVALID_MODE = -1.


### Data rate

- **setDataRate(dataRate: int)** Data rate depends on type of device.
For all devices the index 0..7 can be used, see table below.
Values above 7 ==> will be set to the default 4.
Note: the data rate is not set in the device until an explicit read/request of the ADC (any read call will do).
- **getDataRate()** returns the current data rate (index).

The library has no means to convert this index to the actual numbers
as that would take 32 bytes. 

Data rate in samples per second, based on datasheet numbers.

| data rate | ADS101x | ADS111x | Constant          | Notes   |
|:---------:|--------:|--------:|:-----------------:|:-------:|
|     0     |   128   |   8     | DR_128 or DR_8    | slowest |
|     1     |   250   |   16    | DR_250 or DR_16   |         |
|     2     |   490   |   32    | DR_490 or DR_32   |         |
|     3     |   920   |   64    | DR_920 or DR_64   |         |
|     4     |   1600  |   128   | DR_1600 or DR_128 | default |
|     5     |   2400  |   250   | DR_2400 or DR_250 |         |
|     6     |   3300  |   475   | DR_3300 or DR_475 |         |
|     7     |   3300  |   860   | DR_3300 or DR_860 | fastest |


## ReadADC Single mode

Reading the ADC is very straightforward, the **readADC()** function handles all in one call. This function will wait until conversion finished.
- **readADC(pin: int)** normal ADC functionality, pin = 0..3. 
If the pin number is out of range, this function will return 0.

```python
# read ADC in pin 0
ADS.readADC(0)
```

To read the ADC in an asynchronous way (e.g. to minimize blocking) one has to use three calls:
- **requestADC(pin: int)**  Start the conversion. pin = 0..3. 
- **isBusy()** (Is the conversion not ready yet?) or **isReady()** (Is the conversion ready?) Works only in SINGLE mode!
- **getValue()** Read the result of the conversion.

in terms of code
```python
# configuration things here
ADS.setMode(ADS.MODE_SINGLE)    # SINGLE SHOT MODE
ADS.requestADC(0)               # request on pin 0

if ADS.isReady() :
    value = ADS.getValue()
    ADS.requestADC(0)           # request new conversion
# do other things here
```
See examples


## ReadADC continuous mode

To use the continuous mode one need three calls
- **setMode(0)** 0 = MODE_CONTINUOUS, 1 = MODE_SINGLE (default).
Note: the mode is not set in the device until an explicit read/request of the ADC (any read call will do).
- **readADC(pin: int)** or **requestADC(pin: int)** to get the continuous mode started.
- **getValue()** to return the last value read by the device. 
Note this can be a different pin, so be warned.
Calling this over and over again can give the same value multiple times.

```python
# configuration things here
ADS.setMode(ADS.MODE_CONTINUOUS)
ADS.requestADC(0)               # request on pin 0

while True :
    value = ADS.getValue()
    sleep(1)
```

By using **isBusy()** or **isReady()** one can wait until new data is available.
Note this only works in the SINGLE_SHOT mode.

In continuous mode one should use the **ALERT/RDY** pin to trigger via hardware the readiness of the conversion.
This can be done by using an interrupt.

See examples.


## ReadADC Differential

For reading the ADC in a differential way there are 4 calls possible.

- **readADC_Differential_0_1()** returns the difference between 2 ADC pins.
- **readADC_Differential_0_3()** ADS1x15 only
- **readADC_Differential_1_3()** ADS1x15 only
- **readADC_Differential_2_3()** ADS1x15 only

```python
# read differential ADC between pin 0 and 1
ADS.readADC_Differential_0_1(0)
```

The differential reading of the ADC can also be done with asynchronous calls.

- **requestADC_Differential_0_1()** starts conversion for differential reading
- **requestADC_Differential_0_3()** ADS1x15 only
- **requestADC_Differential_1_3()** ADS1x15 only
- **requestADC_Differential_2_3()** ADS1x15 only

After one of these calls one need to call
- **getValue()** Read the result of the last conversion.

The readiness of a CONTINUOUS conversion can only be detected by the **RDY** line.
Best to use an interrupt for this, see examples.


### Threshold registers ==> mode RDY pin

If the thresholdHigh is set to 0x0100 and the thresholdLow to 0x0000
the **ALERT/RDY** pin is triggered when a conversion is ready.

- **setComparatorThresholdLow(lo)** writes value to device directly.
- **setComparatorThresholdHigh(hi)** writes value to device directly.
- **getComparatorThresholdLow()** reads value from device.
- **getComparatorThresholdHigh()** reads value from device.

See examples.


## Comparator

Please read Page 15 of the datasheet as the behaviour of the
comparator is not trivial.

NOTE: all comparator settings are copied to the device only after an explicit 
**readADC()** or **requestADC()**


### Comparator Mode

When configured as a **TRADITIONAL** comparator, the **ALERT/RDY** pin asserts
(active low by default) when conversion data exceed the limit set in the
high threshold register. The comparator then de-asserts when the input
signal falls below the low threshold register value.

- **setComparatorMode(mode: int)** value 0 = TRADITIONAL 1 = WINDOW, 
- **getComparatorMode()** returns value set.
  
  
If the comparator **LATCH** is set, the **ALERT/RDY** pin asserts and it will be
reset after reading the sensor (conversion register) again.
*An SMB alert command (00011001) on the I2C bus will also reset the alert state.*
*Not implemented in the library (yet)*

In **WINDOW** comparator mode, the **ALERT/RDY** pin asserts if conversion data exceeds
the high threshold register or falls below the low threshold register.
In this mode the alert is held if the **LATCH** is set. This is similar as above.


### Polarity

Default state of the **ALERT/RDY** pin is **LOW**, can be to set **HIGH**.

- **setComparatorPolarity(pol)** 
Flag is only explicitly set after a **readADC()** or a **requestADC()**
- **getComparatorPolarity()** returns value set. 
  

### Latch

Holds the **ALERT/RDY** to **HIGH** (or **LOW** depending on polarity) after triggered
even if actual value has been 'restored to normal' value.

- **setComparatorLatch(latch: int)** 0 = NO LATCH, not 0 = LATCH
- **getComparatorLatch()** returns value set.


### QueConvert

Set the number of conversions before trigger activates.
The **setComparatorQueConvert(mode: int)** is used to set the number of
conversions that exceed the threshold before the **ALERT/RDY** pin is set **HIGH**.
A value of 3 (or above) effectively disables the comparator. See table below.

- **setComparatorQueConvert(mode: int)** See table below.
- **getComparatorQueConvert()**  returns value set.

| Value | Constant        | Meaning                           | Notes   |
|:-----:|:---------------:|:----------------------------------|:-------:|
|   0   | COMP_QUE_1_CONV | trigger alert after 1 conversion  |         |
|   1   | COMP_QUE_2_CONV | trigger alert after 2 conversions |         |
|   2   | COMP_QUE_4_CONV | trigger alert after 4 conversions |         |
|   3   | COMP_QUE_NONE   | Disable comparator                | default |


### Threshold registers comparator mode

Depending on the comparator mode **TRADITIONAL** or **WINDOW** the thresholds registers
mean something different see - Comparator Mode above or datasheet.

- **setComparatorThresholdLow(lo)** set the low threshold; take care the hi >= lo.
- **setComparatorThresholdHigh(hi)**  set the high threshold; take care the hi >= lo.
- **getComparatorThresholdLow()** reads value from device.
- **getComparatorThresholdHigh()** reads value from device.


## Future ideas & improvements

- Improve documentation
- More examples ?
- SMB alert command (00011001) on I2C bus?


## Examples

See examples in this [link](https://github.com/chandrawi/ADS1x15-ADC/tree/main/examples)
