import board
import time
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
 
# Initialize the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)
 
# Create an ADS1115 object
ads = ADS.ADS1115(i2c)
 
# Define the analog input channel
channel = AnalogIn(ads, ADS.P0)
 
# Loop to read the analog input continuously
while True:
    print("Analog Value: ", channel.value, "Voltage: ", channel.voltage)
    time.sleep(0.2)

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