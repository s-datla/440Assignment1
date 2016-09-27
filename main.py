#!/usr/bin/python
import sys
import os.path
import graph
import collections
import heapq
import string


'''
    Main() is being used as an initial setup function that will double check that the user has
    entered the correct number of for options the command line operation as well as whether
    the file can be opened (i.e. has the user written the correct file path)
    The correct format is:

    python main.py <maze-file-txt-file> <option>
'''

def main():

    # Double check number of command line arguments

    if(len(sys.argv) < 3):
        print "Incorrect Format: \npython main.py <maze-file-txt-file> <option>"
        sys.exit(2)
    try:
        maze = str(sys.argv[1])
        searchoption = int(sys.argv[2])

        # Double check file path for the maze file

        if not(os.path.exists("./" + maze)):
            print "Incorrect file currentPath for maze file, retype"
            sys.exit(2)
        mazefile = open(maze,"r")
        mazelines = mazefile.readlines()

        # Any search above number 4 is a multidot search so the maze is generated differently

        if searchoption > 4:
            mazematrix = generateMaze(mazelines, True)
        else:
            mazematrix = generateMaze(mazelines, False)

        menu(searchoption, mazematrix)

    # Handle exception
    except Exception as inst:
        print inst
        sys.exit(2)

# generateMaze)() converts the file into a 2-D matrix
# while reading, the pacman and dot locations are saved into global variables

def generateMaze(maze, multi):
    width = 0
    height = 0
    if multi:
        global dots
        dots = []
    index = 0

    # Return width and height of the maze
    for j, lines in enumerate(maze):
        lines = lines.strip('\n')
        lines = lines.strip('\r')
        width = len(lines)
        height += 1
    mazematrix = [['%' for y in range(width)] for x in range(height)]

    global mazeHeight
    global mazeWidth
    mazeHeight = height
    mazeWidth = width

    # Input maze values into the 2-D matrix
    for j, lines in enumerate(maze):
        for i, char in enumerate(lines):
            if not(char == '%' or char == '\n' or char == '\r'):
                mazematrix[j][i] = char
            if char == '.':
                if multi:
                    dots.append((j,i))
                else:
                    global goal
                    goal = (j,i)
            if char == 'P':
                global pacman
                pacman = (j,i)
    return mazematrix

'''
 Handle search option:
    1 - Depth First Search
    2 - Breadth First Search
    3 - Greedy Best First Search
    4 - A* Search
    5 - Pacman Heuristic V1 (BFS Heuristic)
    6 - Pacman Heuristic V2 (Total Manhattan Distance Heuristic)
'''

def menu(option, mazematrix):
    maze = graph.generateGraph(mazematrix,mazeWidth,mazeHeight)
    if option > 6 or option < 1:
        print "Incorrect parameter: \n1 <= Option <= 4"
        sys.exit(2)
    elif option == 1:
        DFS(maze, mazematrix)
    elif option == 2:
        BFS(maze,mazematrix)
    elif option == 3:
        greedy(maze,mazematrix)
    elif option == 4:
        aStar(maze,mazematrix)
    elif option == 5:
        pacmanv1(maze,mazematrix, dots)
    elif option == 6:
        pacmanv2(maze,mazematrix, dots)

# General function to display DFS, BFS, Greedy & A* Search results in console

def displayFinal(mazematrix, optimal, numberExp):
    currentY, currentX = pacman
    print "Optimal Path: \n" + optimal
    print "Optimal Path Length: " + str(len(optimal))
    print "Number of Expansions: " + str(numberExp)
    # for i in range(len(mazematrix)):
    #     print "".join(mazematrix[i])
    for j in list(optimal):

        if j == 'L':
            currentX -= 1
        elif j == 'R':
            currentX += 1
        elif j == 'U':
            currentY -= 1
        elif j == 'D':
            currentY += 1
        mazematrix[currentY][currentX] = '.'
    mazematrix[goal[0]][goal[1]] = 'G'
    for i in range(len(mazematrix)):
        print "".join(mazematrix[i])

# General function to display Multidot Search results in console

def displayMultiFinal(mazematrix, path, optimal, numberExp):
    currentY, currentX = pacman
    print "Optimal Path: \n" + str(path)
    print "Optimal Path Length: " + str(len(path))
    print "Number of Expansions: " + str(numberExp)
    index = 0
    alphanumeric = "123456789" + string.lowercase + string.uppercase
    mazematrix[pacman[0]][pacman[1]] = '0'
    for dot in optimal:
        mazematrix[dot[0]][dot[1]] = alphanumeric[index]
        index += 1
    for i in range(len(mazematrix)):
        print "".join(mazematrix[i])

