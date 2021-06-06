import pymysql
import os
import sys
import boto3
from flask import url_for
from dotenv import load_dotenv

load_dotenv()

# creates the database
def create_database():
  print('Creating database if it doesn\'t exist...', file=sys.stderr)
  run_query('create database if not exists checkers')



# creates the tables
def create_tables():
  run_query('''
      create table if not exists users (
        id int not null auto_increment,
        username text,
        email text,
        password text,
        primary key (id)
      )
    '''
  )
  run_query('''
      create table if not exists results(
        id int not null auto_increment,
        win int,
        lose int,
        primary key (id)
      )
    '''
  )



# drops the tables
def drop():
  run_query('drop table users')
  run_query('drop table results')



# executes an sql statement
def run_query(sql):

  connection = get_database()

  with connection:
    with connection.cursor() as cursor:
      cursor.execute(sql)
    connection.commit()



# returns the result of an executed query
def get_query(sql):
  connection = get_database()

  with connection:
    with connection.cursor() as cursor:
      cursor.execute(sql)
      return cursor.fetchall()



# establishes a connection to the server
def get_database():

  return pymysql.connect(
    host=os.environ.get('AWS_MYSQL_HOST'), 
    user=os.environ.get('AWS_MYSQL_USERNAME'), 
    password=os.environ.get('AWS_MYSQL_PASSWORD'),
    port=int(os.environ.get('AWS_MYSQL_PORT')),
    database='checkers'
  )

def download_assets():

  s3 = boto3.client('s3', 
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'), 
    region_name=os.environ.get('AWS_REGION')
  )
  
  s3.download_file('checkers-game-cc-sem1', 'cell_light.png', 'cell_light.png')
  s3.download_file('checkers-game-cc-sem1', 'cell_dark.png', 'cell_dark.png')
  s3.download_file('checkers-game-cc-sem1', 'checker_light.png', 'checker_light.png')
  s3.download_file('checkers-game-cc-sem1', 'checker_dark.png', 'checker_dark.png')

  print("Game assets downloaded from S3 bucket!\n", file=sys.stderr)

if __name__ == '__main__':

    # type of program
    if len(sys.argv) > 1:

        if sys.argv[1] == 'create_database':
          create_database()
        elif sys.argv[1] == 'create_tables':
          create_tables()
        elif sys.argv[1] == 'drop':
          drop()
        else:
            print('\nInvalid parameters... Please use:')
            print('python databaseUtil <create_database|create_tables|drop>\n')
    else:
        print('\nInvalid parameters... Please use:')
        print('python databaseUtil <create_database|create_tables|drop>\n')
