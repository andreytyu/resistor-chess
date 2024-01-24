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

'''
# for cell switchers
enable_pins = {
    0: 5,
    1: 4
    #2:
    #3:
}
'''

known_resistor_values = [2000,2200,5600,22000,680,560,1000,4700,10000,47000,100000,1000000]

GPIO.setmode(GPIO.BCM)
for pin in address_pins["ohm_meter"]:
    GPIO.setup(pin, GPIO.OUT)
for pin in address_pins["cell_switch"]:
    GPIO.setup(pin, GPIO.OUT)

'''
for x in range(2):
    GPIO.setup(enable_pins[x], GPIO.OUT)
'''

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
channe0 = AnalogIn(ads, ADS.P0)
channel1 = AnalogIn(ads, ADS.P1)

def read_resistance(voltage, known_value):
    resistance = (known_value * (voltage))/ (4.9 - voltage)
    return resistance

try:
    while True:
        
        board_state0 = []
        board_state1 = []
        '''
        for x in range(2):
            disable_mux(x)
        

        for cell_switch in range(2):
            
            enable_mux(cell_switch)
        '''    
        for cell_switch_channel in range(16):

            set_channel("cell_switch", cell_switch_channel)

            fin_error0 = 0.5
            resistance0 = 0
            fin_error1 = 0.5
            resistance1 = 0

            for mux_channel in range(12):
            # enable_mux()
                set_channel("ohm_meter", mux_channel)
                voltage0 = channel0.voltage
                ohms0 = read_resistance(voltage0, known_resistor_values[mux_channel])
                error0 = known_resistor_values[mux_channel] - ohms0
                error_percent0 = (known_resistor_values[mux_channel] - ohms0) / known_resistor_values[mux_channel]
                if abs(error_percent0) < fin_error0:
                    fin_error0 = abs(error_percent0)
                    resistance0 = known_resistor_values[mux_channel]
                #disable_mux()
            
                voltage1 = channel1.voltage
                ohms1 = read_resistance(voltage0, known_resistor_values[mux_channel])
                error1 = known_resistor_values[mux_channel] - ohms1
                error_percent1 = (known_resistor_values[mux_channel] - ohms1) / known_resistor_values[mux_channel]
                if abs(error_percent1) < fin_error1:
                    fin_error1 = abs(error_percent1)
                    resistance1 = known_resistor_values[mux_channel]


            if resistance0 != 0:
                board_state0.append("{} Ohm, error {}%".format(resistance0, round(fin_error0*100,2)))
            else:
                board_state0.append("-")

            if resistance1 != 0:
                board_state1.append("{} Ohm, error {}%".format(resistance1, round(fin_error1*100,2)))
            else:
                board_state1.append("-")

        #disable_mux(cell_switch)

        print(board_state0)
        print(board_state1)
        print('='*10)
        #time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()

# Loop to read the analog input continuously
#while True:
#    print("Analog Value: ", channel.value, "Voltage: ", channel.voltage)
#    time.sleep(0.2)




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
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)


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

        board = {}
        for board_segment in range(2):
            
            enable_mux(board_segment)

            cells = []

            for cell in range(16):

                set_channel("cell_switch", cell)
                fin_error = 0.5
                resistance = 0
                for mux_channel in range(12):

                    set_channel("ohm_meter", mux_channel)
                    #set_channel(mux_channel)
                    #voltage = channel.voltage
                    #enable_mux()
                    voltage = channel.voltage

                    #print("Channel {}".format(mux_channel))
                    #print("Voltage: " + str(round(voltage,3)))
                    #print("Channel {}".format(mux_channel))
                    #print("Voltage: " + str(round(voltage,3)))
                    ohms = read_resistance(voltage, known_resistor_values[mux_channel])
                    error = known_resistor_values[mux_channel] - ohms
                    error_percent = round((known_resistor_values[mux_channel] - ohms) / known_resistor_values[mux_channel] * 100, 1)
                    error_percent = (known_resistor_values[mux_channel] - ohms) / known_resistor_values[mux_channel]
                    if abs(error_percent) < fin_error:
                        fin_error = abs(error_percent)
                        resistance = known_resistor_values[mux_channel]

                    #print("Known resistance: " + str(known_resistor_values[mux_channel]))
                    #print("Channel {}: resistance {}".format(mux_channel, round(ohms)))
                    #print("Error: {} Ohm, {}% ".format(error, error_percent))
                    #print("\n")
                    
                    #print("Known resistance: " + str(known_resistor_values[mux_channel]))
                    #print("Channel {}: resistance {}".format(mux_channel, round(ohms)))
                    #print("Error: {} Ohm, {}% ".format(error, error_percent))
                    #print("\n")
                    # Read analog value from the selected channel
                    # Add your ADC reading logic here

                    #disable_mux()
                #print('='*20)
                #time.sleep(5)
                if resistance != 0:
                    cells.append("{}: {} Ohm, error {}%".format(cell, resistance, round(fin_error*100,2)))
                else:
                    cells.append("{}: o".format(cell))
                #time.sleep(1)
            board[board_segment] = cells
            disable_mux(board_segment)
        print(board)
        print('='*10)

except KeyboardInterrupt:
    GPIO.cleanup()
# Loop to read the analog input continuously
#while True:
#    print("Analog Value: ", channel.value, "Voltage: ", channel.voltage)
#    time.sleep(0.2)
