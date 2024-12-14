import pandas as pd

# Input: Processes with Arrival Time and Burst Time
processes = {"Arrival Time": [0, 1, 3, 5, 6],
             "Burst Time": [5, 3, 6, 1, 4]}
timeQuantum = 3

# Create a DataFrame for processes
processesDF = pd.DataFrame(processes, index=["P1", "P2", "P3", "P4", "P5"])
print("Initial Processes:\n")
print(processesDF, '\n')

# Initialize variables
waitingQueue = []
output = []
currentTime = 0

print("Starting Round Robin Scheduling...\n")

# Run the scheduling loop until all processes are fully executed
while any(processesDF["Burst Time"] > 0):
    # Add newly arrived processes to the waiting queue
    for process in processesDF.index:
        if process not in waitingQueue and processesDF.loc[process, "Arrival Time"] <= currentTime and processesDF.loc[process, "Burst Time"] > 0:
            waitingQueue.append(process)
            print(f"Process {process} arrived and added to the waiting queue.")

    # If the waiting queue is empty, the CPU is idle
    if not waitingQueue:
        print(f"CPU is idle at time {currentTime}.")
        currentTime += 1
        continue

    # Dequeue the first process from the waiting queue
    currentProcess = waitingQueue.pop(0)
    print(f"\nTime {currentTime}: Process {currentProcess} dequeued. Waiting queue: {waitingQueue}")

    # Execute the process for the time quantum or its remaining burst time
    burstTime = processesDF.loc[currentProcess, "Burst Time"]
    executedTime = min(burstTime, timeQuantum)
    output.extend([currentProcess] * executedTime)
    currentTime += executedTime
    processesDF.loc[currentProcess, "Burst Time"] -= executedTime
    print(f"Process {currentProcess} executed for {executedTime} units. Remaining Burst Time: {processesDF.loc[currentProcess, 'Burst Time']}.")
    print(f"Time {currentTime}: Execution completed. Output so far: {output}")

    # Add processes arriving during this execution period to the queue
    for process in processesDF.index:
        if process not in waitingQueue and processesDF.loc[process, "Arrival Time"] > currentTime - executedTime and processesDF.loc[process, "Arrival Time"] <= currentTime and processesDF.loc[process, "Burst Time"] > 0:
            waitingQueue.append(process)
            print(f"Process {process} arrived and added to the waiting queue during execution of {currentProcess}.")

    # If the current process is not finished, re-enqueue it
    if processesDF.loc[currentProcess, "Burst Time"] > 0:
        waitingQueue.append(currentProcess)
        print(f"Process {currentProcess} re-added to the waiting queue.")

    print(f"End of Time {currentTime}: Waiting queue: {waitingQueue}")

print("\nFinal Output (Execution Order):\n")
print(output)
print("\nProcesses After Execution:\n")
print(processesDF)

