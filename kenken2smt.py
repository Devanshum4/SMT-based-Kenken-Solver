#!/usr/bin/env python3
import re
import sys
from itertools import permutations

def read_puzzle(filename):
    """
    Reads the given puzzle from a text file and parses them into a list of constraints.

    Parameters:
    - filename (str): The name of the text file containing the puzzle.

    Returns:
    - constraints (list): A list of constraints extracted from the puzzle file.
    
    """  
    constraints = []

    with open(filename, 'r') as puzzle_txt:
        for line in puzzle_txt:
            if '#' in line:
                continue
            unit = line.rstrip('\n').split(",")
            for u in unit:
                sub_unit = re.split(r'\.', u)
                sub_unit.append("V" + str(len(constraints)))
                constraints.append(sub_unit)

    return constraints

def operator_function(output_file,constraints):
    """
    Generates SMT-LIB assertions for constraints involving arithmetic operations (+, -, *, /) 
    and writes them to the output file.
    
    Parameters:
    - output_file (file object): The file object for writing SMT-LIB assertions.
    - constraints (list): A list of constraints extracted from the puzzle file.
    
    Returns: None.
    
    """
    for c in constraints:
        if len(c)==3:
            current = c[0]
            op = ''
            if '/' in c[1] or '-' in c[1]:
                if '/' in c[1]:
                    op = '/'
                    result = c[1].strip('/')
                else:
                    op = '-'
                    result = c[1].strip('-')

                region = [c[2]]
                for j in range(len(constraints)):
                    if current == constraints[j][0] and len(constraints[j]) == 2:
                        region.append(constraints[j][1])

                permut = list(permutations(region, len(region)))
                output_file.write("(assert (or ")
                for i in range(len(permut)):
                    output_file.write(" (= "+result+" ("+op)
                    for j in range(len(permut)):
                        output_file.write(" "+permut[i][j])
                    output_file.write("))")
                output_file.write("))\n")
                continue

            elif '*' in c[1] or '+' in c[1]:
                if '*' in c[1]:
                    op = '*'
                    result = c[1].strip('*')
                else:
                    op = '+'
                    result = c[1].strip('+')
                output_file.write("(assert (= "+result+" ("+op+" "+c[2])
                for i in range(len(constraints)):
                    if current == constraints[i][0] and len(constraints[i]) == 2:
                        output_file.write(" "+constraints[i][1])
                output_file.write('))) \n')
                
            if op== '':
                continue

def write_smt(constraints):
    """
    Writes the puzzle constraints in SMT-LIB format to a file, including declarations, assertions, 
    and arithmetic operations.
    
    Parameters:
    - constraints (list): A list of constraints extracted from the puzzle file.
    
    Returns: None.
    
    """
    output_file = open("puzzle.smt", 'w')
    output_file.write("(set-logic UFNIA)\n(set-option :produce-models true)\n(set-option :produce-assignments true)\n")

    for i in range(49):
        output_file.write("(declare-const V{} Int)\n".format(i))
    
    for i in range(49):
        output_file.write("(assert (and (> V{} 0) (< V{} 8)))\n".format(i, i))

    for c in constraints:
        if len(c) == 3:
            op = ''
            if '+' in c[1]:
                op = '+'
            elif '*' in c[1]:
                op = '*'
            elif '/' in c[1]:
                op = '/'
            elif '-' in c[1]:
                op = '-'
            if op == '':
                output_file.write("(assert (= "+c[2]+" "+c[1]+"))\n")

    for i in range(7):
        output_file.write("(assert (distinct {}))\n".format(" ".join("V{}".format(i*7 + j) for j in range(7))))
    
    for i in range(7):
        output_file.write("(assert (distinct {}))\n".format(" ".join("V{}".format(j*7 + i) for j in range(7))))

    operator_function(output_file,constraints) 

    output_file.write("(check-sat)\n")
    output_file.write("(get-value (")

    for i in range(49):
        output_file.write("V"+str(i)+" ")

    output_file.write("))\n")
    output_file.write("(exit)\n")

    output_file.close()

def main(): 
    if len(sys.argv)!=2:
        print("Error: Invalid argument passed, please try again!")
        exit()

    puzzle_txt = sys.argv[1]
    constraints = read_puzzle(puzzle_txt)
    write_smt(constraints)

if __name__ == "__main__":
    main()






