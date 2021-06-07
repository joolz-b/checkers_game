from customSecrets import get_secret
from Board import Board
import boto3
from boto3.dynamodb.conditions import Attr, Or
from botocore.exceptions import ClientError

#Use this probably
def check_game_exists_with_players(player_1_email, player_2_email):
    game_ID = get_game_ID(player_1_email, player_2_email)
    return check_game_exists(game_ID)

#Use this
def is_user_in_game(game_ID, username):
    inGame = False
    board = load_board_from_ID(game_ID)
    if board and (board.getPlayer1() == username or board.getPlayer2() == username):
        inGame = True
    return inGame

#Use this
def load_board_from_players(player_1, player_2):
    game_ID = get_game_ID(player_1, player_2)
    board = load_board_from_ID(game_ID)
    return board

def load_board_from_ID(game_ID, dynamoClient=None, dynamoResource=None):
    game_dict = load_game_state(game_ID, dynamoClient, dynamoResource)
    if game_dict:
        try:
            pieces = game_dict['pieces']
            for piece in pieces:
                piece['position_x'] = int(piece['position_x'])
                piece['position_y'] = int(piece['position_y'])
                piece['team'] = int(piece['team'])
        except KeyError:
            pieces = None
        board = Board(game_dict['game_ID'], int(game_dict['dimension']), game_dict['player_1'],game_dict['player_2'], pieces, int(game_dict['current_turn']))
    else:
        board = None
    return board 

#Use this - Note: It will delete the existing game if it exists.
def create_board(player_1, player_2, dimension):
    if check_game_exists_with_players(player_1, player_2):
        delete_game(player_1, player_2)
    game_ID = get_game_ID(player_1, player_2)
    board = Board(game_ID, dimension, player_1, player_2)
    item=board.exportGame()
    put_game_state(item)
    board = load_board_from_players(player_1, player_2)
    return board

#Use this
def update_board(board):
    update_game_state(board)
    game_state = load_board_from_players(board.getPlayer1(), board.getPlayer2())
    return game_state

#Maybe Use this
def get_game_ID(player1email, player2email):
    game_id = hash(player1email + player2email)
    return game_id

def put_game_state(item, dynamoResource=None):
    table = get_games_table()
    response = table.put_item(
       Item=item
    )
    return response

def update_game_state(board):
    table = get_games_table()

    response = table.update_item(
        Key={
            'game_ID': board.getGame_ID()
        },
        UpdateExpression="set current_turn=:t, pieces=:p, winner=:w",
        ExpressionAttributeValues={
            ':t': board.getCurrentTurn(),
            ':p': board.exportPieces(),
            ':w': board.checkWinner()
        },
    )
    return response

def load_game_state(game_ID, dynamoClient=None, dynamoResource=None):
    if not dynamoClient:
       dynamoClient = boto3.client("dynamodb",
                              aws_access_key_id=get_secret("access_key_id"),
                              aws_secret_access_key=get_secret(
                                  "access_key_secret"),
                              region_name="us-east-1"
                              )
    if not dynamoResource:
        dynamoResource = boto3.resource("dynamodb",
                          aws_access_key_id=get_secret("access_key_id"),
                          aws_secret_access_key=get_secret(
                              "access_key_secret"),
                          region_name="us-east-1"
                          )
    games_table = get_games_table(dynamoClient, dynamoResource)
    try:
        response = games_table.get_item(Key={'game_ID': game_ID})
        game = response.get('Item')
    except dynamoClient.exceptions.ClientError as e:
        game = None
        print(e.response['Error']['Message'])
    return game


def get_games_table(dynamoClient = None, dynamoResource=None):
    if not dynamoClient:
       dynamoClient = boto3.client("dynamodb",
                              aws_access_key_id=get_secret("access_key_id"),
                              aws_secret_access_key=get_secret(
                                  "access_key_secret"),
                              region_name="us-east-1"
                              )
    if not dynamoResource:
        dynamoResource = boto3.resource("dynamodb",
                          aws_access_key_id=get_secret("access_key_id"),
                          aws_secret_access_key=get_secret(
                              "access_key_secret"),
                          region_name="us-east-1"
                          )
    try:
        table = dynamoResource.create_table(
            TableName='Games',
            KeySchema=[
                {
                    'AttributeName': 'game_ID',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'game_ID',
                    'AttributeType': 'N'  # Partition key
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        table.meta.client.get_waiter('table_exists').wait(TableName='Games')
    except dynamoClient.exceptions.ResourceInUseException:
        table = dynamoResource.Table('Games')
    return table

def delete_game(player_1_email, player_2_email):
    game_ID = get_game_ID(player_1_email, player_2_email)
    delete_game_ID(game_ID)

def delete_game_ID(game_ID):
    table = get_games_table()
    try:
        response = table.delete_item(
            Key={
                'game_ID': game_ID,
            }
        )
    except ClientError as e:
            raise
    else:
        return response

def check_game_exists(game_ID, dynamoClient=None):
    if not dynamoClient:
       dynamoClient = boto3.client("dynamodb",
                              aws_access_key_id=get_secret("access_key_id"),
                              aws_secret_access_key=get_secret(
                                  "access_key_secret"),
                              region_name="us-east-1"
                              )
    games_table = get_games_table()
    try:
        response = games_table.get_item(Key={'game_ID': game_ID})
        user = response.get('Item')
    except dynamoClient.exceptions.ClientError as e:
        user = None
    exists = False
    if user:
        exists= True
    return exists

def scan_users_games(username):
    games = []

    table = get_games_table()
    scan_kwargs = {
        'FilterExpression': Or(Attr('player_1').eq(username), Attr('player_2').eq(username))
    }

    done = False
    start_key = None
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_kwargs)
        game_page = response.get('Items', None)
        for game in game_page:
            games.append(game)
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None
    return games