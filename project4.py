#Jeriel Leyble 11/15/2023 CS330-01 
import numpy as np
# Constants representing actions
FOLLOW = 1
PULL_OUT = 2
ACCELERATE = 3
PULL_IN_AHEAD = 4
PULL_IN_BEHIND = 5
DECELERATE = 6
DONE = 7

# Function to append a message to a file
def writeToFile(filepath, msg, mode='a'):
        with open(filepath, mode) as file:
            file.write(msg + '\n')
# Main function to run the simulation for a given scenario
def runSimulation(scenario):
    # Set parameters based on the chosen scenario
    scenarioTrace = [True, False][scenario - 1]
    scenarioIterations = [100, 1000000][scenario - 1]
    scenarioInterval = [1, 10000][scenario - 1]
    transitionProbability = [[0.8, 0.4, 0.3, 0.4, 0.3, 0.3, 0.8, 0.8, 0.8],
                             [0.9, 0.6, 0.3, 0.2, 0.2, 0.4, 0.7, 0.9, 0.7]][scenario - 1]
    # Initialize counters for states and transitions
    stateCount = [0] * 7
    transitionCount = [0] * 9
    # Define the output file name
    outputFile = f"scenario_{scenario}_output.txt"  # Separate file for each scenario
   
# Define function to write simulation summary to a file
    def writeSummary(textfile):
        # Calculate state and transition frequencies
        stateFrequency = [count / sum(stateCount) for count in stateCount]
        transitionFrequency = [count / sum(transitionCount) for count in transitionCount]

    # Write the calculated statistics to the file
        with open(textfile, 'a') as file:
            file.write("\nSummary:\n")
            file.write(f"scenario = {scenario}\n")
            file.write(f"trace = {scenarioTrace}\n")
            file.write(f"iterations = {scenarioIterations}\n")
            file.write("transition probabilities= " + " ".join(map(str, transitionProbability)) + "\n")
            file.write("state counts = " + " ".join(map(str, stateCount)) + "\n")
            file.write("state frequencies = " + " ".join(f"{freq:.3f}" for freq in stateFrequency) + "\n")
            file.write("transition counts = " + " ".join(map(str, transitionCount)) + "\n")
            file.write("transition frequencies = " + " ".join(f"{freq:.3f}" for freq in transitionFrequency) + "\n")
    # Define action functions for each state, which update the state count and write to the file
    def followAction():
        if scenarioTrace:
            writeToFile(outputFile,"state= 1 Follow")
        stateCount[FOLLOW - 1] += 1

    def pullOutAction():
        if scenarioTrace:
            writeToFile(outputFile, "state= 2 Pull out")
        stateCount[PULL_OUT - 1] += 1

    def accelerateAction():
        if scenarioTrace:
            writeToFile(outputFile, "state= 3 Accelerate")
        stateCount[ACCELERATE - 1] += 1

    def pullInAheadAction():
        if scenarioTrace:
            writeToFile(outputFile, "state= 4 Pull in ahead")
        stateCount[PULL_IN_AHEAD - 1] += 1

    def pullInBehindAction():
        if scenarioTrace:
            writeToFile(outputFile, "state= 5 Pull in behind")
        stateCount[PULL_IN_BEHIND - 1] += 1

    def decelerateAction():
        if scenarioTrace:
            writeToFile(outputFile, "state= 6 Decelerate")
        stateCount[DECELERATE - 1] += 1

    def doneAction():
        if scenarioTrace:
            writeToFile(outputFile, "state= 7 Done\n")
        stateCount[DONE - 1] += 1
    # Main loop for the simulation
    for i in range(scenarioIterations):
        if scenarioTrace:
            # Write the iteration number to the file
            writeToFile(outputFile, f"iteration= {i + 1}", mode='a' if i != 0 else 'w')
        # Initialize the starting state
        state = FOLLOW
        followAction()
        # Loop until the state is DONE
        while state != DONE:
            # Get random number between 0 and 1
            R = np.random.uniform(0.0, 1.0)
            # Conditional blocks to determine the next state based on the current state and random number
            # Check transitions
            if state == FOLLOW:
                if R < transitionProbability[0]:
                    transitionCount[0] += 1
                    state = PULL_OUT
                    pullOutAction()
                else:
                    state = FOLLOW
                    followAction()

            elif state == PULL_OUT:
                if R < transitionProbability[1]:
                    transitionCount[1] += 1
                    state = ACCELERATE
                    accelerateAction()
                elif R < transitionProbability[1] + transitionProbability[3]:
                    transitionCount[3] += 1
                    state = PULL_IN_BEHIND
                    pullInBehindAction()
                else:
                    state = PULL_OUT
                    pullOutAction()

            elif state == ACCELERATE:
                if R < transitionProbability[2]:
                    transitionCount[2] += 1
                    state = PULL_IN_AHEAD
                    pullInAheadAction()
                elif R < transitionProbability[2] + transitionProbability[4]:
                    transitionCount[4] += 1
                    state = PULL_IN_BEHIND
                    pullInBehindAction()
                elif R < transitionProbability[2] + transitionProbability[4] + transitionProbability[5]:
                    transitionCount[5] += 1
                    state = DECELERATE
                    decelerateAction()
                else:
                    state = ACCELERATE
                    accelerateAction()

            elif state == PULL_IN_AHEAD:
                if R < transitionProbability[8]:
                    transitionCount[8] += 1
                    state = DONE
                    doneAction()
                else:
                    state = PULL_IN_AHEAD
                    pullInAheadAction()

            elif state == PULL_IN_BEHIND:
                if R < transitionProbability[6]:
                    transitionCount[6] += 1
                    state = FOLLOW
                    followAction()
                else:
                    state = PULL_IN_BEHIND
                    pullInBehindAction()

            elif state == DECELERATE:
                if R < transitionProbability[7]:
                    transitionCount[7] += 1
                    state = PULL_IN_BEHIND
                    pullInBehindAction()
                else:
                    state = DECELERATE
                    decelerateAction()

            elif state == DONE:
                print("Error, unexpected state value=", state)
                break

            else:
                print("Error, unexpected state value=", state)
                break
        # Like a loading bar, will tell you if code is done running
        if (i + 1) % scenarioInterval == 0:
            print(".", end="")
    # After completing all iterations, write the summary to the file
    writeSummaryToFile(outputFile, scenario, stateCount, transitionCount, scenarioIterations, transitionProbability)

# New function to write summary
def writeSummaryToFile(filepath, scenario, stateCount, transitionCount, scenarioIterations, transitionProbability):
    stateFrequency = [count / sum(stateCount) for count in stateCount]
    transitionFrequency = [count / sum(transitionCount) for count in transitionCount]

    summary = "\nSummary:\n"
    summary += f"scenario = {scenario}\n"
    summary += f"trace = {'True' if scenario == 1 else 'False'}\n"
    summary += f"iterations = {scenarioIterations}\n"
    summary += "transition probabilities= " + " ".join(map(str, transitionProbability)) + "\n"
    summary += "state counts = " + " ".join(map(str, stateCount)) + "\n"
    summary += "state frequencies = " + " ".join(f"{freq:.3f}" for freq in stateFrequency) + "\n"
    summary += "transition counts = " + " ".join(map(str, transitionCount)) + "\n"
    summary += "transition frequencies = " + " ".join(f"{freq:.3f}" for freq in transitionFrequency) + "\n"

    writeToFile(filepath, summary)

# After all iterations, write the summary
runSimulation(1)
runSimulation(2)

