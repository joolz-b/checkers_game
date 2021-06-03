from secrets import get_secret
from Board import Board

def get_board(gameId, dynamoClient, dynamoResource):
    game_dict = load_game_state(gameId, dynamoClient, dynamoResource)
    try:
        pieces = game_dict['pieces']
    except KeyError:
        pieces = None
    board = Board(game_dict['dimension'], pieces)
    return board


def load_game_state(gameId, dynamoClient, dynamoResource):
    games_table = get_games_table(dynamoClient, dynamoResource)
    try:
        response = games_table.get_item(Key={'gameID': gameId})
        game = response.get('Item')
    except dynamoClient.exceptions.ClientError as e:
        game = None
        print(e.response['Error']['Message'])
    return game


def get_games_table(dynamoClient, dynamoResource):
    try:
        table = dynamoClient.create_table(
            TableName='Games',
            KeySchema=[
                {
                    'AttributeName': 'gameID',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'gameID',
                    'AttributeType': 'S'  # Partition key
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
    except dynamoClient.exceptions.ResourceInUseException:
        table = dynamoResource.Table('Games')
    return table

