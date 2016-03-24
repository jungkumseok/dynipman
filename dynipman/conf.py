import os
_base_dir = os.path.join(os.path.expanduser('~'), '.dynipman')

# Change this secret to something only you know
SHARED_SECRET = 'ThisIsNotASecureSecret'

SERVER = {
          'url': 'http://localhost:7883/',
          'port': 7883,
          'data_path': os.path.join(_base_dir, 'addressbook.json')
          }

CLIENT = {
          'name': 'my-home-ubuntu',
          'update_interval': 60
          }