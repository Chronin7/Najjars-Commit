import random
rangee=(-5,5)
x=10
y=10
e=[]
for i in range(x):
    o=[]
    for z in range(y):
        o.append(random.uniform(rangee[0],rangee[1]))
    e.append(o)
print(e)