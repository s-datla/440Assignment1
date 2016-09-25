#!/usr/bin/python
import sys, getopt, subprocess, random
import os.path
import tree

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
        generateMaze(mazelines)
        # menu(searchoption)
        for i in range(len(mazematrix)):
            print "".join(mazematrix[i])

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
    global mazematrix
    mazematrix = [['%' for y in range(width-1)] for x in range(height)]

    for j, lines in enumerate(maze):
        for i, char in enumerate(lines):
            if not(char == '%' or char == '\n' or char == '\r'):
                mazematrix[j][i] = char

def menu(option):
    if option > 4 or option < 1:
        print "Incorrect parameter: \n1 <= Option <= 4"
        sys.exit(2)
    elif option == '1':
        BFS()
    elif option == '2':
        DFS()
    elif option == '3':
        greedy()
    elif option == '4':
        aStar()

# def BFS():
#
# def DFS():
#
# def greedy():
#
# def aStar():



if __name__ == '__main__':
    main()
