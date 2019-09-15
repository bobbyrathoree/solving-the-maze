#!/usr/local/bin/python3
#
# hide.py : a simple friend-hider
#
# Submitted by : Bobby Rathore (brathore)
#
# Based on skeleton code by D. Crandall and Z. Kachwala, 2019
#
# The problem to be solved is this:
# Given a campus map, find a placement of F friends so that no two can find one another.

import sys
from collections import deque


# Parse the map from a given filename
def parse_map(filename):
    with open(filename, "r") as f:
        return [[char for char in line] for line in f.read().split("\n")]


# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    return "\n".join(["".join(row) for row in board])


# Add a friend to the board at the given position, and return a new board (doesn't change original)
def add_friend(board, row, col):
    return (
        board[0:row]
        + [board[row][0:col] + ["F"] + board[row][col + 1 :]]
        + board[row + 1 :]
    )


def is_safe(arr: list, position):
    left, right = arr[0:position], arr[position + 1 :]
    left_clear, right_clear = True, True
    if "F" in left:
        if not any(
            buildings
            in left[
                next(i for i in reversed(range(len(left))) if left[i] == "F") : position
            ]
            for buildings in ["&", "@"]
        ):
            left_clear = False
    if "F" in right:
        if not any(
            buildings in right[position : right.index("F")] for buildings in ["&", "@"]
        ):
            right_clear = False

    return left_clear and right_clear


# Get list of successors of given board state
def successors(board):
    return [
        add_friend(board, r, c)
        for r in range(0, len(board))
        for c in range(0, len(board[0]))
        if board[r][c] == "."
        and is_safe(board[r], c)
        and is_safe([col[c] for col in board], r)
    ]


# check if board is a goal state
def is_goal(board):
    return sum([row.count("F") for row in board]) == K


# Solve n-rooks!
def solve(initial_board):
    # fringe = deque()
    fringe = [initial_board]
    # fringe.append(initial_board)
    while len(fringe) > 0:
        for s in successors(fringe.pop()):
            if is_goal(s):
                return s
            fringe.append(s)
            print('\n\nfringe: {}'.format(len(fringe)))
    return False


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
    # This is K, the number of friends
    K = int(sys.argv[2])
    print(
        "Starting from initial board:\n"
        + printable_board(iub_map)
        + "\n\nLooking for solution...\n"
    )
    solution = solve(iub_map)
    print("Here's what we found:")
    print(printable_board(solution) if solution else "None")
