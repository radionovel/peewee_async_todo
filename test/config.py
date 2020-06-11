import os

host = os.getenv('MYSQL_HOST') or 'localhost'
port = os.getenv('MYSQL_PORT') or 33006

config = {
    'host': host,
    'port': port,
    'database': 'app_test',
    'user': 'root',
    'password': 'secret'
}
