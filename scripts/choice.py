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
            percentage = random.random()
            index = random.randint(0,len(p)-1)
            if percentage <= p[index]:
                #success
                if replace:
                    output.append(a[index])
                    picked = picked + 1
                else:
                #check if element was already picked
                    if a[index] not in output:
                        output.append(a[index])
                        picked = picked + 1
        return output