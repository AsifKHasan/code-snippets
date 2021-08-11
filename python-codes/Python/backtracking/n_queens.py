import prompt
from goody import implements_protocol, ProtocolError
from stopwatch import Stopwatch
from backtracking import *

class Aspect:
    def __hash__(self):
        return self.row_working_on * sum(self.ok_columns)
    
    def __init__(self, row_working_on, problem):
        self.row_working_on = row_working_on
        self.problem        = problem
        self.ok_columns     = []
        for c in range(self.problem.max_n):
            for k,v in self.problem.assignments.items():
                row    = k.row_working_on
                column = v
                if c == column or abs(c - column) == (self.row_working_on - row):
                    break
            else: # No break: all placements work
                self.ok_columns.append(c)

    def __repr__(self):
        return 'Aspect[row_working_on={},ok_columns={}]'.format(self.row_working_on,self.ok_columns)
                
    def __iter__ (self):
        for c in self.ok_columns:
            yield c

    def __eq__(self, right):
        return self is right or self.row_working_on == right.row_working_on



class Problem:
    def __init__(self, board_size):
        self.max_n       = board_size
        self.assignments = {}

    def __repr__(self):
        return 'Problem[max_n={};assignments={}]'.format(self.max_n, self.assignments)

    def reduce (self):
        p = Problem(self.max_n)
        p.assignments = dict(self.assignments)
        return p

    def choose_and_exclude_aspect(self):
        if len(self.assignments) == self.max_n:
            raise BacktrackSucceed
        return Aspect(len(self.assignments), self)

    def bind_aspect_value (self, aspect, value):
        self.assignments[aspect] = value

    def unbind_aspect_value (self, aspect):
        del self.assignments[aspect]

    def get_solution (self):
        return self.assignments





n = prompt.for_int("Enter N for NxN Chessboard", 4)
problem = Problem(n)
if not implements_protocol(problem, protocol):
    print('Problem class does not implement protocol: missing one or more methods')
    raise ProtocolError
timer = Stopwatch(running_now=True)
solution = solve_it(problem)
print('\n\nTime to search for single solution =',timer.read(),'secs')
print('Single Solution to: ', problem)
print(illustrate_solution(solution))

problem = Problem(n)
if not implements_protocol(problem, protocol):
    print('Problem class does not implement protocol: missing one or more methods')
    raise ProtocolError
solutions = []
timer.reset(running_now=True)
solve_all(problem, solutions)
print('\n\nTime to search for all solutions =',timer.read(),'secs')

print('All Solutions to: ', problem)
if solutions == None:
    print('No solutions')
else:
    print('\n# Solutions = ', len(solutions))
    for c,s in enumerate(solutions, 1):
        print('\nSolution #', c, ' ' + illustrate_solution(s))
    
