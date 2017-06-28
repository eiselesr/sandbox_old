import pprint
from pysmt.shortcuts import Symbol, Or, Equals, Int, Plus, And, get_model
from pysmt.typing import INT

c1 = 1
c2 = 2
c3 = 1
n1 = 3
n2 = 1

NO_OF_NODES = 2
NO_OF_COMPONENTS = 3

componentResrcWeights = [1,2,1]
nodeRsrc = [3,1]

c2n = [[Symbol("c2n_%s_%s" % (i, j), INT) for j in range(NO_OF_NODES)] for i in range(NO_OF_COMPONENTS)]

pprint.pprint(c2n)

# Range constraints: zero or one
domain = [Or(Equals(c2n[i][j],Int(0)), Equals(c2n[i][j],Int(1))) for j in range(NO_OF_NODES) for i in range(NO_OF_COMPONENTS)]
print ("domain")
pprint.pprint(domain)
constrain_c2n_values = And(domain)

#Each component is deployed 0 or 1 times
g_asgn_c2n = [(Plus(c2n[i][j] for j in range(NO_OF_NODES)) <= Int(1)) for i in range(NO_OF_COMPONENTS)]
print("g_asgn_c2n")
pprint.pprint(g_asgn_c2n)

#must deploy every component
md_c2n = [(Plus(c2n[i][j] for j in range(NO_OF_NODES)).Equals(Int(1))) for i in range(NO_OF_COMPONENTS)]
print("md_c2n")
pprint.pprint(md_c2n)

#deployed constraints cannont exceed resources.
rsrcConstraint = [(Plus(c2n[i][j]*componentResrcWeights[i]
    for i in range(NO_OF_COMPONENTS)) <= nodeRsrc[j]) for j in range(NO_OF_NODES)]
print("rsrc constraint")
pprint.pprint(rsrcConstraint)

formula = And(And(domain), And(rsrcConstraint), And(md_c2n))
print("formula")
pprint.pprint(formula)

model = get_model(formula)
if model:
    print(model)
else:
    print("No solution found")
