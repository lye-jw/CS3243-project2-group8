import sys
import copy

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists
        self.domains = list()
        self.unassigned_vars = set()
        self.reduced_vars = []

    def solve(self):
        self.init_domains()
        self.backtrack()
        print(puzzle)
        return self.ans
    
    def backtrack(self):
        if len(self.unassigned_vars) == 0:
            return True

        #variable selection
        curr_var = self.most_constr_var(self.unassigned_vars)
        #value selection
        domain = self.var_domain(self.domains,curr_var)

        for index in range(9):
            if domain[index] == 1:
                self.assign_val(curr_var, index+1)
                if self.constraints_check(curr_var, index+1):
                    forwardcheck_succeeds = self.forward_checking(curr_var, index + 1)
                else:
                    self.unassign_val(curr_var, index+1)
                    continue

                if forwardcheck_succeeds and self.backtrack():
                    return True
                else:
                    self.unassign_val(curr_var, index+1)
                    self.undo_last_forwardcheck()

        #add back to unassigned                
        self.unassigned_vars.add(curr_var)
        return False
    
    def most_constr_var(self,unassigned_vars):
        MCV = unassigned_vars.pop()
        return MCV
    
    def var_domain(self,domainlist,curr_var):
        var_index = curr_var[0]*9 + curr_var[1]
        curr_domain = self.domains[var_index]
        return curr_domain
    
    def assign_val(self,curr_var,value):
        self.puzzle[curr_var[0]][curr_var[1]] = value
        return 1
    
    def unassign_val(self,curr_var,value):
        self.puzzle[curr_var[0]][curr_var[1]] = 0
        return 1
    
    def init_domains(self):
        domainset = [1,1,1,1,1,1,1,1,1]
        for row in range(9):
            for col in range(9):
                self.domains.append(copy.copy(domainset))
                if self.puzzle[row][col] == 0:
                    self.unassigned_vars.add((row,col))
        for row in range(9):
            for col in range(9):
                if self.puzzle[row][col] != 0:           
                    pass
        return 1

    def constraints_check(self,curr_var,value):
        row = curr_var[0]
        col = curr_var[1]
        for c in range(9):
            if c != col:
                if self.puzzle[row][c] == value:
                    return False
        for r in range(9):
            if r != row:
                if self.puzzle[r][col] == value:
                    return False
        layers = [[0,1,2],[3,4,5],[6,7,8]]
        for layer in layers:
            if row in layer:
                neighbour_row = layer
            if col in layer:
                neighbour_col = layer
        for sqrow in neighbour_row:
            for sqcol in neighbour_col:
                if sqrow != row or sqcol != col:
                    if self.puzzle[sqrow][sqcol] == value:
                        return False
        return True

    def forward_checking(self, curr_var, value):
        row = curr_var[0]
        col = curr_var[1]

        # Remove value from domain of var in same column
        for c in range(9):
            if c != col:
                if not self.reduce_var(row, c, value):
                    return False

        # Remove value from domain of var in same row
        for r in range(9):
            if r != row:
                if not self.reduce_var(r, col, value):
                    return False

        layers = [[0,1,2],[3,4,5],[6,7,8]]
        for layer in layers:
            if row in layer:
                neighbour_row = layer
            if col in layer:
                neighbour_row = layer 
        for sqrow in neighbour_row:
            for sqcol in neighbour_col:
                if sqrow != row or sqcol != col:
                    if not self.reduce_var(sqrow, sqcol, value]:
                        return False
        return True

    def reduce_var(row, col, value):
        reduce_ind = row * 9 + col
        reducedvar = self.domains[reduce_ind]
        reducedvar[value] = 0
        self.reduced_vars.append((row, col, value))
        if reducedvar:
            return True
        else:
            return False

    def undo_last_forwardcheck():
        last_reduced_var = self.reduced_vars.pop()
        row = last_reduced_var[0]
        col = last_reduced_var[1]
        removed_val = last_reduced_var[2]
        reduce_ind = row * 9 + col
        self.domains[reduce_ind][removed_val] = 1
    
    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
