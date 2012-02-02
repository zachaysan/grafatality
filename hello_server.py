import tornado.ioloop
import tornado.web
from grafatality import Grafatality
from simulated_social_interaction import SSI
import os
from pprint import pprint


s = SSI().s


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    def get(self,node):
        if not self.current_user:
            self.redirect("/approach-the-door")
            return
        friends = s.list_friends(node)
        friend_requesters = s.list_friend_req(node)
        self.render("template.html", node=node,
                    friends=friends,
                    friend_requesters=friend_requesters)
        

    def post(self,node):
        self.set_header("Content-Type", "text/html")
        friend_request = self.get_argument("friend-request")
        s.request_friend(node,friend_request)
        self.redirect("/" + node)

class MusingHandler(BaseHandler):
    def get(self,node):
        if not self.current_user:
            self.redirect("/approach-the-door")
            return
        musings = s.list_musings(node)
        self.render("musings.html", node=node, musings=musings)
        
    def post(self,node):
        self.set_header("Content-Type", "text/html")
        title = self.get_argument("title")
        body = self.get_argument("body")
        s.add_musing(node=node, title=title, body=body)
        self.redirect("/musings/" + node)
        
            
class Login(BaseHandler):
    def get(self):
        self.render("login.html")
        
    def post(self):
        self.set_header("Content-Type", "text/html")
        username = self.get_argument("callsign")
        password = self.get_argument("password")

        resp = s.check_password(username, password)
        if resp:
            self.set_secure_cookie("user", username)
            self.redirect("/" + username)
        else:
             self.redirect("/approach-the-door")

class SignUp(BaseHandler):
    def get(self):
        self.render("signup.html")

    def post(self):
        self.set_header("Content-Type", "text/html")
        username = self.get_argument("callsign")
        password = self.get_argument("password")
        email = self.get_argument("email")
        resp = s.create_account(self, username, password) == 'name taken'
        if resp == 'name taken':
            self.redirect("/learn-the-knock")
        elif resp == 'account created':
            self.set_secure_cookie("user", username)
        else:
            "error"

settings = {
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/approach-the-door",
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}
print settings['static_path']
application = tornado.web.Application([
    (r"/([a-z]+)", MainHandler),
    (r"/approach-the-door", Login),
    (r"/learn-the-knock", SignUp),
    (r"/musings/([a-z]+)", MusingHandler),
], **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
