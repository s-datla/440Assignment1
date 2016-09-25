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
            print "Incorrect file path for maze file, retype"
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
    elif option == 1:
        result = traverseBFS(maze)
        print result
    elif option == 2:
        DFS()
    elif option == 3:
        greedy()
    elif option == 4:
        aStar()


def traverseBFS(maze):
    q = collections.deque([("", pacman)])
    marked = set()
    while q:
        currentPath, currentNode = q.popleft()
        if node == goal:
            return currentPath
        elif currentNode in visited:
            continue
        marked.add(node)
        for move, nextNode in maze[node]:
            queue.append((currentNode + move, nextNode))
    return "Illegal function return"

def DFS():
    return 1

def greedy():
    return 1

def aStar():
    return 1


if __name__ == '__main__':
    main()
