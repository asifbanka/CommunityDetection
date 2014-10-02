import random
def choice(a, size=1, replace=True, p=None):
        if a is None:
            raise Exception("need data")

        if (size > len(a)) and (replace==False):
            raise Exception("can't sample more then there are items in the set if replace is false")

        if p is None: # default is uniform distribution
            p = list()
            for x in range(len(a)):
                p.append(float(1) / len(a))

        output = list()
        picked = 0
        while(picked < size):
            #sample from distribution
            percentage = random.random() #uniform float in [0,1)
            index = random.randint(0,len(p)-1) #unifrom integer in [0,last index of p]
            if percentage <= p[index]: #check if sampled float is below function graph of p at position index
                #success
                if replace: #if we pick with replacing add without checking if already contained
                    output.append(a[index])
                    picked = picked + 1
                else:
                #check if element was already picked
                    if a[index] not in output:
                        output.append(a[index])
                        picked = picked + 1
        return output