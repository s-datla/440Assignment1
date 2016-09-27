import sys

'''

    Using the matrix generated earlier, we are populating a dictionary to contain the actions
    available to the current node.
    The key being used for the dictionary is the tuple of the coordinates of the current node.
    By iterating through the matrix, we determine if the adjacent cells are empty and if they are,
    the dictionary will be populated with the available actions (L = left, R = right, etc.).

'''

def generateGraph(matrix, width, height):
    maze = {(i,j): [] for j in range(width-1) for i in range(height) if not (matrix[i][j] == '%')}
    for i, j in maze.keys():
        if j > 0 and not matrix[i][j-1] == '%':
            maze[(i,j)].append(("L",(i,j-1)))
            # maze[(i,j-1)].append(("R",(i,j)))
        if j < width - 1 and not matrix[i][j+1] == '%':
            maze[(i,j)].append(("R",(i,j + 1)))
            # maze[(i,j+1)].append(("L",(i,j)))
        if i > 0 and not matrix[i-1][j] == '%':
            maze[(i,j)].append(("U",(i - 1, j)))
            # maze[(i-1,j)].append(("D",(i,j)))
        if i < height - 1 and not matrix[i+1][j] == '%':
            maze[(i,j)].append(("D",(i + 1, j)))
            # maze[(i+1,j)].append(("U",(i,j)))
    return maze
