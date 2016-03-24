import os, json
import tornado.ioloop
import tornado.web
import conf

SERVER_PORT = conf.SERVER['port']
DATA_PATH = conf.SERVER['data_path']

def load_addressbook():
    result = {}
    try:
        with open(DATA_PATH, 'r') as bookfile:
            result = json.loads(bookfile.read())
    except ValueError:
        pass
    finally:
        return result
    
def save_addressbook(addressbook):
    try:
        with open(DATA_PATH, 'w') as bookfile:
            data = json.dumps(addressbook)
            bookfile.write(data)
        return True
    except ValueError:
        return False

addressbook = load_addressbook()

def update_address(name, new_info):
    addressbook[name] = new_info
    return save_addressbook(addressbook)

def is_authorized(handler):
    code = handler.get_query_arguments('code')
    if len(code) > 0:
        return (code[0] == conf.SHARED_SECRET)
    else:
        return False

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if is_authorized(self):
            message = "You are authorized to view the addressbook"
            message += "\n"+json.dumps(addressbook)
            self.write(message)
            print("Main - Authorized")
        else:
            self.write("Unauthorized")
            print("Main - UNAUTHORIZED")
        print(repr(self.request))
        print(self.request.body)
        
class UpdateHandler(tornado.web.RequestHandler):
    def post(self):
        client_data = json.loads(self.request.body.decode())
        if is_authorized(self):
            print('Update - Authorized')
            client_info = {
                           'ip': self.request.remote_ip,
                           'host': client_data['host'],
                           'name': client_data['name'],
                           }
            print("IP Update Request from "+client_info['name'])
            print('    Client host : '+client_info['host'])
            print('    Client IP   : '+client_info['ip'])
            saved = update_address(client_info['name'], client_info)
            if saved:
                response = { 'result': 'success',
                            'data': 'Update saved successfully',
                            }
            else:
                response = { 'result': 'failure',
                            'data': 'Failed to save data',
                            }
        else:
            print('Update - UNAUTHORIZED')
            response = { 'result': 'failure',
                         'data': 'Unauthorized Access',
                        }
        print(repr(self.request))
        print(self.request.body)
        self.write(response)
        
def make_app():
    print('========================')
    print(' starting jksdns server ')
    print('========================')
    return tornado.web.Application([ (r'/$', MainHandler),
                                     (r'/update/$', UpdateHandler), 
                                    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(SERVER_PORT)
    tornado.ioloop.IOLoop.current().start()