import matplotlib.pyplot as plt
import json
import numpy as np

f = open('good_run_v3.json', 'r')
results = json.load(f)


x = np.array([int(d['k1']) for _, d in results.items()])
y = np.array([int(d['k2']) for _, d in results.items()])

z_dict = {}

for _, d in results.items():

    if d['k1'] not in z_dict:
        z_dict[d['k1']] = []

    z_dict[d['k1']].append(d['result']['train'][0]['pa'])

z = np.array([l for _, l in z_dict.items()])

# X, Y = np.meshgrid(x, y)

fig = plt.figure()
ax = plt.axes(projection='3d')

ax.plot_surface(x, y, z, cmap='viridis', edgecolor='none')
ax.set_title('Optimize results')
plt.xlabel('k1')
plt.ylabel('k2')
# plt.zlabel('ll')
plt.show()
