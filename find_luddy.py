#!/usr/local/bin/python3
#
# find_luddy.py : a simple maze solver
#
# Submitted by : Bobby Rathore (brathore)
#
# Based on skeleton code by Z. Kachwala, 2019
#
import queue
import sys


# Parse the map from a given filename
def parse_map(filename):
    with open(filename, "r") as f:
        return [[char for char in line] for line in f.read().split("\n")]


# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
    return 0 <= pos[0] < n and 0 <= pos[1] < m


visited = list()


# Find the possible moves from position (row, col)
def moves(input_map, row, col):
    possible_moves = (
        ((row + 1, col), "S"),
        ((row - 1, col), "N"),
        ((row, col - 1), "W"),
        ((row, col + 1), "E"),
    )

    # Return only moves that are within the board, non-visited and legal (i.e. on the sidewalk ".")
    valid_moves = [
        move
        for move in possible_moves
        if valid_index(move[0], len(input_map), len(input_map[0]))
        and (input_map[move[0][0]][move[0][1]] in ".@" and move[0] not in visited)
    ]
    [visited.append(move[0]) for move in valid_moves]
    return valid_moves


def get_my_location(input_map):
    return [
        (row_i, col_i)
        for col_i in range(len(input_map[0]))
        for row_i in range(len(input_map))
        if input_map[row_i][col_i] == "#"
    ][0]


def get_number_of_sidewalks(input_map):
    return len([
        'foo'
        for col_i in range(len(input_map[0]))
        for row_i in range(len(input_map))
        if input_map[row_i][col_i] == "."
    ])


# Perform search on the map
def search1(input_map):
    my_location = get_my_location(input_map)

    # We use queue for our purpose
    fringe = queue.Queue()
    fringe.put(((my_location, ""), 0))
    visited.append(my_location)

    while fringe:
        (curr_move, curr_dist) = fringe.get()
        moves_for_this_point = moves(input_map, *curr_move[0])
        for move in moves_for_this_point:
            if input_map[move[0][0]][move[0][1]] == "@":
                return curr_dist + 1, curr_move[1] + move[1]
            else:
                # Terminating condition in case no solution is found
                if len(visited) == get_number_of_sidewalks(input_map):
                    return None

                # Add to queue the point to explore next, along with path traveled until now
                fringe.put(((move[0], curr_move[1] + move[1]), curr_dist + 1))


# Main Function
if __name__ == "__main__":
    # iub_map = parse_map(sys.argv[1])
    iub_map = [
        [".", ".", ".", ".", "&", "&", "&"],
        [".", "&", "&", "&", ".", ".", "."],
        [".", ".", ".", ".", "&", ".", "."],
        [".", "&", ".", "&", ".", ".", "."],
        [".", "&", ".", "&", ".", "&", "."],
        ["#", "&", ".", ".", ".", "&", "@"],
    ]
    print("Leave me alone, I'm navigating!")
    solution = search1(iub_map)
    if solution:
        print("I found the solution btw.\nIt took me {0} steps to get there."
              "\nHere's the path that I took: {1}"
              "\nThe line below is for the not-so-smart grading program to grade my output.".format(solution[0], solution[1]))
        print(solution[0], solution[1])
    else:
        print("No solution found.")