# BFS() --> traverseBFS()
def BFS(maze, mazematrix):
    result = traverseBFS(maze)
    displayFinal(mazematrix, result[0], result[1])


def traverseBFS(maze):
    # Counter for Number of Expansions
    numberExp = 0

    # Generates a queue structure to add the nodes to be expanded
    q = collections.deque([("", pacman)])

    # For Repeated state detection, we implement a marked set
    marked = set()
    while q:
        currentPath, currentNode = q.popleft()

        # Base case if currentNode is at the goal
        if currentNode == goal:
            return (currentPath, numberExp)

        # Don't expand if expanded node before
        if currentNode in marked:
            continue
        marked.add(currentNode)
        numberExp += 1

        # Add neighbouring nodes to the queue
        for move, nextNode in maze[currentNode]:
            q.append((currentPath + move, nextNode))

    # Just in case the function fails
    return "Unexpected Function Return"

# DFS() --> traverseDFS()
def DFS(maze, mazematrix):
    result = traverseDFS(maze)
    displayFinal(mazematrix, result[0], result[1])


# Essentially the same as traverseBFS() but uses a stack structure instead of queues
def traverseDFS(maze):
    numberExp = 0
    s = collections.deque([("", pacman)])
    marked = set()
    while s:
        currentPath, currentNode = s.pop()
        if currentNode == goal:
            return (currentPath, numberExp)
        if currentNode in marked:
            continue
        marked.add(currentNode)
        numberExp += 1
        for move, nextNode in maze[currentNode]:
            s.append((currentPath + move, nextNode))

    return "Unexpected Function Return"

# Returns Manhattan Distance
def manhattanDistance(start, end):
    return abs(end[0] - start[0]) + abs(end[1] - start[1])

# greedy() --> traverseGreedy() --> manhattanDistance()
def greedy(maze,mazematrix):
    result = traverseGreedy(maze)
    displayFinal(mazematrix, result[0], result[1])


def traverseGreedy(maze):
    numberExp = 0

    '''
    A Priority Queue implementation is used for the greedy and A* searching
    The python 'heapq' function will generate a priority queue that will sort out
    the neighbours added to the queue by the heuristic value. This allows us to
    easily add new nodes without having to worry about searching for the smallest valued
    node as we only need to use the pop function to do this.
    Greatly saves on complexity and run time
    '''

    # Generate priority queue and populate with initial node with current pacman location
    priorityQueue = []
    # Heap state stored as tuple of (manhattanDistance, current path length, current node)
    heapq.heappush(priorityQueue, (manhattanDistance(pacman, goal), "", pacman))

    marked = set()
    while priorityQueue:
        cost, currentPath, currentNode = heapq.heappop(priorityQueue)
        if currentNode == goal:
            return (currentPath, numberExp)
        if currentNode in marked:
            continue
        marked.add(currentNode)
        numberExp += 1

        # Adds nodes to heap which are automatically sorted
        for move, nextNode in maze[currentNode]:
            heapq.heappush(priorityQueue, (manhattanDistance(currentNode,goal),currentPath + move, nextNode))
    return "Unexpected Function Return"


# aStar --> traverseAStar() --> manhattanDistance()
def aStar(maze, mazematrix):
    result = traverseAStar(maze)
    displayFinal(mazematrix, result[0], result[1])

# Same as greedy except a new state is recorded which is the current path length + manhattanDistance
def traverseAStar(maze):
    numberExp = 0
    priorityQueue = []
    heapq.heappush(priorityQueue, (manhattanDistance(pacman,goal),0,"", pacman))
    marked = set()
    while priorityQueue:
        _, cost, currentPath, currentNode = heapq.heappop(priorityQueue)
        if currentNode == goal:
            return (currentPath, numberExp)
        if currentNode in marked:
            continue
        marked.add(currentNode)
        numberExp += 1
        for move, nextNode in maze[currentNode]:
            heapq.heappush(priorityQueue, (cost + manhattanDistance(currentNode,goal), cost + 1, currentPath + move, nextNode))
    return "Unexpected Function Return"

# pacmanv1() --> traversePacmanv1() --> pacHeuristic1() --> pacBFS()
def pacmanv1(maze, mazematrix, goals):
    length = prompt()
    result = traversePacmanv1(maze, goals, length)
    displayMultiFinal(mazematrix, result[0], result[1], result[2])

