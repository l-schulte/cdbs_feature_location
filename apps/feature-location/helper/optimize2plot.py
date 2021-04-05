import matplotlib.pyplot as plt
import json
import numpy as np

f = open('results.json', 'r')
results = json.load(f)

x = np.array([int(d['k1']) for d in results])
y = np.array([int(d['k2']) for d in results])
z = np.array([[float(d['result']['train'][0]['pa'])] for d in results])

fig = plt.figure()
ax = plt.axes(projection='3d')

ax.scatter(x, y, z)
ax.set_title('Optimize results')
plt.show()
