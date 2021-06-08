from GameController import load_board_from_players, create_board, update_board, delete_game, load_board_from_ID
from Board import Board

pieces = []
pieces.append({"position_x":1, "position_y":5, "team":1, "king": True})
pieces.append({"position_x":1, "position_y":1, "team":1, "king": False})
pieces.append({"position_x":3, "position_y":1, "team":1, "king": False})
pieces.append({"position_x":4, "position_y":0, "team":2, "king": False})
pieces.append({"position_x":4, "position_y":4, "team":2, "king": False})
# board = Board(6, pieces)

current_team = 2
player_1_email = "testUser@test.com"
player_2_email = "player2@email.com"
dimension = 6

# print(board)
print("Creating board")
board = create_board(player_1_email, player_2_email, dimension)
print(board)
current_team = board.movePiece((1,1), (2,0))
print(board)
update_board(board)
board = load_board_from_players(player_1_email, player_2_email)
print(board)
current_team = board.movePiece((4,2), (3,1))
update_board(board)
board = load_board_from_players(player_1_email, player_2_email)
print(board)
current_team = board.movePiece((2,0), (4,2))
update_board(board)
board = load_board_from_players(player_1_email, player_2_email)

print(board)

print("Now testing load from ID")
game_ID = hash(player_1_email + player_2_email)
board = load_board_from_ID(game_ID)
print("Printing loaded from ID")
print(board)

delete_game(player_1_email, player_2_email)