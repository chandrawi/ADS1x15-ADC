from smbus2 import SMBus
import time

# ADS1x15 default i2c address
I2C_address    = 0x48

# General ADS1x15 family ADC class
class ADS1x15:

    # ADS1x15 register address
    CONVERSION_REG = 0x00
    CONFIG_REG     = 0x01
    LO_THRESH_REG  = 0x02
    HI_THRESH_REG  = 0x03

    # Input multiplexer configuration
    INPUT_DIFF_0_1 = 0
    INPUT_DIFF_0_3 = 1
    INPUT_DIFF_1_3 = 2
    INPUT_DIFF_2_3 = 3
    INPUT_SINGLE_0 = 4
    INPUT_SINGLE_1 = 5
    INPUT_SINGLE_2 = 6
    INPUT_SINGLE_3 = 7

    # Programmable gain amplifier configuration
    GAIN_6_144V = 0
    GAIN_4_096V = 1
    GAIN_2_048V = 2
    GAIN_1_024V = 3
    GAIN_0_512V = 4
    GAIN_0_256V = 5

    # Device operating mode configuration
    MODE_CONTINUE = 0
    MODE_SINGLE   = 1

    # Data rate configuration
    DR_ADS1015_128  = 0
    DR_ADS1015_250  = 1
    DR_ADS1015_490  = 2
    DR_ADS1015_920  = 3
    DR_ADS1015_1600 = 4
    DR_ADS1015_2400 = 5
    DR_ADS1015_3300 = 6
    DR_ADS1115_8    = 0
    DR_ADS1115_16   = 1
    DR_ADS1115_32   = 2
    DR_ADS1115_64   = 3
    DR_ADS1115_128  = 4
    DR_ADS1115_250  = 5
    DR_ADS1115_475  = 6
    DR_ADS1115_860  = 7

    # Comparator configuration
    COMP_MODE_TRADITIONAL = 0
    COMP_MODE_WINDOW      = 1
    COMP_POL_LOW          = 0
    COMP_POL_HIGH         = 1
    COMP_LAT_LATCH        = 0
    COMP_LAT_NON_LATCH    = 1
    COMP_QUE_ONE          = 0
    COMP_QUE_TWO          = 1
    COMP_QUE_FOUR         = 2
    COMP_QUE_DISABLE      = 3

    # I2C object from smbus library
    i2c = SMBus(1)

    # I2C address
    _address = I2C_address

    # Default config register
    _config = 0x8583

    # Default conversion delay
    _conversionDelay = 8

    # Maximum input port
    _maxPorts = 4

    # Default conversion lengths
    _adcBits = 16

    # Constructor with SMBus ID and I2C address input
    def __init__(self, busId, address = I2C_address) :
        self.i2c = SMBus(busId)
        self._address = address
        # Store initial config resgister to config property
        self._config = self.readRegister(self.CONFIG_REG)

    # Write 16-bit integer to an address pointer register
    def writeRegister(self, address, value) :
        registerValue = [(value >> 8) & 0xFF, value & 0xFF]
        self.i2c.write_i2c_block_data(self._address, address, registerValue)

    # Read 16-bit integer value from an address pointer register
    def readRegister(self, address) :
        registerValue = self.i2c.read_i2c_block_data(self._address, address, 2)
        return (registerValue[0] << 8) + registerValue[1]

    # Set input multiplexer configuration
    def setInput(self, input) :
        # Filter input argument
        if input < 0 or input > 7 : inputRegister = 0x0200
        else : inputRegister = input << 12
        # Masking input argument bits (bit 12-14) to config register
        self._config = (self._config & 0x8FFF) | inputRegister
        self.writeRegister(self.CONFIG_REG, self._config)

    # Get input multiplexer configuration
    def getInput(self) :
        return (self._config & 0x7000) >> 12

    # Set programmable gain amplifier configuration
    def setGain(self, gain) :
        # Filter gain argument
        if gain < 0 or gain > 7 : gainRegister = 0x0200
        else : gainRegister = gain << 9
        # Masking gain argument bits (bit 9-11) to config register
        self._config = (self._config & 0xF1FF) | gainRegister
        self.writeRegister(self.CONFIG_REG, self._config)

    # Get programmable gain amplifier configuration
    def getGain(self) :
        return (self._config & 0x0E00) >> 9

    # Set device operating mode configuration
    def setMode(self, mode) :
        # Filter mode argument
        if mode == 0 : modeRegister = 0x0000
        else : modeRegister = 0x0100
        # Masking mode argument bit (bit 8) to config register
        self._config = (self._config & 0xFEFF) | modeRegister
        self.writeRegister(self.CONFIG_REG, self._config)

    # Get device operating mode configuration
    def getMode(self) :
        return (self._config & 0x0100) >> 8

    # Set data rate configuration
    def setDataRate(self, dataRate) :
        # Filter dataRate argument
        if dataRate < 0 or dataRate > 7 : dataRateRegister = 0x0080
        else : dataRateRegister = dataRate << 5
        # Masking dataRate argument bits (bit 5-7) to config register
        self._config = (self._config & 0xFF1F) | dataRateRegister
        self.writeRegister(self.CONFIG_REG, self._config)

    # Get data rate configuration
    def getDataRate(self) :
        return (self._config & 0x00E0) >> 5

    # Set comparator mode configuration
    def setComparatorMode(self, comparatorMode) :
        # Filter comparatorMode argument
        if comparatorMode == 1 : comparatorModeRegister = 0x0010
        else : comparatorModeRegister = 0x0000
        # Masking comparatorMode argument bit (bit 4) to config register
        self._config = (self._config & 0xFFEF) | comparatorModeRegister
        self.writeRegister(self.CONFIG_REG, self._config)

    # Get comparator mode configuration
    def getComparatorMode(self) :
        return (self._config & 0x0010) >> 4

    # Set comparator polarity configuration
    def setComparatorPolarity(self, comparatorPolarity) :
        # Filter comparatorPolarity argument
        if comparatorPolarity == 1 : comparatorPolarityRegister = 0x0008
        else : comparatorPolarityRegister = 0x0000
        # Masking comparatorPolarity argument bit (bit 3) to config register
        self._config = (self._config & 0xFFF7) | comparatorPolarityRegister
        self.writeRegister(self.CONFIG_REG, self._config)

    # Get comparator polarity configuration
    def getComparatorPolarity(self) :
        return (self._config & 0x0008) >> 3

    # Set comparator polarity configuration
    def setComparatorLatch(self, comparatorLatch) :
        # Filter comparatorLatch argument
        if comparatorLatch == 1 : comparatorLatchRegister = 0x0004
        else : comparatorLatchRegister = 0x0000
        # Masking comparatorPolarity argument bit (bit 2) to config register
        self._config = (self._config & 0xFFFB) | comparatorLatchRegister
        self.writeRegister(self.CONFIG_REG, self._config)

    # Get comparator polarity configuration
    def getComparatorLatch(self) :
        return (self._config & 0x0004) >> 2

    # Set comparator queue configuration
    def setComparatorQueue(self, comparatorQueue) :
        # Filter comparatorQueue argument
        if comparatorQueue < 0 or comparatorQueue > 3 : comparatorQueueRegister = 0x0002
        else : comparatorQueueRegister = comparatorQueue
        # Masking comparatorQueue argument bits (bit 0-1) to config register
        self._config = (self._config & 0xFFFC) | comparatorQueueRegister
        self.writeRegister(self.CONFIG_REG, self._config)

    # Get comparator queue configuration
    def getComparatorQueue(self) :
        return (self._config & 0x0003)

    # Set low threshold for voltage comparator
    def setComparatorThresholdLow(self, threshold) :
        self.writeRegister(self.LO_THRESH_REG, threshold)

    # Get voltage comparator low threshold
    def getComparatorThresholdLow(self) :
        threshold = self.readRegister(self.LO_THRESH_REG)
        if threshold >= 32768 : threshold = threshold - 65536
        return threshold

    # Set high threshold for voltage comparator
    def setComparatorThresholdHigh(self, threshold) :
        self.writeRegister(self.HI_THRESH_REG, threshold)

    # Get voltage comparator high threshold
    def getComparatorThresholdHigh(self) :
        threshold = self.readRegister(self.HI_THRESH_REG)
        if threshold >= 32768 : threshold = threshold - 65536
        return threshold

    # Check if device currently not performing conversion
    def isReady(self) :
        value = self.readRegister(self.CONFIG_REG)
        return (value & 0x8000)

    # Private method for starting a single-shot conversion
    def __requestADC(self, input) :
        self.setInput(input)
        # Set single-shot conversion start (bit 15)
        if self._config & 0x0100 :
            self.writeRegister(self.CONFIG_REG, self._config | 0x8000)

    # Get ADC value with current configuration
    def getADC(self) :
        t = time.time()
        # Wait conversion process finish or reach timeout
        while not self.isReady() and (time.time() - t) < self._conversionDelay :
            pass
        value = self.readRegister(self.CONVERSION_REG)
        # Shift bit based on ADC bits and change 2'complement negative value to negative integer
        value = value >> (16 - self._adcBits)
        if value >= (2 ** (self._adcBits - 1)) : value = value - (2 ** (self._adcBits))
        return value

    # Request single-shot conversion of a pin to ground
    def requestADC(self, pin) :
        if (pin >= self._maxPorts or pin < 0) : return 0
        self.__requestADC((pin << 12) + 4)

    # Get ADC value of a pin
    def readADC(self, pin) :
        self.requestADC(pin)
        return self.getADC()

    # Request single-shot conversion between pin 0 and pin 1
    def requestADC_Differential_0_1(self) :
        self.__requestADC(0x0000)

    # Get ADC value between pin 0 and pin 1
    def readADC_Differential_0_1(self) :
        self.requestADC_Differential_0_1()
        return self.getADC()

    # Get maximum voltage conversion range
    def getMaxVoltage(self) :
        if self._config & 0x0E00 == 0x0000 : return 6.144
        elif self._config & 0x0E00 == 0x0100 : return 4.096
        elif self._config & 0x0E00 == 0x0200 : return 2.048
        elif self._config & 0x0E00 == 0x0400 : return 1.024
        elif self._config & 0x0E00 == 0x0800 : return 0.512
        else : return 0.256

    # Transform an ADC value to nominal voltage
    def toVoltage(self, value) :
        volts = self.getMaxVoltage() * value
        return volts / ((2 ** (self._adcBits - 1)) - 1)

