<!-- PROJECT SHIELDS -->
[![PyPI - Downloads](https://img.shields.io/pypi/dm/ADS1x15-ADC)](https://pypi.org/project/ADS1x15-ADC/)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/chandrawi/ADS1x15-ADC)](https://github.com/chandrawi/ADS1x15-ADC/releases)
[![GitHub license](https://img.shields.io/github/license/chandrawi/ADS1x15-ADC)](https://github.com/chandrawi/ADS1x15-ADC/blob/main/LICENCE)

# ADS1X15

Python library for I2C ADC ADS1015, ADS1115, and similar analog to digital converter. This library works with Raspberry pi or other SBC using I2C bus under Linux kernel.

For using I2C ADC with Arduino, you can check this similar library in this [link](https://github.com/RobTillaart/ADS1X15).


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


## Installation

### Using pip

Using terminal run following command.
```sh
pip3 install ADS1x15-ADC
```

### Using Git and Build Package

To using latest update of the library, you can clone then build python package manually. Using this method require **setuptools** and **wheel** module.
```sh
git clone https://github.com/chandrawi/ADS1x15-ADC.git
cd ADS1x15-ADC
python3 setup.py bdist_wheel
pip3 install dist/ADS1x15_ADC-1.2.1-py3-none-any.whl
```

### Enabling I2C Interface

Before using the library, I2C interface must be enabled. For Raspberry pi OS, this is done by set I2C interface enable using raspi-config or edit `/boot/config.txt` by adding following line.
```txt
dtparam=i2c_arm=on
```


## Initializing

The address of the ADS1113/4/5 is determined by to which pin the **ADDR**
is connected to:

| ADDR pin connected to | Address | Notes   |
|:---------------------:|:-------:|:-------:|
|      GND              |   0x48  | default |
|      VDD              |   0x49  |         |
|      SDA              |   0x4A  |         |
|      SCL              |   0x4B  |         |

To initialize the library you must call constructor as described below.
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

For example.

```python
import ADS1x15

# initialize ADS1115 on I2C bus 1 with default address 0x48
ADS = ADS1x15.ADS1115(1)
```


## Configuration

### Programmable Gain

- **setGain(gain: int)** set the gain value, indicating the maxVoltage that can be measured. Adjusting the gain allowing to make more precise measurements.
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
Check the [examples](https://github.com/chandrawi/ADS1x15-ADC/blob/main/examples/ADS_comparator.py).

```python
  f = ADS.toVoltage()
  ADS.setComparatorThresholdLow( 1.5 / f )
  ADS.setComparatorThresholdHigh( 2.5 / f )
```


### Operational mode

The ADS sensor can operate in single shot or continuous mode. 
Depending on how often conversions needed you can tune the mode.
- **setMode(mode: int)** 0 = MODE_CONTINUOUS, 1 = MODE_SINGLE (default)
Note: the mode is not set in the device until an explicit read/request of the ADC (any read call will do).
- **getMode()** returns current mode 0 or 1, or INVALID_MODE = -1.


### Data rate

- **setDataRate(dataRate: int)** Data rate depends on type of device.
For all devices the index 0..7 can be used, see table below.
Values above 7 ==> will be set to the default 4.
Note: the data rate is not set in the device until an explicit read/request of the ADC (any read call will do).
- **getDataRate()** returns the current data rate (index).

Data rate in samples per second, based on datasheet is described on table below.

| data rate | ADS101x  | ADS111x | Constant        | Constant       | Notes   |
|:---------:|---------:|--------:|:---------------:|:--------------:|:-------:|
|     0     | 128 SPS  | 8 SPS   | DR_ADS101X_128  | DR_ADS111X_8   | slowest |
|     1     | 250 SPS  | 16 SPS  | DR_ADS101X_250  | DR_ADS111X_16  |         |
|     2     | 490 SPS  | 32 SPS  | DR_ADS101X_490  | DR_ADS111X_32  |         |
|     3     | 920 SPS  | 64 SPS  | DR_ADS101X_920  | DR_ADS111X_64  |         |
|     4     | 1600 SPS | 128 SPS | DR_ADS101X_1600 | DR_ADS111X_128 | default |
|     5     | 2400 SPS | 250 SPS | DR_ADS101X_2400 | DR_ADS111X_250 |         |
|     6     | 3300 SPS | 475 SPS | DR_ADS101X_3300 | DR_ADS111X_475 |         |
|     7     | 3300 SPS | 860 SPS | DR_ADS101X_3300 | DR_ADS111X_860 | fastest |


## ReadADC Single mode

Reading the ADC in single mode is very straightforward, the **readADC()** function handles all in one call. This function will wait until conversion finished.
- **readADC(pin: int)** normal ADC functionality, pin = 0..3. 
If the pin number is out of range, this function will return 0.

```python
# read ADC in pin 0
ADS.readADC(0)
```

See [examples](https://github.com/chandrawi/ADS1x15-ADC/blob/main/examples/ADS_minimum.py).

To read the ADC in an asynchronous way (e.g. to minimize blocking) you need call three functions:
- **requestADC(pin: int)**  Start the conversion. pin = 0..3. 
- **isBusy()** (Is the conversion not ready yet?) or **isReady()** (Is the conversion ready?) Works only in SINGLE mode!
- **getValue()** Read the result of the conversion.

```python
# configuration things here
ADS.setMode(ADS.MODE_SINGLE)    # SINGLE SHOT MODE
ADS.requestADC(0)               # request on pin 0

if ADS.isReady() :
    value = ADS.getValue()
    ADS.requestADC(0)           # request new conversion
# do other things here
```

See [examples](https://github.com/chandrawi/ADS1x15-ADC/blob/main/examples/ADS_read_async.py).


## ReadADC continuous mode

To use the continuous mode you need call three functions:
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

See [examples](https://github.com/chandrawi/ADS1x15-ADC/blob/main/examples/ADS_continuous.py).


In continuous mode, you can't use **isBusy()** or **isReady()** functions to wait until new data available.
Instead you can configure **ALERT/RDY** pin to trigger an interrupt signal when conversion data ready.

### Configure RDY pin interrupt signal

Interrupt signals on the **ALERT/RDY** pin can be triggered every conversion data ready. 
This is done by setting Hi_thresh register MSB to 1 and the Lo_thresh register MSB to 0.

- **setComparatorThresholdLow(lo: int)** set 0x8000 as parameter.
- **setComparatorThresholdHigh(hi: int)** set 0x7FFF as parameter.

See [examples]().


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

The differential reading of the ADC can also can be done using asynchronous calls.

- **requestADC_Differential_0_1()** starts conversion for differential reading
- **requestADC_Differential_0_3()** ADS1x15 only
- **requestADC_Differential_1_3()** ADS1x15 only
- **requestADC_Differential_2_3()** ADS1x15 only

After one of these calls you need to call
- **getValue()** Read the result of the last conversion.

See [examples](https://github.com/chandrawi/ADS1x15-ADC/blob/main/examples/ADS_differential.py).


## Comparator

Please read Page 15 of the datasheet as the behaviour of the
comparator is not trivial.

NOTE: all comparator settings are copied to the device only after calling 
**readADC()** or **requestADC()** functions.


### Comparator Mode

When configured as a **TRADITIONAL** comparator, the **ALERT/RDY** pin asserts
(active low by default) when conversion data exceed the limit set in the
high threshold register. The comparator then de-asserts when the input
signal falls below the low threshold register value.

- **setComparatorMode(mode: int)** value 0 = COMP_MODE_TRADITIONAL 1 = COMP_MODE_WINDOW, 
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

Depending on the comparator mode **TRADITIONAL** or **WINDOW** the thresholds registers mean something different.
See Comparator Mode section or datasheet for more information.

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
