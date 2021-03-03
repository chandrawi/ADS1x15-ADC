import ADS1x15
import RPi.GPIO as GPIO

ads = ADS1x15.ADS1115(1)

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.output(26, GPIO.HIGH)

ads.setInput(7)
ads.setGain(1)
ads.setMode(1)
ads.setDataRate(7)

value = ads.readADC(0)
voltage = ads.toVoltage(value)
print(f"raw ADC: {value}\tvoltage: {voltage} V")

GPIO.cleanup()
