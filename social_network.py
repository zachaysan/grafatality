from grafatality import Grafatality
from pprint import pprint
import commands
import bcrypt

class SocialNetwork(object):
    def __init__(self, filename='social_network.js'):
        self.g = Grafatality(filename)

    def create_account(self, username, password, email):
        if username in self.g.graph.node:
            return "name taken"
        else:
            password_hash = bcrypt.hashpw((password + username + "saltybaconi$fantastic"), bcrypt.gensalt(5))
            self.g.add_node(username, password_hash=password_hash, email=email)
            return "account created"

    def check_password(self, username, password):
        password_hash = self.g.graph.node[username]['password_hash']
        return bcrypt.hashpw(password + username + "saltybaconi$fantastic",
                             password_hash) == password_hash
    
    def list_friends(self, node):
        print node
        for dst in self.g.graph[node]:
            if 'friend' in self.g.graph[node][dst]:
                yield dst

    def request_friend(self, node1, node2):
        if node2 in list(self.list_friends(node1)):
            return "you already have that person as a friend"
        elif node1 in list(self.list_friend_req(node2)):
            return "you already requested being friends, creeper"
        self.g.add_edge(node2, node1, key='request_friend', exists=True)

    def accept_friend_req(self, node1, node2):
        if 'request_friend' in self.g.graph[node1][node2]:
            self.g.remove_edge(node1, node2, 'request_friend')
            self.add_friend(node1, node2)
        
    def list_friend_req(self, node):
        for requester in self.g.graph[node]:
            if 'request_friend' in self.g.graph[node][requester]:
                yield requester
                
    def yield_edges(self,node, edge_attr):
        for (src,dst,data) in self.g.graph.edges(node, data=True):
            for edge in data:
                if edge == edge_attr:
                    yield (src, dst, data)

    def add_friend(self, node1, node2):
        def friend(n1,n2):
            self.g.add_edge(n1, n2, key='friend', exists=True)

        if node2 not in list(self.list_friends(node1)):
            friend(node1, node2)

        if node1 not in list(self.list_friends(node2)):
            friend(node2, node1)


if __name__ == '__main__':
    s = SocialNetwork()
    pprint(s.g.graph.__dict__)
    print "---"
    commands.getstatusoutput('rm social_network.js')
    s = SocialNetwork()
    s.create_account("zach")
    s.g.add_node("laura")

    s.request_friend('zach', 'laura')
    for node in s.list_friend_req('laura'):
        print node + " requesting"
    s.accept_friend_req('laura', 'zach')
    pprint(s.g.graph.__dict__)

"""    
'edge': {u'frank': {u'zach': {0: {u'friends': u'horay'},
                               1: {u'friends': u'horay'},
                               2: {u'friends': u'horay'}}},
          u'laura': {},
          u'zach': {u'laura': {0: {u'friends': True},
                               1: {u'friends': True},
                               2: {u'friends': True}}}},
"""
