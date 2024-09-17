#!/usr/bin/env python3
import sys
import re

def check_argument():
    """
    Checks if the correct number of command-line arguments is provided. 
    Exits the program if an incorrect number of arguments is detected.
    
    Parameters: None.

    Returns: None.
    """
    if len(sys.argv) != 1:
        print("Error: Invalid argument passed, please try again!", file=sys.stderr)
        sys.exit(1)

def read_from_smt():
    """
    Reads the input from the SMT solver via standard input and parses it into a list of lines, 
    while also checking if the puzzle is satisfiable or unsatisfiable.
    
    Parameters: None.
    
    Returns:
    - smt_file (list): A list of lines from the input.
    - sat_puzzle (bool): A boolean indicating whether the puzzle is satisfiable (True) or unsatisfiable (False).

    """
    smt_file = []
    sat_puzzle = True
    for line in sys.stdin:
        line = re.sub('\n', '', line)
        smt_file.append(line.split(")"))
        if "unsat" in line:
            print("UNSAT")
            sat_puzzle = False
            break
    return smt_file, sat_puzzle

def get_from_smt(smt_file, sat_puzzle):
    """
    Extracts the solved values from the parsed SMT-LIB output if the puzzle is satisfiable.

    Parameters:
    - smt_file (list): A list of lines from the input.
    - sat_puzzle (bool): A boolean indicating whether the puzzle is satisfiable.

    Returns:
    - solved (list): A list of solved values for the puzzle.
    """
    solved = []
    if sat_puzzle:
        for i, box in enumerate(smt_file[1:50], start=1):
            box = box[0].split(" ")
            solved.append(box[2] if i == 1 else box[3])
    return solved

def write_solution(solved):
    """
    Writes the solution of the puzzle to a text file named "solution.txt" if the puzzle is satisfiable. 
    Otherwise, writes a message indicating that the puzzle is not satisfiable.

    Parameters:
    - solved (list): A list of solved values for the puzzle.

    Returns: None
    """
    with open('solution.txt', 'w') as solution:
        if solved:
            solution.write(''.join(solved))
            solution.write("\n")
        else:
            solution.write("Puzzle is not satisfiable.\n")

def main():
    """
    Entry point of the script; it orchestrates the execution by checking arguments, 
    reading from the SMT solver, extracting the solution, and writing it to a file.

    """
    check_argument()
    smt_file, sat_puzzle = read_from_smt()
    solved = get_from_smt(smt_file, sat_puzzle)
    write_solution(solved)

if __name__ == "__main__":
    main()