from communityutils import *
import os.path

graph_file = "./../data/hiphop/hiphop.edges"
community_file = "./../data/hiphop/hiphop.communities"
seed_file_start = "./../data/hiphop/hiphop_"
seed_file_end = ".seed"

if not (os.path.isfile(graph_file) and os.path.isfile(community_file)):
    raise Exception("files not found!")

graph = Graph()
graph.readGraphOurFormat(graph_file)

communities = Communities()
communities.readCommunitiesOurFormat(community_file)

for fraction in [0.05,0.1,0.15,0.2]:
    seeds = communities.generateSeeds(fraction)
    communities.writeSeedsCustom(seeds, seed_file_start+str(fraction)+seed_file_end)