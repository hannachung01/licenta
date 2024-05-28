from issue import Issue
from agent import Agent
from network1 import *
from content import *
from collections import defaultdict
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Function to update the plot for each frame, where i is each iteration
def update(i):
    #print(f"Iteratie {i}: ")
    if i == 0: #iteration zero
        plt.cla()
        # Draw edges
        for node in Agent.allAgents:
            for connectedNode in node.connected:
                plt.plot([points[node.id][0], points[connectedNode.id][0]], [points[node.id][1], points[connectedNode.id][1]], zorder=1, color='gray')
        # Draw nodes
        for point in points:
            plt.plot(point[0], point[1], 'o', zorder=1, color='gray')
        # Draw agentZero     
        plt.scatter([points[agentZero.id][0]], [points[agentZero.id][1]], zorder=2, color="red")
    else:
        for affected in affectedInTurn[i]:
            #later if we want to have multiple content, we can use affected[2], different color
            recID = affected[1].id
            #print(f"recID = {recID}")    
            sendID = affected[0].id
            #print(f"sendID = {sendID}")
            
            #draw points for this iteration
            plt.scatter([points[recID][0]], [points[recID][1]], zorder=2, color=((numSteps-i)/numSteps, 0, 0)) #if we want just simple colors, do color="red"
            
            #draw edges for this iteration
            if i > 0:
                plt.plot([points[sendID][0], points[recID][0]], [points[sendID][1], points[recID][1]], zorder=2, color=((numSteps-i)/numSteps, 0, 0 )) #if we want just simple colors, do color="red"

def assignNodeColors(i):
    nodeDict = defaultdict(lambda: 'gray')
    for j in range(0, i+1):
        for k in affectedInTurn[j]:
            nodeDict[k[1].id] = ((numSteps-j)/numSteps, 0, 0) #every node k affected in turn j has this color  
    return nodeDict    
def assignEdgeColors(i):
    edgeDict = defaultdict(lambda: 'gray')
    for j in range(1, i+1):
        for k in affectedInTurn[j]:
            edgeDict[(k[0].id, k[1].id)] = ((numSteps-j)/numSteps, 0, 0) #every edge of a node k affected in turn j has this color  
            #print(f"Iteratie {i}: edge {k[0].id}, {k[1].id} added with color {(numSteps-j)/numSteps}")
    return edgeDict

def updateNx(i):
    plt.cla()
    node_color_dict=assignNodeColors(i)
    edge_color_dict=assignEdgeColors(i)
    print(f"Iteration {i}: Edge colors: {edge_color_dict}")
    nx.draw(G, pos, with_labels=True, node_color=[node_color_dict[node] for node in G.nodes()], edge_color=[edge_color_dict[edge] for edge in G.edges()])

# create issues (probably limit to 3 to visualize)
try:
    numIssues = int(input('How many issues do you want to test? (up to 3): '))
    if numIssues > 3:
        print("This simulation can only do a visualization of up to 3 issues. We'll initialize for 3 issues.")
        numIssues = 3
    elif numIssues < 1:
        print("This simulation needs at least 1 issue to run. Using 1 issue.")
        numIssues = 1
except ValueError:
    print("\nThat isn't a valid value. Using 1 issue. ")
for i in range(0, numIssues):
    print(f"Initializing issue {i+1}...")
    issueName = input("What do you want to call this issue? ")
    try:
        cust = int(input("Do you want to \n1. enter your own parameters \n2. randomly generate parameters for the issue \n3. use a neutral issue on default settings? \n"))
        if cust >= 1 and cust <= 3:
            Issue(issueName, cust)
        else:
            print("That isn't a valid selection. Will use default settings.")
            Issue(issueName, cust=3)
    except ValueError:
        print("That isn't a valid selection. Will use default settings.")
        Issue(issueName, cust=3)
        
# after creating issues, we correlate the issues
cust = 0
if numIssues > 1:
    cust = input('Would you like to 1. customize or 2. randomize correlations between issues? ')
if cust == '1':
    Issue.correlateIssues(True)
else:
    Issue.correlateIssues(False)

# create agents
numAgents = int(input("Number of agents (minim 3): "))
if numAgents < 3:
    numAgents = 3
for i in range(0, numAgents):
    n = Agent(i)
    Agent.allAgents.append(n)

