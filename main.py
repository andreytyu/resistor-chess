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
address_pins = [26, 19, 13, 6]  # Replace with your actual GPIO pin numbers
enable_pin = 5  # Replace with your actual GPIO pin number


S0_PIN = 26
S1_PIN = 19
S2_PIN = 13
S3_PIN = 6



# Set up GPIO
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(address_pins + [enable_pin], GPIO.OUT)
#GPIO.setup(address_pins, GPIO.OUT)
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

# Function to select a channel on CD74HC4067
def select_channel(channel):
    GPIO.output(S0_PIN, channel & 1)
    GPIO.output(S1_PIN, channel & 2)
    GPIO.output(S2_PIN, channel & 4)
    GPIO.output(S3_PIN, channel & 8)




def set_channel(mux_channel):
    # Set the address pins based on the binary representation of the channel
    binary_channel = bin(mux_channel)[2:].zfill(4)
    for pin, value in zip(address_pins, binary_channel):
        GPIO.output(pin, int(value))
 
def enable_mux():
    GPIO.output(enable_pin, GPIO.LOW)

def disable_mux():
    GPIO.output(enable_pin, GPIO.HIGH)


# Create an ADS1115 object
ads = ADS.ADS1115(i2c, address=0x48, gain=2)
print("ADS1115 Configuration:", ads)
 
# Define the analog input channel
channel = AnalogIn(ads, ADS.P0)
#print("Analog Value:", channel.value, "Voltage:", channel.voltage) 


known_resistor_values = [1,10,47,100,1000]  # 1 kΩ resistor as an example


#4.096
def read_resistance(voltage, known_value):

    resistance = (known_value * (voltage))/ ( 2.048 - voltage + 1)
    #resistance = known_value * (5 / voltage - 1)
    return resistance

try:
    while True:
        for mux_channel in range(5):
           # enable_mux()
            select_channel(mux_channel)
            #set_channel(mux_channel)
            #voltage = channel.voltage
            #enable_mux()
            voltage = channel.voltage
            print("Known: " + str(known_resistor_values[mux_channel]))
            print("Voltage: " + str(round(voltage,3)))
            ohms = read_resistance(voltage, known_resistor_values[mux_channel])
            print("Channel {}: resistance {}".format(mux_channel, round(ohms,3)))
            print("/n")
            # Read analog value from the selected channel
            # Add your ADC reading logic here

            #disable_mux()
        print('='*20)
        time.sleep(10)

except KeyboardInterrupt:
    GPIO.cleanup()

# Loop to read the analog input continuously
#while True:
#    print("Analog Value: ", channel.value, "Voltage: ", channel.voltage)
#    time.sleep(0.2)

'''
import os
import time
import chess
import requests

chat_id = token=os.environ.get('CHAT_ID')
token = os.environ.get('BOT_TOKEN')

board = chess.Board()

board2 = ''♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟
⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
⭘ ⭘ ⭘ ⭘ ⭘ ♙ ⭘ ⭘
⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
♙ ♙ ♙ ♙ ♙ ⭘ ♙ ♙
♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖''

for move in board.legal_moves:
    board_ = board.copy()
    board_.push(move)
    if board_.unicode() == board2:
        break

text = board.unicode() + '\n\n' + move.uci() + ' was the move' + '\n\n' + board2

def send_msg(text):
   url_req = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}'
   print('trying')
   results = requests.get(url_req)
   print(results.json())

while True:
    send_msg(text)
    time.sleep(60*60)
'''
