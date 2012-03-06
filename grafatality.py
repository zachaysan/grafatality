import ujson
from pprint import pprint
from networkx import MultiDiGraph

class Grafatality(object):
    def __init__(self, filename='graph.json'):
        self.filename=filename
        self.graph = MultiDiGraph()
        self.typed_nodes = {}
        self.typed_nodes[None] = []
        try:
            self.load_file(filename)
        except IOError as e:
            print 'file "%s" does not exist, creating' % filename
        
    def handle(self, line):
        obj = ujson.loads(line)
        action = obj['action']
        if action == 'add_node':
            self.load_node(obj)
        elif action == 'add_edge':
            self.load_edge(obj)
        elif action == 'remove_edge':
            self.load_remove_edge(obj)

    def load_file(self, filename):
        f = open(filename)
        for line in f:
            self.handle(line)
        f.close()

    def listify_typed_node(self, node):
        if type(node) == list:
            node = tuple(node)
            if len(node) == 2:
                node = tuple(node)
        return node

    def load_edge(self, obj):
        data = obj.get('data', None)
        key =  obj.get('key', None)
        src_node = obj['src_node']
        dst_node = obj['dst_node']
        src_node = self.listify_typed_node(src_node)
        dst_node = self.listify_typed_node(dst_node)
        if data:
            self.graph.add_edge(src_node, dst_node, key=key, **data)
        else:
            self.graph.add_edge(src_node, dst_node, key=key)
    
    def load_remove_edge(self, obj):
        key = obj.get('key', None)
        self.graph.remove_edge(obj['src_node'], obj['dst_node'], key=key)
        
    def load_node(self, obj):
        data = obj.get('data', None)
        node = obj['node']
        node_type = None
        node = self.listify_typed_node(node)
        if data:
            self.graph.add_node(node, node_type=node_type, **data)
        else:
            self.graph.add_node(node, node_type=node_type)
    
    def add_node(self, node, node_type=None, **attr):
        if node_type:
            if not node_type in self.typed_nodes:
                self.typed_nodes[node_type] = []
            node = (node, node_type)
            self.typed_nodes[node_type].append(node)
        else:
            self.typed_nodes[None].append(node)

        data = {"action": "add_node",
                "node": node}

        if len(attr):
            data['data'] = attr
        self.append_log(data)

        return self.graph.add_node(node, **attr)

    def nodes_of_type(self, node_type=None, full=True):
        if full:
            return self.typed_nodes[node_type]
        else:
            return self.typed_nodes[node_type][0]

    def add_edge(self, src_node, dst_node, key=None, **attr):
        
        data = {"action": "add_edge",
                "src_node": src_node,
                "dst_node": dst_node}
        if len(attr):
            data['data'] = attr
        if key:
            data['key'] = key
        self.append_log(data)
        
        return self.graph.add_edge(src_node, dst_node, key=key, **attr)

    def remove_edge(self, src_node, dst_node, key):
        data = {"action": "remove_edge",
                "src_node": src_node,
                "dst_node": dst_node,
                "key": key}
        self.append_log(data)
        
        return self.graph.remove_edge(src_node, dst_node, key)

    def append_log(self,data):
        """
        This persists the data and while it may be true that 
        the logfile could be kept open indefinitely, for some reason
        this causes dataloss when running multiprocess files.
        """
        self.log = open(self.filename, 'a')
        self.log.write(ujson.encode(data))
        self.log.write("\n")
        self.log.close()


    def shutdown(self):
        self.log.close()


def main():
    """ Useful only for testing the speed at which grafatality can write """
    g = Grafatality('test_lots.js')
    foo = {"something": "important", "for": ["a","r","r","a","y","s"]}

    # This currently takes 20 seconds
    # Ideally, it should take no more than 2 seconds since before validation
    # it didn't
    for i in range(1000000):
        g.append_log(foo)
    g.shutdown()

if __name__ == '__main__':
    main()
