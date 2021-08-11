from backtracking import *
from goody import irange, safe_open, implements_protocol, ProtocolError
from stopwatch import Stopwatch


class Aspect:
    def __hash__(self):
        return self.row_working_on * self.col_working_on
    
    def __init__(self, row, col, problem):
        self.row_working_on = row
        self.col_working_on = col
        self.problem        = problem
        self.ok_values = [i for i in irange(1,9)]
        for c in range(9):
            if problem.puzzle[row][c] in self.ok_values:
                self.ok_values.remove(problem.puzzle[row][c])
        for r in range(9):
            if problem.puzzle[r][col] in self.ok_values:
                self.ok_values.remove(problem.puzzle[r][col])
        for r in range(row//3*3,row//3*3+3):
            for c in range(col//3*3,col//3*3+3):
                if problem.puzzle[r][c] in self.ok_values:
                    self.ok_values.remove(problem.puzzle[r][c])

    def __repr__(self):
        return 'Sudoku.Aspect[row={},col={}]'.format(self.row_working_on,self.col_working_on)

    def __iter__(self):
        for v in self.ok_values:
            yield v
            
    def __eq__(self,right):
        return self is right or\
              (self.row_working_on == right.row_working_on and self.col_working_on == right.col_working_on)
                
    def row(self):
        return self.row_working_on
    
    def col(self):
        return self.col_working_on


class Problem:
    def __init__(self,puzzle):
        self.puzzle = [9*[0] for _i in range(9)]
        for r in range(9):
            for c in range(9):
                self.puzzle[r][c] = puzzle[r][c]

    def __repr__(self):
        answer = 'Problem[\n'
        for r in range(9):
            for c in range(9):
                answer+=' '+str(self.puzzle[r][c])
            answer += '\n'
        return answer + ']'

    def reduce (self):
        return Problem(self.puzzle)

    def choose_and_exclude_aspect(self):
        for r in range(9):
            for c in range(9):
                if self.puzzle[r][c] == 0:
                    return Aspect(r,c,self)
        # No aspects left!
        raise BacktrackSucceed

    def bind_aspect_value (self, aspect, value):
        self.puzzle[aspect.row_working_on][aspect.col_working_on] = value

    def unbind_aspect_value (self, aspect):
        self.puzzle[aspect.row_working_on][aspect.col_working_on] = 0

    def get_solution (self):
        return {Aspect(r,c,self):self.puzzle[r][c] for r in range(9) for c in range(9)}





def read_puzzle():
    file = safe_open('Enter file containing Sudoko puzzle', 'r', 'File not found', 'sudoku.txt').read()
    file = file.replace('\n',' ').split()
    puzzle = [9*[0] for _i in range(9)]
    i = 0
    for r in range(9):
        for c in range(9):
            puzzle[r][c] = int(file[i])
            i += 1
    return puzzle

def print_solution (solution):
    puzzle = [9*[0] for _i in range(9)]
    for k,v in solution.items():
        puzzle[k.row()][k.col()] = v

    for r in range(9):
        for c in range(9):
            print(' {}'.format(puzzle[r][c]),end='')
            if c != 8 and (c+1)%3 == 0:
                print(" |",end='')
        print()
        if r != 8 and (r+1)%3 == 0:
           print('-------+-------+------')


puzzle = read_puzzle()
problem = Problem(puzzle)
if not implements_protocol(problem, protocol):
    print('Problem class does not implement protocol: missing one or more methods')
    raise ProtocolError
timer = Stopwatch(running_now=True)
solution = solve_it(problem)
print('\n\nTime to search for single solution =',timer.read(),'secs')
print('Single Solution to:\n', problem, '\n', sep='')
print_solution(solution)