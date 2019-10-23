#! python

from dancing_link_list import DancingLinkList

import math


class Solver():
    def __init__(self):
        self.dll = None
        self.solution = []
        self.sodoku_size = 0

    def build_linked_list(self, raw_matrix):
        self.sudoku_size = len(raw_matrix[0])
        num_of_columns = self.sudoku_size * self.sudoku_size * 4
        self.dll = DancingLinkList(num_of_columns)

        for i in xrange(0, len(raw_matrix)):
            row = raw_matrix[i]
            for j in xrange(0, len(row)):
                if row[j] > 0:
                    self.remove_single_column_head(i, j, row[j]-1)

        for i in xrange(0, len(raw_matrix)):
            row = raw_matrix[i]
            for j in xrange(0, len(row)):
                if row[j] == 0:
                    self.build_sudoku_rows(i, j)

    def remove_single_column_head(self, i, j, val):
       section_size = self.sudoku_size * self.sudoku_size
       
       idx1 = i * self.sudoku_size + j
            
       idx2 = i * self.sudoku_size + val + section_size

       idx3 = j * self.sudoku_size + val + section_size * 2

       location_size = int(math.sqrt(self.sudoku_size + 1))
       location_idx = (j/location_size) * location_size + i/location_size
       idx4 = location_idx * self.sudoku_size + val + section_size * 3

       for idx in [idx1, idx2, idx3, idx4]:
           node = self.dll.column_heads[idx]
           node.remove_column()

    
    def build_sudoku_rows(self, i, j):
        section_size = self.sudoku_size * self.sudoku_size
       
        row_cnt = 0
        for val in xrange(0, self.sudoku_size):
            row_idx = len(self.dll.row_heads)
            
            # Section 1: every cell can only place one value, totally
            # size*size cells.
            idx1 = i * self.sudoku_size + j

            
            # Section 2: every row can only have 1-9 showing up once,
            # 9 rows, each row has 9 values (each value occupies a
            # column).
            idx2 = i * self.sudoku_size + val + section_size


            # Section 3: every column can only have 1-9 showing up
            # once, 9 columns, each column has 9 values (each value
            # occupies a column).
            idx3 = j * self.sudoku_size + val + section_size * 2

            
            # Section 4: every location can only have 1-9 showing up
            # once, 9 locations, each location has 9 values (each
            # value occupies a column).
            location_size = int(math.sqrt(self.sudoku_size + 1))
            location_idx = (j/location_size) * location_size + i/location_size
            idx4 = location_idx * self.sudoku_size + val + section_size * 3

            if self.dll.column_heads[idx1].is_removed_from_column or\
               self.dll.column_heads[idx2].is_removed_from_column or\
               self.dll.column_heads[idx3].is_removed_from_column or\
               self.dll.column_heads[idx4].is_removed_from_column:
                continue

            self.dll.insert_node(row_idx, idx1, val)
            self.dll.insert_node(row_idx, idx2, val)
            self.dll.insert_node(row_idx, idx3, val)
            self.dll.insert_node(row_idx, idx4, val)


    def print_sudoku_solution(self):
        print "--"
        x = 0
        row_ids = [int(e.val)-1 for e in self.solution]
        row_ids = sorted(row_ids)
        
        for row_idx in row_ids:
            row_head = self.dll.row_heads[row_idx]
            node1 = row_head.right
            column_idx1 = node1.col_head.val-1
            i = column_idx1 / self.sudoku_size
            j = column_idx1 % self.sudoku_size

            node2 = node1.right
            column_idx2 = node2.col_head.val-1
            val = column_idx2 - (self.sudoku_size*self.sudoku_size) - (i*self.sudoku_size)
            if i > x:
                print ""
                x = i
            
            print "(%s, %s)-> %s " % (i, j, val+1),


    def pre_solve(self):
        empty_heads = self.dll.get_empty_column_heads()
        for head in empty_heads:
            head.remove_column()
        
        column_heads = self.dll.get_single_node_column_heads()

        row_heads = []
        for head in column_heads:
            if not head.down.row_head in row_heads:
                row_heads.append(head.down.row_head)

        columns = []
        for row_head in row_heads:
            self.solution.append(row_head)
            cols = self.dll.get_columns_impacted_by_row(row_head)
            for col in cols:
                if not col in columns:
                    columns.append(col)
                else:
                    print "duplicated:", col.val, "by row -->", row_head.val
            self.dll.remove_column_heads_for_row(row_head)
            rows = self.dll.get_rows_impacted_by_row(row_head)
            for row in rows:
                self.dll.remove_row(row)

        return len(column_heads)
    
        
    def recursive_solve(self):
        if self.dll.is_completely_empty():
            return True

        if self.dll.has_column_empty():
            return False

        cnt = 1
        row_head = self.dll.select_row(cnt)
        while not row_head:
            cnt += 1
            row_head = self.dll.select_row(cnt)

        while True:
            if row_head == self.dll.root: break

            self.solution.append(row_head)
            rows = self.dll.get_rows_impacted_by_row(row_head)

            self.dll.remove_column_heads_for_row(row_head)
            for row in rows:
                self.dll.remove_row(row)

            if self.recursive_solve():
                return True

            self.dll.restore_column_heads_for_row(row_head)
            for row in rows:
                self.dll.restore_row(row)

            self.solution.remove(row_head)
            row_head = row_head.down

        return False

