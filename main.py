import board
import time
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
 
# Initialize the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# 0 - ohm meter, 1,2,3,4 - cell switchers
address_pins = {
    "ohm_meter": [26, 19, 13, 6],
    "cell_switch": [21, 20, 16, 12]
    }

# for cell switchers
enable_pins = {
    0: 5,
    1: 4
    #2:
    #3:
}

known_resistor_values = [2000,2200,5600,22000,680,560,1000,4700,10000,47000,100000,1000000]

GPIO.setmode(GPIO.BCM)
for pin in address_pins["ohm_meter"]:
    GPIO.setup(pin, GPIO.OUT)
for pin in address_pins["cell_switch"]:
    GPIO.setup(pin, GPIO.OUT)
for x in range(2):
    GPIO.setup(enable_pins[x], GPIO.OUT)


def set_channel(mux, mux_channel):
    # Set the address pins based on the binary representation of the channel
    binary_channel = bin(mux_channel)[2:].zfill(4)
    for pin, value in zip(address_pins[mux], binary_channel):
        GPIO.output(pin, int(value))
 
def enable_mux(mux):
    GPIO.output(enable_pins[mux], GPIO.LOW)

def disable_mux(mux):
    GPIO.output(enable_pins[mux], GPIO.HIGH)

# Create an ADS1115 object
ads = ADS.ADS1115(i2c, address=0x48, gain=2/3)
channel = AnalogIn(ads, ADS.P0)

def read_resistance(voltage, known_value):
    resistance = (known_value * (voltage))/ (4.9 - voltage)
    return resistance

try:
    while True:
        
        board_state = []

        for x in range(2):
            disable_mux(x)

        for cell_switch in range(2):
            
            enable_mux(cell_switch)
            
            for cell_switch_channel in range(16):

                set_channel("cell_switch", cell_switch_channel)

                fin_error = 0.5
                resistance = 0
                for mux_channel in range(12):
                # enable_mux()
                    set_channel("ohm_meter", mux_channel)
                    voltage = channel.voltage
                    ohms = read_resistance(voltage, known_resistor_values[mux_channel])
                    error = known_resistor_values[mux_channel] - ohms
                    error_percent = (known_resistor_values[mux_channel] - ohms) / known_resistor_values[mux_channel]
                    if abs(error_percent) < fin_error:
                        fin_error = abs(error_percent)
                        resistance = known_resistor_values[mux_channel]
                    #disable_mux()
                if resistance != 0:
                    board_state.append("{} Ohm, error {}%".format(resistance, round(fin_error*100,2)))
                else:
                    board_state.append("-")

            disable_mux(cell_switch)

        print(board_state)
        #time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()

# Loop to read the analog input continuously
#while True:
#    print("Analog Value: ", channel.value, "Voltage: ", channel.voltage)
#    time.sleep(0.2)
