from neo4jrestclient import GraphDatabase

class Db(object):
    def __init__(self, url = 'http://127.0.0.1:7474/db/data/'):
        self.gdb = GraphDatabase(url)

class Node(object):
    def __init__(self, id = None, node = None, **properties):
        self._db = Db()

        if id == None and node == None:
            self._node = self._db.gdb.node(**properties)
        elif node:
            self._node = node
        else:
            self._node = self._db.gdb.node[id]

        self._props = self._node.properties

    def setProperty(self, name, val):
        self._node.properties[name] = val

    def getProperty(self, name):
        return self._node.properties.get(name)

    def setProperties(self, mapping):
        if type(mapping) != dict:
            return
        self._node.properties.update(mapping)

    def drawRelation(self, relation, node):
        self._node.relationships.create(relation, node._node)

    def getRelations(self, relation, direction):
        return map(lambda node : Node(node = node), \
                          self.relationships.outgoing(types=[relation]))

    def save(self):
        pass
