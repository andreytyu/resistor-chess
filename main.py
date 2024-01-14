import os
import time
import chess
import requests

chat_id = token=os.environ.get('CHAT_ID')
token = os.environ.get('BOT_TOKEN')

board = chess.Board()

board2 = '''♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟
⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
⭘ ⭘ ⭘ ⭘ ⭘ ♙ ⭘ ⭘
⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
♙ ♙ ♙ ♙ ♙ ⭘ ♙ ♙
♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖'''

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