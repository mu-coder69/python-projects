'''
An attempt to recreate wildlife population with prey and predators and try to see if achieve dynamic stabilitty

NOT WORKING
'''

import numpy as np
import matplotlib.pyplot as plt


def metric(point_1, point_2):
	return np.sqrt((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)

n = 50
m = 10

## initial population-------------------------------------------

predators = 100*np.random.rand(n, 2)
predators = predators[predators[:,0].argsort()] ## sort x coordinates from min to max
predators_sight_range = 10

prey = 100*np.random.rand(m, 2)
prey = prey[prey[:,0].argsort()] ## sort x coordinates from min to max
prey_sight_range = 15

## dist-------------------------------------------

def find_near(list_1, list_2, max_distance):
	nearest = []
	for i in range(list_2.shape[0]):
		entered_range = False
		nearest_items = []
		for j in range(list_1.shape[0]):
			if abs(list_2[i, 0] - list_1[j, 0]) <= max_distance:
				entered_range = True
				dist = metric(list_2[i], list_1[j])
				if dist <= max_distance:
					nearest_items.append([dist, i, j ])
			elif entered_range == True:
				break
		nearest_items = np.array(nearest_items)
		if nearest_items.size != 0:
			for list_ in nearest_items:
				nearest.append(list_)

	nearest = np.array(nearest)
	return nearest

# killed = find_near(predators, prey, predators_sight_range)

def eaten_by_only_one(list_):
	if list_.shape[0] >= 2:
		list_ = list_[np.unique(list_[:, 1], return_index=True, axis=0)[1].astype(int)]
	else:
		list_ = list_
	return list_

def eat_only_one(list_):
	if list_.shape[0] >= 2:
		list_ = list_[np.unique(list_[:, 2], return_index=True, axis=0)[1].astype(int)]
	else:
		list_ = list_
	return list_

# killed = eaten_by_only_one(killed)
# killed = eat_only_one(killed)

## graph-------------------------------------------

def graph_population(list_1, list_2, annotate=False):
	p_x, p_y = list_1.T
	p2_x, p2_y = list_2.T

	ax = plt.gca()
	ax.set_xlim((0, 100))
	ax.set_ylim((0, 100))
	plt.scatter(p_x, p_y)
	plt.scatter(p2_x, p2_y)

	for i in range(list_1.shape[0]):
		circle = plt.Circle((p_x[i], p_y[i]), predators_sight_range, color='b', fill=False)
		ax.annotate(str(i), (p_x[i], p_y[i]))

		ax.add_patch(circle)

	if annotate == True:
		for i in range(killed.shape[0]):
			ax.annotate(str(killed[i, 1:]), (p2_x[int(killed[i, 1])], p2_y[int(killed[i, 1])]))

	plt.show()

# print(f"Population: \nPredatosr: {predators.shape[0]} \nPrey: {prey.shape[0]}")
# graph_population(predators, prey)

## next gen-------------------------------------------

def eliminate(predators, prey, killed):
	if killed.shape[0] >= 2:
		prey = np.delete(prey, killed[:, 1].astype(int), axis=0)
		predators = predators[killed[:, 2].astype(int)]
	elif killed.shape[0] == 1:
		prey = np.delete(prey, killed[0, 1].astype(int))
		predators = predators[killed[0, 2].astype(int)]
	else:
		prey = prey
		predators = predators

	return predators, prey	

# predators, prey = eliminate(predators, prey, killed)

def next_gen(predators, prey):
	if predators.size >= 4:
		predators = np.concatenate((predators, 100*np.random.rand(predators.shape[0], 2)), axis=0)
	elif predators.size == 2:
		predators = np.array([predators, 100*np.random.rand(1, 2)])
	
	if prey.shape[0] >= 2:
		prey = np.concatenate((prey, 100*np.random.rand(prey.shape[0], 2)), axis=0)
	else:
		prey = np.ndarray(prey)
		prey = np.concatenate((prey, 100*np.random.rand(prey.shape[0], 2)), axis=0)

	predators = predators[predators[:,0].argsort()]
	prey = prey[prey[:,0].argsort()]

	return predators, prey

# predators, prey = next_gen(predators, prey)

# print(f"Population: \nPredators: {predators.shape[0]} \nPrey: {prey.shape[0]}")
# graph_population(predators, prey)

gens = 10

count = []
for i in range(gens):
	print(f"Population: \nPredators: {predators.shape[0]} \nPrey: {prey.shape[0]}")
	count.append([predators.shape[0], prey.shape[0]])
	killed = find_near(predators, prey, predators_sight_range)
	# graph_population(predators, prey, annotate=True)
	killed = eaten_by_only_one(killed)
	killed = eat_only_one(killed)
	# graph_population(predators, prey, annotate=True)
	predators, prey = eliminate(predators, prey, killed)
	predators, prey = next_gen(predators, prey)

t = [ t for t in range(len(count)) ]
count = np.array(count)

plt.plot(t, count[:,0], label="predators")
plt.plot(t, count[:,1], label="prey")
plt.legend()
plt.show()

