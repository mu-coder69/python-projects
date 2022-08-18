'''
An attempt to simulate human population

WORKS
'''

import numpy as np
import matplotlib.pyplot as plt

global_health = 0.3

class person:

    def __init__(self, expectancy=5):
        self.life = int(round(np.random.normal(expectancy, 4), 0)) if np.random.normal(expectancy, 4) > 0 else 1 ## years to live
        self.age = 0
        death_prob_pre = abs(np.random.normal(self.age, 4))
        self.death_prob = death_prob_pre/100 + (1/global_health * self.age) if death_prob_pre > 0 else 0 ## death prob each year
    
    def grow(self):
        ## increase age by one and recalculate death prob
        self.age += 1
        death_prob = abs(np.random.normal(self.age, 4))
        self.death_prob = death_prob/100 + (1/global_health * self.age) if death_prob > 0 else 0 

    def data(self):
        return [self.age, self.life, self.death_prob] ## statistic of the person
    
    def procreate(self):
        ## generate child of a person
        num_children = np.random.randint(0, 2)
        children = np.array([ person(self.life) for i in range(num_children) ])
        return children

people = np.array(  [person() for i in range(10)]  )

population = []
prom_age = []

for i in range(100):
    print(f"year number: {i}")
    print(f"people alive: {people.size}")
    population.append(people.size)
    aux = 0
    for each in people:
        each.grow()
        aux += each.life
        prob = abs(np.random.random())*100
        if int(each.life) == int(each.age) or each.death_prob >= prob:
            people = np.delete(people, np.where(people == each)[0])
    aux = aux / people.size if people.size != 0 else 0
    prom_age.append(aux)
    top = people.size
    for j in range(top):
        if np.random.choice([True, False]):
            new_people = people[j].procreate()
            people = np.concatenate((people, new_people))
    print("----------------------------------------------------------------------------")
    if people.size == 0:
        break

year = [ i for i in range(len(population)) ]

plt.plot(year, population)
plt.show()
plt.plot(year, prom_age)
plt.show()


