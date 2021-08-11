from statespace import *
from goody import implements_protocol, ProtocolError
from stopwatch import Stopwatch


class State:
    def __hash__(self):
        return sum(self.jug_state)
    
    def __init__(self,state,problem=None):
        if problem == None: # just copy state
            self.problem   = state.problem
            self.jug_state = list(state.jug_state)
        else:               # jug_state and problem
            self.problem   = problem
            self.jug_state = list(state)
            # Verify that state is legal: each indexed value >= 0 and <= problem.jug_sizes

    def __repr__(self):
        return 'State[jug_state=[' + ','.join(str(js) for js in self.jug_state) +']]';

    def __eq__(self,right) -> bool:
        return self is right or self.jug_state == right.jug_state

    def how_close(self):
        #answer = 0;                                 #f(x) = h(x)
        answer = len(self.problem.solutions[self])   #f(x) = #ops + h(x) : the a* algorithm
        for i in range(len(self.problem.jug_sizes)):
            answer += (0 if self.jug_state[i] == self.problem.stop.jug_state[i] else  1)
            #answer += abs(self.jug_state[i]-self.problem.stop.jug_state[i]) #Alternative
            #answer += (self.jug_state[i]-self.problem.stop.jug_state[i]) ** 2    #Alternative
        return answer;



class Operator:
    def __hash__(self):
        return self.jug_from**2 + self.jug_to
        
    def __init__(self,jug_from,jug_to):
        self.jug_from = jug_from
        self.jug_to   = jug_to

    def __repr__(self):
        return 'pour from jug {} to {}'.format(self.jug_from+1,self.jug_to+1)
        return '{} -> {}'.format(self.jug_from+1,self.jug_to+1)

    def __eq__(self,right) -> bool:
        return self is right or\
               (self.jug_from == right.jug_from and self.jug_to == right.jug_to)
    def apply (self,state):
        result_state = State(state.jug_state,state.problem)
        to_capacity = state.problem.jug_sizes[self.jug_to] - state.jug_state[self.jug_to];
        if state.jug_state[self.jug_from] <= to_capacity:
            #Empty jug_from (becomes 0) into jug_to (incremented)
            result_state.jug_state[self.jug_to] += state.jug_state[self.jug_from];
            result_state.jug_state[self.jug_from] =  0
        else:
            #fill jug_to (becomes full) from jug_from (decremented)
            result_state.jug_state[self.jug_from] -= to_capacity;
            result_state.jug_state[self.jug_to]   =  state.problem.jug_sizes[self.jug_to]
        return result_state;


class Problem:
    def __init__(self,all_jug_sizes, start_jugs, stop_jugs):
        assert len(all_jug_sizes) == len(start_jugs)
        # Check sizes >= 0, start <= sizes
        self.jug_sizes = list(all_jug_sizes)
        self.start     = State(start_jugs,self)
        self.stop      = State(stop_jugs,self)
        self.solutions = {} 
        self.operators = set()
        #Transfer i->j and j->i  for all i != j
        for i in range(len(self.jug_sizes)):
            for j in range(len(self.jug_sizes)):
                if i != j:
                    self.operators.add(Operator(i, j));
                    self.operators.add(Operator(j, i));

    def __repr__(self):
        return 'Problem[jug_sizes=[' + ','.join(str(js) for js in self.jug_sizes) +\
               '],start=' + str(self.start) + ',stop=' + str(self.stop) +']'

    def get_start_state (self):
        return self.start

    def get_stop_state(self):
        return self.stop

    def get_all_operators(self):
        return self.operators;





sizes = [5,11,13,24]  #See problem below
start = [0,0,0,24]
stop  = [0,8,8,8]

# sizes = [3,5,8]  #See problem above
# start = [0,0,8]
# stop  = [0,4,4]


problem = Problem(sizes,start,stop)
if not implements_protocol(problem, protocol):
    print('Problem class does not implement protocol: missing one or more methods')
    raise ProtocolError

#Show all operators in the problem
print(problem)
print('Operators for problem')
for o in problem.get_all_operators():
    print('  ' + str(o))
print()

#Try solution via breadth-first tree traversal
print('Breadth-first solution')
timer = Stopwatch(running_now=True)
solution = breadth_first_solution(problem)
print('Time spent searching for breadth-first solution =',timer.read())
print(illustrate_solution(problem.get_start_state(),solution))

#Try solution via best-first tree traversal
print('\nBest-first solution')
timer.reset(running_now=True)
solution = best_first_solution(problem, lambda x : x.how_close(), reverse = True)
print('Time spent searching for best-first solution =',timer.read())
print(illustrate_solution(problem.get_start_state(),solution))





# Problem from http://www.cut-the-knot.org/ctk/Water.shtml
# 
# Three men robbed a gentleman of a vase, containing 24 ounces of balsam.
# Whilst running away they met a glass seller, of whom they purchased
# three vessels. On reaching a place of safety they wished to divide the
# booty, but found that their vessels could hold 5, 11, and 13 ounces respectively.
# How could they divide the balsam into equal portions?
