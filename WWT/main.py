import subprocess
import Costs
import numpy as np
import os
data, tmp = os.pipe()
cities = np.array([[-1.95,4.85],[1.7,4.8],[1.02,2.64],[-0.46,3.72],[-2.4,2.23],[-0.83,1.6]])
string = ""
for city in cities:
    if np.all(city != cities[5]):
        string = string + f"1 {city[0]} {city[1]} "
    else:
        string = string + f"0 {city[0]} {city[1]} "
os.write(tmp, bytes(string,"utf-8"))
os.close(tmp)
out = subprocess.check_output('cd ./WWT && g++ -std=c++20 TSP.cpp -o TSP && ./TSP', stdin=data, shell=True)
print(out.decode())