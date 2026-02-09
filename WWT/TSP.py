import numpy as np
import Costs
import time

def sum(v):
    return v[0] + v[1]

def dot2(v):
    return np.sum(v**2)

def hypot(u, v):
    return np.sqrt(dot2(u - v))

def OptimizeTSP(v):
    cities = np.array([])
    total = 10000000000.0
    ntotal = 0
    epoch = 100
    temp = 6
    for i in range(epoch):
        ntotal = 0
        ncities = np.array([0])
        step1 = 0
        g = 0
        while(not all(iiii in ncities for iiii in range(v.shape[0]))):
            x = 10000000000
            step2 = 0
            while(step2 < v.shape[0]):
                if step2 == ncities[step1]:
                    step2 += 1
                if step2 < v.shape[0]:
                    n = hypot(v[step2],v[int(ncities[step1])])
                    costs = Costs.main(ncities[g:]).cost
                    if costs[f'{step2}'][1] * n * ((10 - temp) + (np.random.rand() * 2 * temp)) / 10 < x and step2 not in ncities and costs[f'{step2}'][2] != 1:
                        x = n
                        ncities = np.append(ncities,step2)
                    if all(costs[f'{iii}'][2] == 1 or iii in ncities for iii in range(v.shape[0])):
                        ncities = np.append(ncities,0)
                        g = len(ncities) - 1
                        break
                step2 += 1
            #print(ntotal)
            step1 += 1
        l = 0
        for m in ncities:
            ntotal += hypot(v[m],v[l])
            l = m
        if ntotal < total:
            total = ntotal
            cities = ncities
    print(f"Total Distance: {total}\nItinerary: ",end="")
    for city in cities:
        print(city,"-> ", end="")
    print("end\n=====================================================================================================================================================================================================================================================================================================")

def main():
    map = np.array([[-1.95,4.85],[1.7,4.8],[1.02,2.64],[-0.46,3.72],[-2.4,2.23],[-0.83,1.6]])
    print(f"=====================================================================================================================================================================================================================================================================================================\nList of City Positions: {map}")
    OptimizeTSP(map)
    
main()