# ADS1013 class derifed from general ADS1x15 class
class ADS1013(ADS1x15) :

    # Constructor with SMBus ID and I2C address input and configuration for ADS1013
    def __init__(self, busId, address = I2C_address) :
        self.i2c = SMBus(busId)
        self._address = address
        self._conversionDelay = 2
        self._maxPorts = 1
        self._adcBits = 12
        # Store initial config resgister to config property
        self._config = self.readRegister(self.CONFIG_REG)

# ADS1014 class derifed from general ADS1x15 class
class ADS1014(ADS1x15) :

    # Constructor with SMBus ID and I2C address input and configuration for ADS1014
    def __init__(self, busId, address = I2C_address) :
        self.i2c = SMBus(busId)
        self._address = address
        self._conversionDelay = 2
        self._maxPorts = 1
        self._adcBits = 12
        # Store initial config resgister to config property
        self._config = self.readRegister(self.CONFIG_REG)

# ADS1015 class derifed from general ADS1x15 class
class ADS1015(ADS1x15) :

    # Constructor with SMBus ID and I2C address input and configuration for ADS1015
    def __init__(self, busId, address = I2C_address) :
        self.i2c = SMBus(busId)
        self._address = address
        self._conversionDelay = 2
        self._maxPorts = 4
        self._adcBits = 12
        # Store initial config resgister to config property
        self._config = self.readRegister(self.CONFIG_REG)

    # Request single-shot conversion between pin 0 and pin 3
    def requestADC_Differential_0_3(self) :
        self.__requestADC(0x1000)

    # Get ADC value between pin 0 and pin 3
    def readADC_Differential_0_3(self) :
        self.requestADC_Differential_0_3()
        return self.getADC()

    # Request single-shot conversion between pin 1 and pin 3
    def requestADC_Differential_1_3(self) :
        self.__requestADC(0x2000)

    # Get ADC value between pin 1 and pin 3
    def readADC_Differential_1_3(self) :
        self.requestADC_Differential_1_3()
        return self.getADC()

    # Request single-shot conversion between pin 2 and pin 3
    def requestADC_Differential_2_3(self) :
        self.__requestADC(0x3000)

    # Get ADC value between pin 2 and pin 3
    def readADC_Differential_2_3(self) :
        self.requestADC_Differential_2_3()
        return self.getADC()

