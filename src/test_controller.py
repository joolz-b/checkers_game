from GameController import load_board, create_board, update_board, delete_game
from Board import Board

pieces = []
pieces.append({"position_x":1, "position_y":5, "team":1, "king": True})
pieces.append({"position_x":1, "position_y":1, "team":1, "king": False})
pieces.append({"position_x":3, "position_y":1, "team":1, "king": False})
pieces.append({"position_x":4, "position_y":0, "team":2, "king": False})
pieces.append({"position_x":4, "position_y":4, "team":2, "king": False})
# board = Board(6, pieces)

current_team = 2
player_1_email = "player1@email.com"
player_2_email = "player2@email.com"
dimension = 6

# print(board)
print("Creating board")
board = create_board(player_1_email, player_2_email, dimension)
print(board)
current_team = board.movePiece((1,1), (2,0))
print(board)
update_board(board)
board = load_board(player_1_email, player_2_email)
print(board)
current_team = board.movePiece((4,2), (3,1))
update_board(board)
board = load_board(player_1_email, player_2_email)
print(board)
current_team = board.movePiece((2,0), (4,2))
update_board(board)
board = load_board(player_1_email, player_2_email)
print(board)

delete_game(player_1_email, player_2_email)