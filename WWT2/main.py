import csv

# TODO: Reset early weight coefficient when unloading
# TODO: Early weight coefficient could be changed to a bias to collect lighter items near the weight limit

# Parameters
path = [0, 1, 3, -1, 2, 4, 5]
loadingTimeCoefficient = 0.1 # Determines how much the weight of future boxes affects the loading time and increases the cost
unloadingTimeCoefficient = 0.1 # Determines how the weight of future boxes affects the unloading time and increases the cost
weightSlowDownMultiplier = 0.01 # Determines how much the slowness caused by the current weight will increase the cost
earlyWeightCoefficient = 1 # Determines how much the algorithm is biased towards getting heavy boxes early
prioritizationCoefficient = -0.1 # Determines decrease in cost due to a box being prioritized
weightLimit = 100 # Weight limit of the fork lift
volumeLimit = 250 # Volume limit of the fork lift

# Extra cost function
def extraCosts(currentPath, boxData):
    # Get weight from previous boxes
    totalCurrentWeight = 0
    totalCurrentVolume = 0
    for visitedBox in currentPath:
        for box in boxData:
            if visitedBox == int(box[0]):
                totalCurrentWeight += int(box[1])
                totalCurrentVolume += int(box[2])

        # Check if items were dropped off
        if visitedBox == -1:
            totalCurrentWeight = 0
            totalCurrentVolume = 0

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

                # Get cost decrease of prioritization
                nextBoxCosts[boxId][0] += int(box[2]) * prioritizationCoefficient

                # Check if getting another box crosses the weight or volume limit
                if int(box[1]) + totalCurrentWeight > weightLimit or int(box[2]) + totalCurrentVolume > volumeLimit:
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
with open("/Users/noahc/Desktop/WWT/boxes.csv", "r") as csvFile:
    csvRaw = csv.reader(csvFile)
    for line in csvRaw:
        boxData.append(line)
boxData = boxData[1:]

# Get extra costs
for i in range(len(path)):
    cost = extraCosts(path[:i + 1], boxData)
    print(cost)