# ADS1113 class derifed from general ADS1x15 class
class ADS1113(ADS1x15) :

    # Constructor with SMBus ID and I2C address input and configuration for ADS1113
    def __init__(self, busId, address = I2C_address) :
        self.i2c = SMBus(busId)
        self._address = address
        self._conversionDelay = 8
        self._maxPorts = 1
        self._adcBits = 16
        # Store initial config resgister to config property
        self._config = self.readRegister(self.CONFIG_REG)

# ADS1114 class derifed from general ADS1x15 class
class ADS1114(ADS1x15) :

    # Constructor with SMBus ID and I2C address input and configuration for ADS1114
    def __init__(self, busId, address = I2C_address) :
        self.i2c = SMBus(busId)
        self._address = address
        self._conversionDelay = 8
        self._maxPorts = 1
        self._adcBits = 16
        # Store initial config resgister to config property
        self._config = self.readRegister(self.CONFIG_REG)

# ADS1115 class derifed from general ADS1x15 class
class ADS1115(ADS1x15) :

    # Constructor with SMBus ID and I2C address input and configuration for ADS1115
    def __init__(self, busId, address = I2C_address) :
        self.i2c = SMBus(busId)
        self._address = address
        self._conversionDelay = 8
        self._maxPorts = 4
        self._adcBits = 16
        # Store initial config resgister to config property
        self._config = self.readRegister(self.CONFIG_REG)

    # Request single-shot conversion between pin 0 and pin 3
    def requestADC_Differential_0_3(self) :
        self.__requestADC(0x1000)

    # Get ADC value between pin 0 and pin 3
    def readADC_Differential_0_3(self) :
        self.requestADC_Differential_0_3()
        return self.getADC()

    # Request single-shot conversion between pin 1 and pin 3
    def requestADC_Differential_1_3(self) :
        self.__requestADC(0x2000)

    # Get ADC value between pin 1 and pin 3
    def readADC_Differential_1_3(self) :
        self.requestADC_Differential_1_3()
        return self.getADC()

    # Request single-shot conversion between pin 2 and pin 3
    def requestADC_Differential_2_3(self) :
        self.__requestADC(0x3000)

    # Get ADC value between pin 2 and pin 3
    def readADC_Differential_2_3(self) :
        self.requestADC_Differential_2_3()
        return self.getADC()
