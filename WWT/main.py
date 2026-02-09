import csv
import os.path as op

# TODO: Reset early weight coefficient when unloading

# Parameters
path = [0, 1, 3, -1, 2, 4, 5]
loadingTimeCoefficient = 0.1 # Determines how much the weight of future boxes affects the loading time and increases the cost
unloadingTimeCoefficient = 0.1 # Determines how the weight of future boxes affects the unloading time and increases the cost
weightSlowDownMultiplier = 0.01 # Determines how much the slowness caused by the current weight will increase the cost
earlyWeightCoefficient = 1 # Determines how much the algorithm is biased towards getting heavy boxes early
weightLimit = 100 # Weight limit of the fork lift

# Extra cost function
def extraCosts(currentPath, boxData):
    # Get weight from previous boxes
    totalCurrentWeight = 0
    for visitedBox in currentPath:
        for box in boxData:
            if visitedBox == int(box[0]):
                totalCurrentWeight += int(box[1])

        # Check if items were dropped off
        if visitedBox == -1:
            totalCurrentWeight = 0

    # Set up next box costs
    nextBoxCosts = {}
    for box in boxData:
        nextBoxCosts[box[0]] = [0, 0, 0] # Extra cost, multiplier, does getting the box cross the weight limit

    # Add costs
    for boxId in nextBoxCosts.keys():
        for box in boxData:
            if box[0] == boxId:
                # Add slowness multiplier for weight (apply multiplier before adding extra costs)
                nextBoxCosts[boxId][1] = (totalCurrentWeight * weightSlowDownMultiplier) + 1

                # Get loading time costs
                nextBoxCosts[boxId][0] += int(box[1]) * loadingTimeCoefficient

                # Get early weight costs (bias search to force heavy boxes to be picked up early)
                nextBoxCosts[boxId][0] += (-(len(currentPath) * earlyWeightCoefficient) + (len(path) / 2)) * int(box[1])

                # Check if getting another box crosses the weight limit
                if int(box[1]) + totalCurrentWeight > weightLimit:
                    nextBoxCosts[boxId][2] = 1

    # Add costs for unloading
    nextBoxCosts["-1"] = [0, 0, 0]
    nextBoxCosts["-1"][1] = (totalCurrentWeight * weightSlowDownMultiplier) + 1
    nextBoxCosts["-1"][0] += int(box[1]) * unloadingTimeCoefficient

    # Round costs
    for boxId in nextBoxCosts.keys():
        nextBoxCosts[boxId][0] = round(nextBoxCosts[boxId][0], 3)
        nextBoxCosts[boxId][1] = round(nextBoxCosts[boxId][1], 3)

    # Output costs
    return nextBoxCosts

# Get box data
boxData = []
fpath = op.abspath(__file__)
with open(f"{fpath[:-len(op.basename(op.abspath(__file__)))]}boxes.csv", "r") as csvFile:
    csvRaw = csv.reader(csvFile)
    for line in csvRaw:
        boxData.append(line)
boxData = boxData[1:]

# Get extra costs
for i in range(len(path)):
    cost = extraCosts(path[:i + 1], boxData)
    print(cost)
