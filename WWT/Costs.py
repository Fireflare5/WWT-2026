import csv
import os.path as op

# TODO: Reset early weight coefficient when unloading
class main:
# Parameters
    def __init__(self,path, loadingTimeCoefficient = 0.1,unloadingTimeCoefficient = 0.1,weightSlowDownMultiplier = 0.01,earlyWeightCoefficient = 1, weightLimit = 100):
        self.path = path
        self.loadingTimeCoefficient = loadingTimeCoefficient # Determines how much the weight of future boxes affects the loading time and increases the cost
        self.unloadingTimeCoefficient = unloadingTimeCoefficient # Determines how the weight of future boxes affects the unloading time and increases the cost
        self.weightSlowDownMultiplier = weightSlowDownMultiplier # Determines how much the slowness caused by the current weight will increase the cost
        self.earlyWeightCoefficient = earlyWeightCoefficient # Determines how much the algorithm is biased towards getting heavy boxes early
        self.weightLimit = weightLimit # Weight limit of the fork lift
        # Get box data
        boxData = []
        fpath = op.abspath(__file__)
        with open(f"{fpath[:-len(op.basename(op.abspath(__file__)))]}boxes.csv", "r") as csvFile:
            csvRaw = csv.reader(csvFile)
            for line in csvRaw:
                boxData.append(line)
        boxData = boxData[1:]
        self.costs = []
        # Get extra costs
        for i in range(len(path)):
            self.cost = self.extraCosts(path[:i + 1], boxData)
            self.costs.append(self.cost)
            #print(self.cost)
# Extra cost function
    def extraCosts(self, currentPath, boxData):
        # Get weight from previous boxes
        self.totalCurrentWeight = 0
        for visitedBox in currentPath:
            for box in boxData:
                if visitedBox == int(box[0]):
                    self.totalCurrentWeight += int(box[1])

            # Check if items were dropped off
            if visitedBox == -1:
                self.totalCurrentWeight = 0

        # Set up next box costs
        nextBoxCosts = {}
        for box in boxData:
            nextBoxCosts[box[0]] = [0, 0, 0] # Extra cost, multiplier, does getting the box cross the weight limit

        # Add costs
        for boxId in nextBoxCosts.keys():
            for box in boxData:
                if box[0] == boxId:
                    # Add slowness multiplier for weight (apply multiplier before adding extra costs)
                    nextBoxCosts[boxId][1] = (self.totalCurrentWeight * self.weightSlowDownMultiplier) + 1

                    # Get loading time costs
                    nextBoxCosts[boxId][0] += int(box[1]) * self.loadingTimeCoefficient

                    # Get early weight costs (bias search to force heavy boxes to be picked up early)
                    nextBoxCosts[boxId][0] += (-(len(currentPath) * self.earlyWeightCoefficient) + (len(self.path) / 2)) * int(box[1])

                    # Check if getting another box crosses the weight limit
                    if int(box[1]) + self.totalCurrentWeight > self.weightLimit:
                        nextBoxCosts[boxId][2] = 1

        # Add costs for unloading
        nextBoxCosts["-1"] = [0, 0, 0]
        nextBoxCosts["-1"][1] = (self.totalCurrentWeight * self.weightSlowDownMultiplier) + 1
        nextBoxCosts["-1"][0] += int(box[1]) * self.unloadingTimeCoefficient

        # Round costs
        for boxId in nextBoxCosts.keys():
            nextBoxCosts[boxId][0] = round(nextBoxCosts[boxId][0], 3)
            nextBoxCosts[boxId][1] = round(nextBoxCosts[boxId][1], 3)

        # Output costs
        return nextBoxCosts

if "__main__" == __name__:
    main()
