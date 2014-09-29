from collections import defaultdict
from collections import deque

##########################################
#
# GRAPH
#
# Internally, the graph is represented as a dictionary. 
# This dictionary maps the ids of each node (starting at 0) to its neighbours

class Graph(object):
    

    def __init__(self):
          #members
        self.graph = None
        self.edges = None
        self.numEdges = None
        self.numVertices = None

    # Read LFR network file.
    # In the LFR file the ids start at one. we subtract 1 to let the ids start at 0.
    def readGraph(self,filename):
        
        with open (filename, "r") as f:

            # split strings into ints on whitespaces and subtract 1 from each value
            self.edges = [[(int(vertex)-1) for vertex in line.split()] for line in f.readlines()]

            self.graph = defaultdict(list)
            for edge in self.edges:
                if len(edge) != 2:
                    raise Exception("there must be exactly two entries in each line of the input graph")
                self.graph[edge[0]].append(edge[1])
        self.numVertices = len(self.graph)
        self.numEdges = 0
        for neighbours in self.graph.values():
            self.numEdges += len(neighbours)




    # Write output graph in our custom format
    # The number and nodes and edges are written in the first line, then a list of edges follow.
    def writeGraph(self, filename):
        with open (filename, "w") as f:
            f.write("{0} {1}".format(self.numVertices, self.numEdges))
            for v, neighbours in self.graph.iteritems():
                for n in neighbours:
                    f.write("\n{0} {1}".format(v, n))


    # Check connectivity by performing a dfs search.
    def isConnected(self):
        visited = set() 
        # start at node 0
        queue = deque([0])
        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                visited.add(vertex)
                for neighbour in self.graph[vertex]:
                    if neighbour not in visited:
                        queue.append(neighbour)
        return len(visited) == len(self.graph)
