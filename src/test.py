from Board import Board
from GamePiece import GamePiece

pieces = []
pieces.append({"position_x":1, "position_y":5, "team":1, "king": True})
pieces.append({"position_x":1, "position_y":1, "team":1, "king": False})
pieces.append({"position_x":3, "position_y":1, "team":1, "king": False})
pieces.append({"position_x":4, "position_y":0, "team":2, "king": False})
pieces.append({"position_x":4, "position_y":4, "team":2, "king": False})
board = Board(6, pieces)

print(board)
board.checkAllMoves()
print(board.checkMoveLegal((4,2), (3,3), 1), " should be False")
print(board.checkMoveLegal((3,1), (4,2), 1), " should be True")
print(board.checkMoveLegal((3,1), (2,0), 1), " should be False")
print(board.checkMoveLegal((4,0), (2,2), 2), " should be True")
print(board.checkMoveLegal((4,4), (3,3), 2), " should be False")
print(board.checkMoveLegal((1,5), (0,4), 1), " should be True")
print("now moving")
print(board.movePiece((4,0), (2,2), 2), "should be True")
print(board)
print(board.movePiece((2,2), (0,0), 2), "should be False")
print(board)
print(board.movePiece((1,5), (0,4), 1), "should be False")
print(board)