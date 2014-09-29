from collections import defaultdict
from random import sample
from math import ceil

##########################################
#
# COMMUNIY INFORMATION
#
# Community information is stored internally in two different ways:
# 
# The first is a map which maps each vertex to the communities it belongs to.
# This structure will be called "vertexToCommunities"
# 
# The second one maps each community to the vertices which are part of it
# this structure is called "communityToVertices".

class Communities(object):
	def __init__(self):
		self.vertexToCommunities = None
		self.communityToVertices = None
		self.seeds = None
		self.numberOfCommunities = None


	# Read LFR community file.
	# The input is a file which where each line consists 
	# of a nodeid and then a list of communities this node belongs to
	# Ids of nodes and communities in the LFR file start at 1, we subtract 1 to let those ids start at 0.
	# Returns vertexToCommunities and communityToVertices, as decribed above.
	def readCommunities(self,filename):
	    self.vertexToCommunities = defaultdict(list)
	    with open (filename, "r") as f:
	        belongings = [[(int(x) - 1) for x in line.split()] for line in f.readlines()]
	        for belonging in belongings:
	            self.vertexToCommunities[belonging[0]] = belonging[1:]

	    # remap value list as keys, keys as values
	    self.communityToVertices = defaultdict(list)
	    for vertex, communities in self.vertexToCommunities.iteritems():
	        for c in communities:
	            self.communityToVertices[c].append(vertex)
		self.numberOfCommunities = len(self.communityToVertices)            
	    

	# Write output community file.
	# Each line represents one community and lists all the vertices in this community.
	def writeCommunites(self, filename):
	    with open (filename, "w") as f:
	        for vertices in self.communityToVertices.values():
	            f.write(" ".join([str(x) for x in vertices]) + "\n")



	# Generate seed nodes.
	# Pick a fraction of "seedFraction" nodes from each community.
	# The number of seeds per community is at least 1 and rounded to the next bigger integer
	def generateSeeds(self, seedFraction):
	    self.seeds = set()
	    for c in self.communityToVertices:
	        if seedFraction == 0:
	            seedCount = 1
	        else:
	            seedCount = int(ceil(seedFraction * len(self.communityToVertices[c])))
	        self.seeds = self.seeds.union(sample(self.communityToVertices[c], seedCount))
	    


	# Write seed-information to file.
	def writeSeeds(self, filename):
	    with open (filename, "w") as f:
	        
	        f.write("{0} {1}".format(len(self.seeds), self.numberOfCommunities))
	        for seed in self.seeds:
	            tmp = [0] * self.numberOfCommunities
	            for community in self.vertexToCommunities[seed]:
	                tmp[community] = 1
	            f.write("\n" + str(seed) + " " + " ".join([str(x) for x in tmp]))