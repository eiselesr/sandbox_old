
# coding: utf-8

# In[1]:


import json
import pprint


# In[2]:


import z3
#https://z3prover.github.io/api/html/z3py_8py_source.html


# In[3]:


optimizer = z3.Optimize()
optimizer.help()


# In[4]:


optimizer = z3.Optimize()
x=z3.Int('x') # (declare-const x Int)
y=z3.Int('y') #(declare-const y Int)

print(optimizer.param_descrs())
optimizer.assert_exprs(x < 2)#(assert (< x 2))
optimizer.assert_exprs((y-x)>1)#(assert (> (- y x) 1))
my_max = optimizer.maximize(x+y)#(maximize (+ x y))
my_min = optimizer.minimize(x+y)
#optimizer.set("priority", "box")
optimizer.check()#(check-sat)
print(optimizer.lower(my_min))
print(optimizer.lower(my_max))
print(optimizer.upper(my_min))
print(optimizer.upper(my_max))
print(optimizer.model())
#print(optimizer.statistics())


# In[5]:


z3.set_param(verbose=10)
optimizer = z3.Optimize()
x=z3.Int('x')#(declare-const x Int)
y=z3.Int('y')#(declare-const y Int)
optimizer.assert_exprs(x < 4)#(assert (< x 4))
optimizer.assert_exprs((y-x) < 1)#(assert (< (- y x) 1))
optimizer.assert_exprs(y < 1)#(assert (< y 1))
optimizer.assert_exprs(y>-10)


# In[6]:


my_min=optimizer.minimize(x+y)#(minimize (+ x y))


# In[7]:


optimizer.check()#(check-sat)


# In[8]:


optimizer.model()


# In[9]:


optimizer.lower(my_min)


# In[10]:


optimizer.upper(my_min)


# In[11]:


with open ('dummy_km.json') as file:
    data = json.load(file)
    
#pprint.pprint(data)


# In[12]:


data['VG1']['dependencies']['nonlocal']


# I think there needs to be a list of all resource types. I'm not sure how to guarantee the ordering otherwise. 

# In[13]:


[j for i in data for j in data[i]['resources'] ]#depth first, pull all elements 


# In[14]:


resourceTypes = set([j for i in data for j in data[i]['resources'] ])
print(resourceTypes)


# nodeList

# In[15]:


nodeList = list()
for i in data:
    if data[i]['type']=='node':
        nodeList.append(i)
print (nodeList)


# In[16]:


appList = list()
for i in data:
    if data[i]['type']=='app':
        appList.append(i)
print (appList)


# In[17]:


a2n = [ [ z3.Int("a2n_%s_%s" % (i, j)) for j in range(len(nodeList)) ]
            for i in range(len(appList)) ]
print(a2n)


# In[18]:


a2n = [ [ z3.Int("a2n_%son%s" % (i, j)) for j in nodeList ]
            for i in appList]
pprint.pprint(a2n)
print(a2n[0][2])


# matrix for resource x node matrix

# In[19]:


#build and check format for matrix of node resources
rsrc_per_node = [[z3.Int("rpn_%s_%s" %(k, j)) for j in nodeList] for k in resourceTypes]
rpn= [[data[j]['resources'][k] for j in nodeList] for k in resourceTypes]

k = 1
j = 0
pprint.pprint (rsrc_per_node)
pprint.pprint(rpn)
print("index [{}][{}] {} {}".format(k,j, rsrc_per_node[k][j], rpn[k][j]))


# In[20]:


#build and check format for matrix of app resource requirements
print ([i for i in appList])
rsrc_per_app = [[z3.Int("rpa_%s_%s" %(k, i)) for i in appList] for k in resourceTypes]

k = 1
i = 1

pprint.pprint(rsrc_per_app)
rpa= [[data[i]['resources'][k] for i in appList] for k in resourceTypes]
print("index [{}][{}] {} {}".format(k,i, rsrc_per_app[k][i], rpa[k][i]))


# In[21]:


#make sure resources match when k changes. 

k = 1
i = 0
j = 1
print("index [{}][{}] {} {}".format(k,j, rsrc_per_node[k][j], rpn[k][j]))
print("index [{}][{}] {} {}".format(k,i, rsrc_per_app[k][i], rpa[k][i]))

rpn[k][j] >= rpa[k][i]


# In[22]:


val_a2n = [ z3.Or(a2n[i][j]==0,a2n[i][j]==1) for j in range(len(nodeList))
          for i in range(len(appList)) ]
pprint.pprint(val_a2n)


# In[23]:


rsrc_constraint = [rpn[k][j] >= z3.Sum([a2n[i][j]*rpa[k][i] for i in range(len(appList))]) 
 for j in range(len(nodeList))
 for k in range(len(resourceTypes))]
rsrc_constraint


# In[24]:


md_constraint1 = [z3.Sum(a2n[0][0], a2n[0][1], a2n[0][2])==1]
md_constraint2 = [z3.Sum(a2n[1][0], a2n[1][1], a2n[1][2])==1]


vg1 = appList.index('VG1')
print(vg1)
md_all = [z3.And([a2n[vg1][node]==1 for node in range(len(nodeList))])]
print(md_all)


# In[25]:


#dependency matrix c2c
a2a = []
for app in appList:
    print(app)
    nl_deps = data[app]['dependencies']['nonlocal']
    deps = []
    for dep in appList:
        if dep in nl_deps:
            print("depends on %s" %(dep))
            deps.append(1)
        else: 
            print("does not depend on %s" %(dep))
            deps.append(0)
            
    a2a.append(deps)
