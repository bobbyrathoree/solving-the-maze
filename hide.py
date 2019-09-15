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
import threading

solution_board = list()
check_started = False
solution_found = False
old_number_of_friends = 0
ctr = 0
time_factor = 1.0


# Parse the map from a given filename
def parse_map(filename):
    with open(filename, "r") as f:
        return [[char for char in line] for line in f.read().split("\n")]


# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    return "\n".join(["".join(row) for row in board])


# Add a friend to the board at the given position, and return a new board (doesn't change original)
def add_friend(board, row, col):
    global check_started
    board_with_new_friend = (
        board[0:row]
        + [board[row][0:col] + ["F"] + board[row][col + 1 :]]
        + board[row + 1 :]
    )
    if not check_started:
        check_number_of_friends(board_with_new_friend)
        check_started = True
    return board_with_new_friend


def is_safe(arr: list, position):
    left, right = arr[0:position], arr[position + 1 :]
    left_clear, right_clear = True, True
    buildings = ["&", "@"]
    if "F" in left:
        if not any(
            building
            in left[
                next(i for i in reversed(range(len(left))) if left[i] == "F") : position
            ]
            for building in buildings
        ):
            left_clear = False
    if "F" in right:
        if not any(
            building in right[position : right.index("F")] for building in buildings
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


def check_number_of_friends(board):
    global ctr, time_factor, old_number_of_friends

    if solution_found:
        raise SystemExit

    new_number_of_friends = sum([row.count("F") for row in board])
    if old_number_of_friends == new_number_of_friends:
        ctr += 1
        time_factor *= 2
    else:
        ctr = 0
        time_factor = 1.0
        old_number_of_friends = new_number_of_friends
    if ctr >= 5:
        print("No solution found!\nPress Ctrl+C to exit the program.")
        raise SystemExit

    threading.Timer(time_factor, check_number_of_friends, [solution_board]).start()


# check if board is a goal state
def is_goal(board):
    return sum([row.count("F") for row in board]) == K


def stringify(arr):
    return "".join(["".join(row) for row in arr])


# Solve n-rooks!
def solve(initial_board):
    global solution_board
    fringe = deque()
    fringe.append(initial_board)
    while len(fringe) > 0:
        for s in successors(fringe.pop()):
            if is_goal(s):
                return s
            solution_board = s
            fringe.append(s)
    return False


def solution_found_checker():
    if solution_found:
        raise SystemExit
    else:
        threading.Timer(1.0, solution_found_checker).start()


# Main Function
if __name__ == "__main__":
    iub_map = parse_map(sys.argv[1])

    # This is K, the number of friends
    K = int(sys.argv[2])

    print(
        "Starting from initial board:\n"
        + printable_board(iub_map)
        + "\n\nLooking for solution...\n"
    )

    solution = solve(iub_map)
    print("Here's what we found:")
    solution_found_checker()
    print(printable_board(solution))
    solution_found = True
    raise SystemExit
