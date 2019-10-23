#! python

class CrossCycleLinkedNode():
    def __init__(self, x, is_head=False):
        self.val = x
        self.is_head = is_head
        self.row_head = self
        self.col_head = self
        self.up = self
        self.down = self
        self.left = self
        self.right = self
        self.is_removed_from_column = False
        self.is_removed_from_row = False
        
    def remove_column(self):
        if self.is_removed_from_column: return
        
        self.left.right = self.right
        self.right.left = self.left
        self.is_removed_from_column = True

    def restore_column(self):
        if not self.is_removed_from_column: return
        
        self.left.right = self
        self.right.left = self
        self.is_removed_from_column = False
        
    def remove_row(self):
        if self.is_removed_from_row: return
    
        self.up.down = self.down
        self.down.up = self.up
        self.is_removed_from_row = True

    def restore_row(self):
        if not self.is_removed_from_row: return
        
        self.up.down = self
        self.down.up = self
        
        self.is_removed_from_row = False
