#!/usr/bin/python
import sys
import os.path
import graph
import collections

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
    if option > 4 or option < 1:
        print "Incorrect parameter: \n1 <= Option <= 4"
        sys.exit(2)
    elif option == 1:
        BFS(mazematrix)
    elif option == 2:
        DFS()
    elif option == 3:
        greedy()
    elif option == 4:
        aStar()


def BFS(mazematrix):
    maze = graph.generateGraph(mazematrix,mazeWidth,mazeHeight)
    result = traverseBFS(maze)
    currentY, currentX = pacman
    print "Optimal Path: \n" + result[0]
    print "Optimal Path Length: " + str(len(result[0]))
    print "Number of Expansions: " + str(result[1])

    for i in range(len(mazematrix)):
        print "".join(mazematrix[i])
    for j in list(result[0]):

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
        for direction, neighbour in maze[currentNode]:
            q.append((currentPath + direction, neighbour))
            numberExp += 1
    return "Unexpected Function Return"

def DFS():
    return 1

def greedy():
    return 1

def aStar():
    return 1


if __name__ == '__main__':
    main()
