#! python


from node import CrossCycleLinkedNode as Node


class DancingLinkList():
    def __init__(self, num_of_columns):
        self.root = Node(0)
        self.column_heads = []
        self.row_heads = []
        
        left_node = self.root
        for i in xrange(0, num_of_columns):
            node = Node(i+1, True)
            node.row_head = self.root
            
            left_node.right = node
            node.left = left_node

            left_node = node
            self.column_heads.append(node)

        self.root.left = left_node
        left_node.right = self.root

    def is_completely_empty(self):
        return self.root == self.root.right and self.root == self.root.down

    def select_row(self, cnt):
        if cnt <= 0: return None
        
        col_head = self.root.right
        if col_head == self.root: return None

        while col_head != self.root:
            node = col_head
            i = cnt
            while i > 0:
                node = node.down
                if node == col_head: break
                i -= 1

            if i == 0 and node.down == col_head:
                return node.row_head
            
            col_head = col_head.right
        return None

    def has_column_empty(self):
        node = self.root.right
        while node != self.root:
            if node.down == node:
                return True
            node = node.right
        return False
    
    def init_row_head(self, i):
        node = Node(i+1, True)
        node.col_head = self.root
        
        self.row_heads.append(node)

        top_node = self.root.up
        self.root.up = node
        node.down = self.root
        top_node.down = node
        node.up = top_node

    def insert_node(self, i, j, val):
        if len(self.row_heads) < i: return False
        if len(self.column_heads) < j: return False

        if len(self.row_heads) == i:
            self.init_row_head(i)
        
        row_head = self.row_heads[i]
        col_head = self.column_heads[j]
        
        top_node = col_head.up
        while top_node.row_head.val-1 > i:
            top_node = top_node.up

        if top_node.row_head.val-1 == i:
            # This location already has a node
            return

        node = Node(val)
        node.row_head = row_head
        node.col_head = col_head

        # insert node into the column
        node.down = top_node.down
        node.down.up = node
        top_node.down = node
        node.up = top_node

        left_node = row_head.left          
        while left_node.col_head.val-1 > j:
            left_node = left_node.left

        if left_node.col_head.val-1 == j:
            # This location already has a node
            return

        # insert node into the row
        node.right = left_node.right
        node.right.left = node
        left_node.right = node
        node.left = left_node

    def get_empty_column_heads(self):
        heads = []
        col_head = self.root.right
        while col_head != self.root:
            if col_head.down == col_head:
                heads.append(col_head)
            col_head = col_head.right
        return heads

    def get_single_node_column_heads(self):
        heads = []
        col_head = self.root.right
        while col_head != self.root:
            if col_head.down != col_head and col_head.down.down == col_head:
                heads.append(col_head)
            col_head = col_head.right
        return heads

    def get_columns_impacted_by_row(self, row_head):
        columns = []
        node = row_head.right
        while node != row_head:
            columns.append(node.col_head)
            node = node.right
        return columns

    def get_rows_impacted_by_row(self, row_head):
        rows = []
        node = row_head.right
        while node != row_head:
            col_head = node.col_head
            col_node = col_head.down
            while not col_node.is_head:
                if not col_node.row_head in rows:
                    rows.append(col_node.row_head)
                col_node = col_node.down
            node = node.right
        return rows

    def remove_column_heads_for_row(self, row_head):
        node = row_head.right
        while node != row_head:
            node.col_head.remove_column()
            node = node.right

    def restore_column_heads_for_row(self, row_head):
        node = row_head.right
        while node != row_head:
            node.col_head.restore_column()
            node = node.right
        
    def remove_row(self, row_head):
        # always starts from the head node of a row
        node = row_head
        while True:
            node.remove_row()
            node = node.right
            if node == row_head: break

    def restore_row(self, row_head):
        node = row_head
        while True:
            node.restore_row()
            node = node.right
            if node == row_head: break
            
