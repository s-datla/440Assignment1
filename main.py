#!/usr/bin/python
import sys
import os.path
import graph
import collections
import heapq

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
        mazematrix = generateMaze(mazelines)
        menu(searchoption, mazematrix)
    except Exception as inst:
        print inst
        sys.exit(2)


def generateMaze(maze):
    width = 0
    height = 0
    for j, lines in enumerate(maze):
        if j == 0 :
            width = len(lines.strip('\n'))
        height += 1

    mazematrix = [['%' for y in range(width-1)] for x in range(height)]

    global mazeHeight
    global mazeWidth
    mazeHeight = height
    mazeWidth = width
    for j, lines in enumerate(maze):
        for i, char in enumerate(lines):
            if not(char == '%' or char == '\n' or char == '\r'):
                mazematrix[j][i] = char
            if char == '.':
                global goal
                goal = (j,i)
            if char == 'P':
                global pacman
                pacman = (j,i)
    return mazematrix

def menu(option, mazematrix):
    maze = graph.generateGraph(mazematrix,mazeWidth,mazeHeight)
    if option > 4 or option < 1:
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

def manhattanDistance(pacman, goal):
    return abs(goal[0] - pacman[0]) + abs(goal[1] - pacman[1])

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


if __name__ == '__main__':
    main()
