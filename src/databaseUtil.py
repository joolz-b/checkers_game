import pymysql
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# creates the database
def create_database():
  run_query('create database checkers')



# creates the tables
def create_table():
  run_query('''
      create table users (
        id int not null auto_increment,
        username text,
        email text,
        password text,
        primary key (id)
      )
    '''
  )
  run_query('''
      create table results(
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