# connect agents in network ...
try:
    selectedSimul = int(input('Select Network type \n 1 for Ring Lattice \n 2 for Erdos Renyi \n 3 for Watts Strogatz \n 4 for Barabasi Albert \n Answer: '))
    if selectedSimul == 1:
        print("Initializing Ring Lattice... ")
        numConnections = int(input("Number of connections:"))
        Agent.allAgents = connectRingLattice(Agent.allAgents, numConnections)
    elif selectedSimul == 2:
        print("Initializing Erdos-Renyi... ")
        probConnection = float(input("Probability of connection (0 to 1):"))
        Agent.allAgents = connectErdosRenyi(Agent.allAgents,probConnection)
    elif selectedSimul == 3:
        print("Initializing Watts-Strogatz... ")
        k = int(input("Number of connections:"))
        probRewire = float(input("Probability of reconnection (0 to 1):"))
        Agent.allAgents = connectWattsStrogatz(Agent.allAgents,k,probRewire)
    elif selectedSimul == 4:
        print("Initializing Barabasi-Albert... ")
        startingNum = int(input("Starting number of central nodes (minimum 2): "))
        if startingNum < 2:
            startingNum = 2
        Agent.allAgents = connectBarabasiAlb(Agent.allAgents,startingNum)
    else:
        raise ValueError
except ValueError:
        print("Input was not a valid choice. Choosing Barabasi-Albert... ")
        startingNum = int(input("Starting number of central nodes: "))
        Agent.allAgents = connectBarabasiAlb(Agent.allAgents,startingNum)
    
# initialize agents with a distribution of properties
Agent.initializeAgents()
#for ag in Agent.allAgents:
#    print(ag)

# initialize messages to launch in system
try:
    numMsg = int(input("How many messages do you want to launch at the start?"))
    if (numMsg < 1):
        raise ValueError
except ValueError:
    print("That is not a valid number. Switching to default of 1.")
    numMsg = 1
for i in range(0, numMsg):
    msg = Content()


'''
# number of iterations of agent actions
numSteps = int(input("Number of iterations to run simulation: "))
# maybe start with 1 piece of content, later we can add more content and interactions between them

broadcastFlag = input("Broadcasting on or off? (1 for on, 0 for off): ")
if int(broadcastFlag) == 1:
    broadcastFlag = True
else:
    broadcastFlag = False

nothingFlag = input("Do Nothing option on or off? (1 for on, 0 for off): ")
if int(nothingFlag) == 1:
    nothingFlag = True
else:
    nothingFlag = False

# debugging / displaying
#postConnections(Agent.allAgents) # for debugging
#visualizeNodes(Agent.allAgents) # for visualization with distance    
#createCircleGraph(Agent.allAgents) # Create and display the circle graph  

# run simulation
affectedInTurn = []

# iteration 0 - first generation and share 
agentZero = random.choice(Agent.allAgents)
newContent = agentZero.generate() #random agent generates content and automatically appended to allContent
affectedInTurn.append([[None, agentZero, newContent]])

# subsequent iterations
for i in range(0, numSteps+1):
    affectedInTurn.append([]) #create a new iteration in affectedInTurn list, so that affectedInTurn[i+1] will work
    # each affectedElement from list of affectedInTurn[i] is a tuple of three things: [sender, recipient, content]
    for agentAffected in affectedInTurn[i]:
        newlyAffected = agentAffected[1].decide(newContent, broadcastFlag, nothingFlag)
        affectedInTurn[i+1].extend(newlyAffected)
   
selectedVis = int(input('Select visualization type \n 1 for Network Visualization \n 2 for Ring Visualization \n Answer: '))
if selectedVis == 1: #nx visualization
    fig, ax = plt.subplots()
    G = nx.Graph()
    for node in Agent.allAgents:
        G.add_node(node.id)
    for node in Agent.allAgents:
        for destnode in node.connected:
            G.add_edge(node.id, destnode.id)
    pos = nx.spring_layout(G)
    ani = FuncAnimation(fig, updateNx, frames=range(0, numSteps+1), interval=3000, repeat=True)
    plt.show()
if selectedVis == 2: #ring visualization
    # Create a new figure and axis
    fig, ax = plt.subplots()
    numNodes = len(Agent.allAgents)
    radius = len(Agent.allAgents)  # Radius of the circle
    center = (0,0)
    points = []
    # Calculate the positions of nodes in a circle
    for i, node in enumerate(Agent.allAgents):
        angle = (2 * i * math.pi) / numNodes
        x = center[0] + radius * 1.5 * math.cos(angle)
        y = center[1] + radius * 1.5 * math.sin(angle)
        points.append([x, y])
    # Create the animation
    ani = FuncAnimation(fig, update, frames=range(0, numSteps+1), interval=1000, repeat=True)
    # Show the animation
    plt.show()
'''