#! python

from raw_matrix import init_raw_matrix, print_raw_matrix
from sudoku_one_solver import Solver

import sys

if __name__ == '__main__':
    filename = sys.argv[1]
    raw_matrix = init_raw_matrix(filename)
    print_raw_matrix(raw_matrix)
    
    s = Solver()
    s.build_linked_list(raw_matrix)

    s.recursive_solve()
    s.print_sudoku_solution()
