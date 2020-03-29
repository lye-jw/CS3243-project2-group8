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
        self.unassignedVars = set()

    def solve(self):
        self.initDomains()
        self.backtrack()
        print(puzzle)
        return self.ans
    def backtrack(self):
        if len(self.unassignedVars) == 0:
            return True

        #variable selection
        currVar = self.mostConstrVar(self.unassignedVars)
        #value selection
        domain = self.varDomain(self.domains,currVar)

        for index in range(9):
            if domain[index] == 1:
                self.assignVal(currVar,index+1)
                if self.validCheck(currVar,index+1) == False:
                    self.unassignVal(currVar,index+1)
                    continue
                if self.backtrack() == False:                    
                    self.unassignVal(currVar,index+1)
                    continue
                else:
                    return True
            else:
                continue

        #add back to unassigned                
        self.unassignedVars.add(currVar)
        return False
    def mostConstrVar(self,unassignedVars):
        MCV = unassignedVars.pop()
        return MCV
    def varDomain(self,domainList,currVar):
        varIndex = currVar[0]*9 + currVar[1]
        currDomain = self.domains[varIndex]
        return currDomain
    def assignVal(self,currVar,value):
        self.puzzle[currVar[0]][currVar[1]] = value
        return 1
    def unassignVal(self,currVar,value):
        self.puzzle[currVar[0]][currVar[1]] = 0
        return 1
    def initDomains(self):
        domainSet = [1,1,1,1,1,1,1,1,1]
        for row in range(9):
            for col in range(9):
                self.domains.append(copy.copy(domainSet))
                if self.puzzle[row][col] == 0:
                    self.unassignedVars.add((row,col))
        for row in range(9):
            for col in range(9):
                if self.puzzle[row][col] != 0:           
                    pass
        return 1

    def validCheck(self,currVar,value):
        row = currVar[0]
        col = currVar[1]
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
                neighbourRow = layer
            if col in layer:
                neighbourCol = layer 
        for sqRow in neighbourRow:
            for sqCol in neighbourCol:
                if sqRow != row or sqCol != col:
                    if self.puzzle[sqRow][sqCol] == value:
                        return False
        return True         
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
