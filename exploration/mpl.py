import time
import board
import busio
import adafruit_mpl3115a2

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_mpl3115a2.MPL3115A2(i2c)
sensor._ctrl_reg1 = adafruit_mpl3115a2._MPL3115A2_CTRL_REG1_OS1 |adafruit_mpl3115a2._MPL3115A2_CTRL_REG1_ALT
time.sleep(.1)

total = 0
for i in range(200):
    print(i)
    total += sensor.pressure
    #time.sleep(.01)
sensor.sealevel_pressure = int(total / 200)

while True:
    print('Pressure: {}'.format(sensor.pressure))
    print('Altitude: {}'.format(sensor.altitude))
    print()

    time.sleep(.02)
