#! python

def init_raw_matrix(filename):
    raw_matrix = []
    
    f = open(filename)
    
    line = f.readline()
    tokens = line.strip().split()
    size = int(tokens[0])
    
    for i in xrange(0,size):
        line = f.readline()
        tokens = line.strip().split()

        row = [int(e) for e in tokens]
        raw_matrix.append(row)
        
    f.close()
    
    return raw_matrix


def print_raw_matrix(raw_matrix):
    for row in raw_matrix:
        for e in row:
            print e,
        print ""
