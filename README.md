Building the KenKen puzzle solver using SMT required us to develop two files: kenken2smt.py and smt2kenken.py. 
The primary purpose of kenken2smt is to interpret a single partially solved KenKen puzzle and transform it into SMT-LIB format which can be passed to a SMT solver (Mathsat) to generate solutions. 
The SMT-LIB format was based on the article "Solving KenKen using an SMT (integer) solver." smt2kenken.py uses the output from the SMT solver (Mathsat) to convert it into a KenKen solution.
The solution provided by smt2kenken is in the form of a string of digits, representing the values assigned to each cell in the KenKen grid. For this project we used 7x7 KenKen Puzzles.
