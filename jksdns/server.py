import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("This is Server Main")
        print("Main")
        print(self.request.body)
        
class UpdateHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Accessed Update Handler")
        print("Update")
        print(self.request.body)
        
    def post(self):
        print("Update")
        print(self.request.body)
        print(repr(self.request))
        
        response = { 'result': "Accessed Update Handler",
                     'data': "Here you go buddy",
                    }
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
    app.listen(8010)
    tornado.ioloop.IOLoop.current().start()