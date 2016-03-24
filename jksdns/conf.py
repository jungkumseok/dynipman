import os
_base_dir = os.path.dirname(os.path.abspath(__file__))

SHARED_SECRET = 'YOUNEVERKNOWWHATYOUWANT'

SERVER = {
          'url': 'http://192.168.0.73:7883/',
          'port': 7883,
          'data_path': os.path.join(_base_dir, 'addressbook.json') 
          }

CLIENT = {
          'name': 'jks-xeon-home',
          }