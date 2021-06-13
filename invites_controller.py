from customSecrets import get_secret
from Board import Board
from userUtil import confirm_user_exists
import boto3
from boto3.dynamodb.conditions import Attr, Or
from botocore.exceptions import ClientError

# Use this!
def invite_user(username, invitor):
    if check_user_exists(username) == False:
        create_invite_list(username)
    add_to_invite_list(username, invitor)
        

def delete_from_invite_list(username, invitor):
    table = get_invites_table()

    response = table.update_item(
        Key={
            'username': username
        },
        UpdateExpression="DELETE invites :i",
        ExpressionAttributeValues={
            ':i': {invitor}
        },
    )
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        print(response)

def add_to_invite_list(username, invitor):
    table = get_invites_table()

    response = table.update_item(
        Key={
            'username': username
        },
        UpdateExpression="ADD #invites :i",
        ExpressionAttributeNames = {
        '#invites' : 'invites'
        },
        ExpressionAttributeValues={
            ':i': {invitor}
        },
    )
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        print(response)

def create_invite_list(username):
    table = get_invites_table()
    response = table.put_item(
       Item={"username":username, "invites":{}}
    )
    return response

def load_player_invites(username, dynamoClient=None, dynamoResource=None):
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
    invites_table = get_invites_table(dynamoClient, dynamoResource)
    returnInvites = {}
    try:
        response = invites_table.get_item(Key={'username': username})
        invites = response.get('Item')
        try:
            if invites:
                returnInvites = invites['invites']
            else:
                returnInvites = {}
        except KeyError:
            returnInvites = {}
    except dynamoClient.exceptions.ClientError as e:
        returnInvites = {}
        print(e.response['Error']['Message'])
    return returnInvites

def check_user_exists(username, dynamoClient=None):
    if not dynamoClient:
       dynamoClient = boto3.client("dynamodb",
                              aws_access_key_id=get_secret("access_key_id"),
                              aws_secret_access_key=get_secret(
                                  "access_key_secret"),
                              region_name="us-east-1"
                              )
    invites_table = get_invites_table()
    try:
        response = invites_table.get_item(Key={'username': username})
        user = response.get('Item')
    except dynamoClient.exceptions.ClientError as e:
        user = None
    exists = False
    if user:
        exists= True
    return exists

def get_invites_table(dynamoClient = None, dynamoResource=None):
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
            TableName='Invites',
            KeySchema=[
                {
                    'AttributeName': 'username',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S'  # Partition key
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        table.meta.client.get_waiter('table_exists').wait(TableName='Invites')
    except dynamoClient.exceptions.ResourceInUseException:
        table = dynamoResource.Table('Invites')
    return table