# Implements the BFS but returns the total distance and closest dot from a start point
def pacBFS(maze,start,end):
    numberExp = 0
    q = collections.deque([("", start)])
    marked = set()
    while q:
        currentPath, currentNode = q.popleft()
        if currentNode == end:
            return (currentNode, len(currentPath))
        if currentNode in marked:
            continue
        marked.add(currentNode)
        numberExp += 1
        for move, nextNode in maze[currentNode]:
            q.append((currentPath + move, nextNode))
    return "Unexpected Function Return"

# This first iteration pacman heuristic uses the total BFS distance between the closest dots
# This is calculated interating the BFS until you find the closest dot and combining total costs
def pacHeuristic1(maze, current, goals, length):
    gs = goals[:]
    totaldist = 0
    olength = len(gs)
    dist = 9999
    nextNode = current
    index = 0
    while(gs and length > index):
        for dot in gs:
            result  = pacBFS(maze, current, dot)
            if result[1] < dist:
                dist = result[1]
        gs.remove(result[0])
        totaldist += dist
        dist = 9999
        current = result[0]
        index += 1
    return totaldist

# The implementation of the search is essentially A* search with some extra return fields for the display functions
def traversePacmanv1(maze, goals, length):
    numberExp = 0
    priorityQueue = []
    marked = set()
    current = pacman
    finalPath = []
    glength = len(goals)
    d = goals[:]
    p = ''
    while(len(finalPath) < glength):
        priorityQueue = []
        heapq.heappush(priorityQueue, (pacHeuristic1(maze, current, d, length),0,"", current))
        marked.clear()
        while priorityQueue:
            _, cost, currentPath, currentNode = heapq.heappop(priorityQueue)
            if currentNode in d:
                d.remove(currentNode)
                finalPath.append(currentNode)
                current = currentNode
                p = p + currentPath
                break
            if currentNode in marked:
                continue
            marked.add(currentNode)
            numberExp += 1
            for move, nextNode in maze[currentNode]:
                heapq.heappush(priorityQueue, (cost + pacHeuristic1(maze, nextNode, d, length), cost + 1, currentPath + move, nextNode))
    return (p, finalPath, numberExp)

# pacmanv2() --> traversePacmanv2() --> pacHeuristic2() --> manhattanDistance()
def pacmanv2(maze, mazematrix, goals):
    length = prompt()
    result = traversePacmanv2(maze, goals, length)
    displayMultiFinal(mazematrix, result[0], result[1], result[2])

# This heuristic finds total Manhattan distance from the closest dots to the furthest manhattanDistance
# Dots are iterated through, finding the minimum Manhattan distance and removing from the dots list
# Once removed, the distance to the next closest node is calculated, repeating until the dots list is empty
def pacHeuristic2(current, goals, length):
    gs = goals[:]
    totaldist = 0
    dist = 9999
    nextNode = current
    index = 0
    while(gs and length > index):
        for dot in gs:
            result  = manhattanDistance(current, dot)
            if result < dist:
                dist = result
                nextNode = dot
        gs.remove(nextNode)
        totaldist += dist
        dist = 9999
        current = nextNode
        index += 1
    return totaldist

# The implementation of the search is essentially A* search with some extra return fields for the display functions
def traversePacmanv2(maze, goals, length):
    numberExp = 0
    priorityQueue = []
    marked = set()
    current = pacman
    finalPath = []
    glength = len(goals)
    d = goals[:]
    p = ''
    while(len(finalPath) < glength):
        priorityQueue = []
        heapq.heappush(priorityQueue, (pacHeuristic2(current, d, length),0,"", current))
        marked.clear()
        while priorityQueue:
            _, cost, currentPath, currentNode = heapq.heappop(priorityQueue)
            if currentNode in d:
                d.remove(currentNode)
                finalPath.append(currentNode)
                current = currentNode
                p = p + currentPath
                break
            if currentNode in marked:
                continue
            marked.add(currentNode)
            numberExp += 1
            for move, nextNode in maze[currentNode]:
                heapq.heappush(priorityQueue, (cost + pacHeuristic2(nextNode, d, length), cost + 1, currentPath + move, nextNode))
    return (p, finalPath, numberExp)

# General function that prompts the user for a max length for the k neighbour nodes
def prompt():
    while(True):
        s = int(raw_input("Please enter the max number of dots to visit in the heuristic: \n"))
        if s > 100 or s < 1:
            print "Invalid number entry"
        else:
            return s


if __name__ == '__main__':
    main()