print ("a2a matrix %s" %a2a)
print (a2a[appList.index('VG1')][appList.index('VG1')])
print (a2a[appList.index('VG1')][appList.index('APP2')])
print (a2a[appList.index('VG1')][appList.index('APP3')])
print(a2a[appList.index('VG1')])
#latency = []
#for node in nodeList:
#    print(node)
#    id = data[node]['id']
#    temp = []
#    for target in data[node]['latencies']:
#        lat = data[node]['latencies'][target]
#        print ("%s : %s" %(target, lat))
#        temp.append(lat)
#    latency.append(temp)
#print (latency)


# In[26]:


#dependency constraints
dependencies = list()

def DependsOn(pack, deps):
    print("deps are %s" %deps)
    return z3.And([ z3.Implies(pack, dep) for dep in deps ])

print ("appList: %s" % appList)
for app in appList:
    appi = appList.index(app)
    nl_deps = data[app]['dependencies']['nonlocal']
    print("%s non-local dependencies: %s" %(app, nl_deps))
    if nl_deps:
        #depi = [appList.index(dep) for dep in nl_deps]
        #print ("dependency index: %s" %depi)
        dependencies = [DependsOn(a2n[appi][nodej]==1,[a2n[appList.index(dep)][nodej]==1 for dep in nl_deps]) for nodej in range(len(nodeList))]
        #print (dependencies)
        test = [[a2n[appList.index(dep)][nodej]==1 for dep in nl_deps] for nodej in range(len(nodeList))]
        #print (test)
        #pre = [z3.Sum([a2n[appi][nodej] for nodej in range(len(nodeList))]) > 0]
        pre = z3.Or([a2n[appi][nodej]==1 for nodej in range(len(nodeList))])
        print("pre %s" %pre)
        post = list()
        for dep in nl_deps:            
            post.append(z3.Or([a2n[appList.index(dep)][nodej]==1 for nodej in range(len(nodeList))]))
            
            
        print("post %s" %post)
        dependencies = [DependsOn(pre, post)]
        print (dependencies)
        #z3.Or(z3.Not(pre), post)
#a2n[appi][nodej]==1, z3.Or()
#[ z3.Or(a2n[i][j]==0,a2n[i][j]==1) for j in range(len(nodeList)) for i in range(len(appList)) ]

    


# In[27]:


solver = z3.Solver()
solver.add(val_a2n + rsrc_constraint + md_all+dependencies )
pprint.pprint(val_a2n + rsrc_constraint + md_all+dependencies)


# In[28]:


solver.check()


# In[29]:


#print(appList)
placement = solver.model()
print (placement)
a2n_r = [[placement.evaluate(a2n[i][j]) for j in range (len(nodeList))] for i in range(len(appList))]
print(a2n_r)


# In[30]:


import numpy as np
import pandas as pd


# In[31]:


# two ways to build latency matrix. The first way does not guarantee the order of the first index when
#reading from the json, but does the second. The second way gurantees nothing. 
# We could do a third way that ensures the FSSNs are in order too. 
n2n = []
for node in nodeList:
    #print(node)
    id = data[node]['id']
    #print("id: %s" %id)
    temp = []    
    for n2 in nodeList:
        id2 = data[n2]['id']
        #print("id2: %s" %id2)
        lat = data[node]['latencies']['n%s%s' %(id, id2)]
        #print (lat)
        temp.append(lat)
    n2n.append(temp)
    #print (n2n)   


# In[32]:


a2n_df = pd.DataFrame(a2n, index=appList, columns=nodeList)
a2nr_df = pd.DataFrame(a2n_r, index=appList, columns=nodeList)
n2n_df = pd.DataFrame(n2n, index=nodeList, columns=nodeList)
a2a_df = pd.DataFrame(a2a, index=appList, columns=appList)
#print(placement)

print(n2n_df)
print(a2a_df)

print(a2n_df)



# In[33]:


type(z3.IntVal(1))


# In[37]:


#------------Latency-------------------------------

deployment_latency = list()
#check a2n for those apps 
for app in appList:
    nl_deps = data[app]['dependencies']['nonlocal']
    print("%s with deps: %s" %(app, nl_deps))
    if nl_deps:        
        for snode in nodeList:    
            for dep in nl_deps:
                print(dep)
                #print("works? %s" %a2n_df.iloc[1,1])
                targets = []
                for tnode in nodeList:
                    #print("source: %s" %a2n_df.loc[app,snode])
                    source = a2n_df.loc[app,snode]
                    #print(type (source))
                    target = a2n_df.loc[dep,tnode]
                    cost = (n2n_df.loc[snode,tnode]).item() # the .item() converts from numpy type to native python.
                    #print("target: %s" %a2n_df.loc[a2n_df.index[dep],tnode])
                    #print("cost: %s" %n2n_df.loc[snode,tnode])
                    lat = z3.Product(source, target, cost)
                    targets.append(lat)
                deployment_latency.append(z3.Sum(targets))

#print(deployment_latency)
latency_constraint = z3.Sum(deployment_latency)
pprint.pprint (latency_constraint)


# In[38]:


print(a2nr_df)


# In[ ]:


from functools import reduce
optimizer = z3.Optimize()
constraints = val_a2n + rsrc_constraint + md_all + dependencies
optimizer.add(constraints)
optimizer.minimize(latency_constraint)
optimizer.check()
#print(optimizer.model())
#optimizer.model()


# In[ ]:




