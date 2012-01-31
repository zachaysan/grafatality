from social_network import SocialNetwork
from pprint import pprint
import commands

class SSI(object):
    def __init__(self):
        filename = 'simulation.js'
        commands.getstatusoutput("rm " + filename)
        s = SocialNetwork(filename)
        s.create_account("zach")
        s.create_account("jaco")
        s.request_friend("zach","jaco")
        s.create_account("laura")
        s.request_friend("laura", "jaco")
        s.request_friend("laura", "zach")
        s.accept_friend_req("zach", "laura")
        s.accept_friend_req("jaco", "zach")
        s.accept_friend_req("jaco", "laura")
        s.create_account("jen")
        s.create_account("andrew")
        s.request_friend("andrew", "jen")
        s.request_friend("andrew", "zach")
        s.request_friend("andrew", "jaco")
        s.accept_friend_req("zach", "andrew")
        self.s = s


if __name__ == '__main__':
    ssi = SSI()
    pprint(ssi.s.g.graph.__dict__)
