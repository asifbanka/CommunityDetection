import shlex, subprocess, shutil,os

#settings
numberOfNodes = 5000
k = 20
maxk = 50
t1 = 2
t2 = 1
small = True
mu_step_size = 0.1
number_overlap = 0 #number of nodes that are in more than one community
overlap_amount = 0 #the number of communities a node is in, if it is in more than one community
numberOfGraphs = 10  #the number of graphs with the same settings

#..................

#setting values that are implied by setings, don't change these
mu = mu_step_size
maxc = 0
minc = 0
communitySizePath = ""

if small:
    minc = 10
    maxc = 50
    communitySizePath = "small"
else:
    minc = 20
    maxc = 100
    communitySizePath = "big"

while (mu < 1):
    current = 1
    for i in range(0,numberOfGraphs):
        # file paths
        filepath = "./generatedGraphs/{0}N".format(numberOfNodes)+"/"+communitySizePath+"/"
        file1 = "network.dat"
        file2 = "community.dat"

        file1_new = str(numberOfNodes)+"N_"+communitySizePath+"C_"+str(mu)+"mu_"+str(number_overlap)+"on_"+str(current)+".graph"
        file2_new = str(numberOfNodes)+"N_"+communitySizePath+"C_"+str(mu)+"mu_"+str(number_overlap)+"on_"+str(current)+".communities"

        #generate one graph with the selected parameters
        subprocess.call(["./benchmark", "-N", str(numberOfNodes), "-k", str(k), "-maxk", str(maxk), "-mu", str(mu),
         "-t1", str(t1), "-t2", str(t2), "-minc", str(minc), "-maxc", str(maxc), "-on", str(number_overlap), "-om", str(overlap_amount)])

        #move the generated files to the desired location
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        os.rename("./"+file1,"./"+file1_new)
        shutil.move("./"+file1_new,filepath)

        os.rename("./"+file2,"./"+file2_new)
        shutil.move("./"+file2_new,filepath)
        current+=1
    mu += mu_step_size