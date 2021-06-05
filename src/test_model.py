from Board import Board
from GamePiece import GamePiece
from GameController import get_game_ID

pieces = []
pieces.append({"position_x":1, "position_y":5, "team":1, "king": True})
pieces.append({"position_x":1, "position_y":1, "team":1, "king": False})
pieces.append({"position_x":3, "position_y":1, "team":1, "king": False})
pieces.append({"position_x":4, "position_y":0, "team":2, "king": False})
pieces.append({"position_x":4, "position_y":4, "team":2, "king": False})
current_team = 2
player_1_email = "player1@email.com"
player_2_email = "player2@email.com"
dimension = 6
game_ID = get_game_ID(player_1_email, player_2_email)
board = Board(game_ID, dimension, player_1_email, player_2_email, pieces, current_team)
# board = Board(game_ID, dimension, player_1_email, player_2_email)

print(board)
board.checkAllMoves()
print(board.checkMoveLegal((4,2), (3,3)), " should be False")
print(board.checkMoveLegal((3,1), (4,2)), " should be False")
print(board.checkMoveLegal((3,1), (2,0)), " should be False")
print(board.checkMoveLegal((4,0), (2,2)), " should be True")
print(board.checkMoveLegal((4,4), (3,3)), " should be False")
print(board.checkMoveLegal((1,5), (0,4)), " should be False")
print("now moving")
print(board.movePiece((4,0), (2,2)), "should be 2")
print(board)
print(board.movePiece((2,2), (0,0)), "should be 1")
print(board)
print(board.movePiece((1,5), (0,4)), "should be 2")
print(board)