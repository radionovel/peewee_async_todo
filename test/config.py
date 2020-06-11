import os

host = os.getenv('MYSQL_HOST') or 'localhost'

config = {
    'host': host,
    'port': 33006,
    'database': 'app_test',
    'user': 'root',
    'password': 'secret'
}
