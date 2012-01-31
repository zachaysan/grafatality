import tornado.ioloop
import tornado.web
from grafatality import Grafatality
from simulated_social_interaction import SSI
import os
from pprint import pprint
s = SSI().s

graf = Grafatality('actions.js')

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):

    def get(self,node):
#        self.write("hello")
#        self.write('<html><body><form action="/" method="post">'
#                   '<input type="text" name="message">'
#                   '<input type="submit" value="Submit">'
#                   '</form></body></html>')
        

        if not self.current_user:
            self.redirect("/approach-the-door")
            return

        items = ["Item 1", "Item 2", "Item 3"]
        friends = s.list_friends(node)
        self.render("template.html", node=node, items=items,
                    friends=friends)
        

    def post(self):
        self.set_header("Content-Type", "text/html")
        #self.write("You wrote " + self.get_argument("message"))
        self.write('friends: <br \>')
        for friend in s.list_friends(self.get_argument("message")):
            self.write(friend + '<br \>')
            
class Login(BaseHandler):
    def get(self):
        self.render("login.html")
        self.next_page = self.get_argument("next")
        
    def post(self):
        self.set_header("Content-Type", "text/html")
        username = self.get_argument("callsign")
        password = self.get_argument("password")
        if password == 'a':
            self.set_secure_cookie("user", username)
            self.redirect("/" + username)

settings = {
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/approach-the-door",
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}
print settings['static_path']
application = tornado.web.Application([
    (r"/([a-z]+)", MainHandler),
    (r"/approach-the-door", Login),
], **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
