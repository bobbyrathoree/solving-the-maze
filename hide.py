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
no_solution_exists = False
visited = set()


def parse_map(filename: str) -> list:
    """
    To parse the map from a given filename
    :param filename: name of the file
    :return: a two-dimensional list of the map
    """
    with open(filename, "r") as f:
        return [[char for char in line] for line in f.read().split("\n")]


def printable_board(board: list) -> str:
    """
    To return a string with the board rendered in a human-friendly format
    :param board: the 2-d solution board
    :return: that same board in a presentable string format
    """
    return "\n".join(["".join(row) for row in board])


def stringify(arr):
    """
    Returns a map as a string to save in visited set.
    String because list of lists would take a whole lot memory
    :param arr: the list that we want as a string
    :return: the string made up of list elements
    """
    return "".join(["".join(row) for row in arr])


def solution_found_checker() -> None:
    """
    a simple function that checks every 1 second if the solution has been found.
    """
    if solution_found:
        raise SystemExit
    else:
        threading.Timer(1.0, solution_found_checker).start()


def add_friend(board: list, row: int, col: int) -> list:
    """
    Add a friend to the board at the given position, and return a
    new board (doesn't change original)
    :param board: the 2-d list of map
    :param row: row index
    :param col: column index
    :return: a list consisting of the map with the added friend
    """
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


def is_safe(arr: list, position: int) -> bool:
    """
    :param arr: this list is checked left and right if there is no immediate friend
    :param position: position where the friend is supposed to be placed
    :return: boolean value whether friend is safe to be placed there or not
    """
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


def successors(board: list) -> list:
    """
    Get list of successors of given board state
    :param board: instance of the board at a particular time in the fringe
    :return: list of possible successors for a board state
    """
    return [
        add_friend(board, r, c)
        for r in range(0, len(board))
        for c in range(0, len(board[0]))
        if board[r][c] == "."
        and is_safe(board[r], c)
        and is_safe([col[c] for col in board], r)
    ]


def check_number_of_friends(board: list) -> None:
    """
    To check the board every n^2 seconds so that for a no-solution case, it doesn't
    into an infinite loop. Executes a thread safe implementation, that doesn't slow
    down the actual search algorithm
    :param board: board
    """
    global ctr, time_factor, old_number_of_friends, no_solution_exists

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
        print("No solution found!")
        no_solution_exists = True
        sys.exit()

    threading.Timer(time_factor, check_number_of_friends, [solution_board]).start()


def is_goal(board: list) -> bool:
    """
    Check if board is a goal state
    :param board: list of board at a particular time in execution cycle
    :return: a boolean value signifying whether we're at the goal state
    """
    return sum([row.count("F") for row in board]) == K


def solve(initial_board):
    """
    Solve n-rooks!
    :param initial_board: the user map without any friends in a 2d list
    :return: either False if no solution found, or the solution itself
    """
    global solution_board
    fringe = deque()
    fringe.append(initial_board)
    while len(fringe) > 0:
        if no_solution_exists:
            sys.exit()
        for s in successors(fringe.pop()):
            if stringify(s) in visited:
                break
            if no_solution_exists:
                sys.exit()
            if is_goal(s):
                return s
            solution_board = s
            visited.add(stringify(s))
            fringe.append(s)
    return False


# Main Function
if __name__ == "__main__":
    iub_map = parse_map(sys.argv[1])

    # This is K, the number of friends
    K = int(sys.argv[2])

    print(
        "Starting from initial board:\n"
        + printable_board(iub_map)
        + "\n\nLooking for solution..."
    )

    solution = solve(iub_map)
    solution_found_checker()
    print(
        "\nHere's what we found:\n{0}".format(printable_board(solution))
        if solution
        else "None"
    )
    solution_found = True
    raise SystemExit
