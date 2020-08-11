
 

import copy


def read(fname):  #Read file
    f = open(fname)
    l = f.readlines()
    markov = GraphicalModel()
    commands = []
    edges = []
    for line in l:
        line = line.strip().split()
        if len(line)>0 and line[0]!='c':
            commands.append(line)
    
    markov = GraphicalModel()
    #Number of Nodes 
    markov.numberofNodes = int(l[1])  
    #Number of Clique    
    markov.numberofClique = int(l[3])  
   
    #Cardinality
    markov.cardinality = commands[2]   
  
    nodeelement = ''       #To Represent each node 
    dictionary = {}        #To represent the edged from one node to other 
    markov.node = []

    #list of nodes
    for i in range(0,markov.numberofNodes):  
        markov.node.append(str(i))

    #print("Nodes :", node)
    #list of edges
    for j in range(4+markov.numberofNodes,markov.numberofClique+4):
        markov.edges.append(commands[j][1:])
    
    #assigning nodes to edges
    for nodeelement in markov.node:
        for i in range(0,markov.numberofClique-markov.numberofNodes):
            if nodeelement in markov.edges[i]:
                dictionary.setdefault(nodeelement,set([]))
                for k in markov.edges[i]:
                    dictionary[nodeelement].add(k)
                    dictionary[nodeelement] -= {nodeelement}
    
    print('Nodes with edges :')
    for key,value in dictionary.items():
        print(key, '-->', value)

    #list of factors
    markov.cpt = {}
    nodewithcpt = []
    for j in range(4,4+markov.numberofClique):
        nodewithcpt.append(commands[j][1:])
    listofcpt = commands[5+markov.numberofClique:len(commands):2]   
    return markov
    
def readevi(fename):   #Read Evidence file
    f = open(fename)
    l = f.readlines()
    
    l = [x.strip().split() for x in l]
    l = [x for x in l if len(x)>0][0] 
    
    evidenceindex = []
    evidencevalue = []
    for i in range(1,len(l),2):
        evidenceindex.append(int(l[i]))
        evidencevalue.append(int(l[i+1]))

    #print(evidenceindex)
    #print(evidencevalue)
    numberofevids = int(l[0])
    #print("Number of evidence :", numberofevids)
    

class GraphicalModel(object):
    def __init__(self):
        self.commands = []
        self.numberofnodes = 0
        self.variables = []
        self.node = []
        self.numberofClique = 0
        self.edges = []
        self.cardinalities = []
        self.CPT = {}
        self.factor = []
        self.factor_count = 0
        self.bucket = []
        self.veorder = []
        
    def __isEmpty__(self):
        if self.variables == []:
            return True
        return False
    def mindegree(self):
        veorder = []
        v = ''
        node = copy.copy(self.node)
        while not self.__isEmpty__():
            minvar = None
            minval = float('inf')
            if self.variables == []:
                for item in self.variables:
                    vcount = len(node[item].intersection(self.variables))
                    if vcount < minval:
                        minval = vcount
                        minvar = item
            veorder.append(minvar)
            if minvar in self.variables:
                self.variables.remove(minv)
                for adjecentnode in node[minvar]:
                    node[adjecentnode] = node[minvar].union(node[adjecentnode])-{adjecentnode}
        self.veorder = veorder
        return veorder

    def add(self,v): 
        self.factor.append(v)
        for j in range(len(v)):
            if v[j] in self.variables:
                self.node[v[j]] = self.node[v[j]].union(v[0:j]+v[j+1:])
            else:
                self.variables.append(v[j])
                self.node[v[j]] = set(v[0:j]+v[j+1:])

    
    def getfactor(self, v):                                       
        vfunc = [] 
        if len(self.factor) > 0:
            for i in range(len(self.factor)):
                if v in self.factor[i]:
                    nclique = tuple(self.factor[i])
                    vfunc.append(nclique)
            if len(vfunc)>0:
                return vfunc
       
        return False


    def getclique(self,v, f):                 
        nclique = set({})
        for f in f:
            nclique = nclique.union(set(f))
        nclique -= {v} 
        nclique = list(nclique)
        list(nclique).sort()
        ncliquecardinality = [self.cardianlities[x] for x in nclique]
        nclique = tuple(nclique)
        return nclique,ncliquecardinality

    def addbucket(self, f):                   
        for v in self.veorder:
            if v in f:
                self.bucket[v].append(f)
                break
    
    def removevar(self, var):                        
        vfunc = [] 
        if len(self.factor) > 0:
            for f in self.factor:
                if var in f:
                        vfunc.append(f)
        for f in vfunc:
            self.factor.remove(f)
        self.factor_count = len(self.factor)
        
    
    
    def create_bucket(self):
        self.bucket = [[] for a in range(self.numberofNodes)]
        for func in self.CPT.keys():
            self.addbucket(func)   

    #def sumproduct(self, v):
        #sum product
        
                
    #def VE(self):
        #for ve

markov = read("1.uai")
evid = readevi("1.uai.evid")
markov.mindegree()
markov.create_bucket()


