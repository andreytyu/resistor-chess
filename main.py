import board
import time
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
 
# Initialize the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)
print("I2C addresses:", [hex(device_address) for device_address in i2c.scan()])

ads = ADS.ADS1115(i2c, address=0x48, gain=2/3)
ads.mode = 0
ads.data_rate = 860

# Define GPIO pins for address selection (S0-S3) and enable (E)
reference_voltage = 4.9
address_pins = [26, 19, 13, 6]  # Replace with your actual GPIO pin numbers
known_resistor_values = [560,680,1000,2000,2200,4700,5600,10000,22000,47000,100000,1000000]

address_pins = {
    "ohm_meter": [26, 19, 13, 6],
    "cell_switch": [21, 20, 16, 12]
    }

# for cell switchers

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
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)


def set_channel(mux, mux_channel):
    # Set the address pins based on the binary representation of the channel
    binary_channel = bin(mux_channel)[2:].zfill(4)
    for pin, value in zip(address_pins[mux], binary_channel):
        GPIO.output(pin, int(value))

# Define the analog input channel
channels = [AnalogIn(ads, x) for x in [ADS.P0,ADS.P1,ADS.P2,ADS.P3]]

def calc_resistance(voltage, known_value):
    resistance = (known_value * voltage)/(reference_voltage - voltage)
    return resistance

def calc_resistance_error(voltage, known_value):
    resistance = (known_value * voltage)/(reference_voltage - voltage)
    ohms = calc_resistance(voltage, known_value)
    error = (known_value - ohms) / known_value
    return resistance

try:
    while True:
        start_time = time.time()
        board = {}

        for cell in range(16):

            errors = {0:0.5,1:0.5,2:0.5,3:0.5}
            values = {0:0,1:0,2:0,3:0}
            set_channel("cell_switch", cell)
            
            for mux_channel in range(12):
                set_channel("ohm_meter", mux_channel)
                time.sleep(0.0035)
                for i, channel in enumerate(channels):
                    board[channel] = {}
                    voltage = channel.voltage
                    error = calc_resistance_error(voltage, known_resistor_values[mux_channel])
                    if abs(error) < errors[i]:
                        errors[i] = abs(error)
                        values[i] = known_resistor_values[mux_channel]
                if values[i] != 0:
                    board[channel][cell] = "{}: {} Ohm, error {}%".format(cell, values[i], round(errors[i]*100,2))
                errors[i] = 0.5
                values[i] = 0
        print(board)
        print("\n")
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time} seconds")
        print('='*10)

except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    ads.mode = 256
    ads.stop_continuous_mode()
