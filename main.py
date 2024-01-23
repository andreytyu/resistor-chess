import board
import time
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
 
# Initialize the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)
print("I2C addresses:", [hex(device_address) for device_address in i2c.scan()])

# Define GPIO pins for address selection (S0-S3) and enable (E)
reference_voltage = 4.9
address_pins = [26, 19, 13, 6]  # Replace with your actual GPIO pin numbers
known_resistor_values = [560,680,1000,2000,2200,4700,5600,10000,22000,47000,100000,1000000]


address_pins = {
    "ohm_meter": [26, 19, 13, 6],
    "cell_switch": [21, 20, 16, 12]
    }

# for cell switchers
enable_pins = {
    0: 23,
    1: 24
    #2:
    #3:
}

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
#GPIO.setup(23, GPIO.OUT)
#GPIO.setup(24, GPIO.OUT)


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
print("ADS1115 Configuration:", ads)
 
# Define the analog input channel
channel = AnalogIn(ads, ADS.P0)
#print("Analog Value:", channel.value, "Voltage:", channel.voltage) 

def read_resistance(voltage, known_value):

    #resistance = (known_value * (voltage))/ (5 - voltage)
    resistance = (known_value * (voltage))/ (reference_voltage - voltage)
    #resistance = known_value * (5 / voltage - 1)
    return resistance

try:
    while True:
        start_time = time.time()
        cells = []

        for cell in range(16):

            set_channel("cell_switch", cell)
            fin_error = 0.5
            resistance = 0
            for mux_channel in range(12):

                set_channel("ohm_meter", mux_channel)
                voltage = channel.voltage

                ohms = read_resistance(voltage, known_resistor_values[mux_channel])
                error = known_resistor_values[mux_channel] - ohms
                error_percent = round((known_resistor_values[mux_channel] - ohms) / known_resistor_values[mux_channel] * 100, 1)
                error_percent = (known_resistor_values[mux_channel] - ohms) / known_resistor_values[mux_channel]
                if abs(error_percent) < fin_error:
                    fin_error = abs(error_percent)
                    resistance = known_resistor_values[mux_channel]

            if resistance != 0:
                cells.append("{}: {} Ohm, error {}%".format(cell, resistance, round(fin_error*100,2)))
        end_time = time.time()
            #else:
            #    cells.append("{}: o".format(cell))
        print(cells)
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time} seconds")
        print('='*10)

except KeyboardInterrupt:
    GPIO.cleanup()

