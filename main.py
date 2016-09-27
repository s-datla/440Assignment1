#!/usr/bin/python
import sys
import os.path
import graph
import collections
import heapq
import string

searchoption = 0

def main():
    if(len(sys.argv) < 3):
        print "Incorrect Format: \npython main.py <maze-file-txt-file> <option>"
        sys.exit(2)
    try:
        maze = str(sys.argv[1])
        searchoption = int(sys.argv[2])
        if not(os.path.exists("./" + maze)):
            print "Incorrect file currentPath for maze file, retype"
            sys.exit(2)
        mazefile = open(maze,"r")
        mazelines = mazefile.readlines()
        if searchoption > 4:
            mazematrix = generateMaze(mazelines, True)
        else:
            mazematrix = generateMaze(mazelines, False)
        menu(searchoption, mazematrix)
    except Exception as inst:
        print inst
        sys.exit(2)

def generateMaze(maze, multi):
    width = 0
    height = 0
    if multi:
        global dots
        dots = []
    index = 0
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

def menu(option, mazematrix):
    maze = graph.generateGraph(mazematrix,mazeWidth,mazeHeight)
    if option > 6 or option < 1:
        print "Incorrect parameter: \n1 <= Option <= 4"
        sys.exit(2)
    elif option == 2:
        BFS(maze, mazematrix)
    elif option == 1:
        DFS(maze,mazematrix)
    elif option == 3:
        greedy(maze,mazematrix)
    elif option == 4:
        aStar(maze,mazematrix)
    elif option == 5:
        pacmanv1(maze,mazematrix, dots)
    elif option == 6:
        pacmanv2(maze,mazematrix, dots)

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

def BFS(maze, mazematrix):
    result = traverseBFS(maze)
    displayFinal(mazematrix, result[0], result[1])


def traverseBFS(maze):
    numberExp = 0
    q = collections.deque([("", pacman)])
    marked = set()
    while q:
        currentPath, currentNode = q.popleft()
        if currentNode == goal:
            return (currentPath, numberExp)
        if currentNode in marked:
            continue
        marked.add(currentNode)
        numberExp += 1
        for move, nextNode in maze[currentNode]:
            q.append((currentPath + move, nextNode))
    return "Unexpected Function Return"

def DFS(maze, mazematrix):
    result = traverseDFS(maze)
    displayFinal(mazematrix, result[0], result[1])


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

def manhattanDistance(start, end):
    return abs(end[0] - start[0]) + abs(end[1] - start[1])

def greedy(maze,mazematrix):
    result = traverseGreedy(maze)
    displayFinal(mazematrix, result[0], result[1])

def traverseGreedy(maze):
    numberExp = 0
    priorityQueue = []
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
        for move, nextNode in maze[currentNode]:
            heapq.heappush(priorityQueue, (manhattanDistance(currentNode,goal),currentPath + move, nextNode))
    return "Unexpected Function Return"



def aStar(maze, mazematrix):
    result = traverseAStar(maze)
    displayFinal(mazematrix, result[0], result[1])

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

def pacmanv1(maze, mazematrix, goals):
    length = prompt()
    result = traversePacmanv1(maze, goals, length)
    displayMultiFinal(mazematrix, result[0], result[1], result[2])


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


# Nearest BFS difference
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

def pacmanv2(maze, mazematrix, goals):
    length = prompt()
    result = traversePacmanv2(maze, goals, length)
    displayMultiFinal(mazematrix, result[0], result[1], result[2])

# Distance combination of totals
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

def prompt():
    while(True):
        s = int(raw_input("Please enter the max number of dots to visit in the heuristic: \n"))
        if s > 100 or s < 1:
            print "Invalid number entry"
        else:
            return s


if __name__ == '__main__':
    main()
