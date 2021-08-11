from priorityqueue import PriorityQueue

State,Operator,Problem = object,object,object  # Names for parameter annotations

protocol = ['get_start_state','get_stop_state','get_all_operators']

#Given a solution (a list of operators that when applied on the start state generate the stop
#  state), return the solution as a nicely formatted string (typically, this result is printed).
def illustrate_solution (state : State, operators : [Operator]):
    if operators == None:
        return 'No solution found'

    if len(operators) == 0:
        return 'Trivial solution found (start state = stop state)'

    solution = 'Solution length = {}\n  {}: Starting State\n'.format(len(operators),state)
    try:
        for op in operators:
            state = op.apply(state);
            solution += '  ' + str(state) + ': ' + str(op) + '\n'
        solution += '  ' + str(state) + ': Final State'
    except Exception as e:
        solution += 'Exception during state application'
    return solution


#Find solution to a problem and return it.
#The actual argument that matches the parameter "exploring" might be a list
#  (see breadth_first_solution) or a priority queue (see best_first_solution):
#  the algorithm for #  the solution is the same, but depends on how pop is implemented.
def solve_it (problem : Problem, exploring : 'List or Priority Queue'):
    operator_count = 0;
    start          = problem.get_start_state()
    stop           = problem.get_stop_state()
    
    #Trivial solutions: no operators needed
    if start == stop:
        print('Found Solution: Operator applications = 0 (start state is also stop state)')
        return []

    
    operators = problem.get_all_operators()
    
    solutions = problem.solutions
    solutions.clear()
    
    exploring.append(start)
    solutions[start] = []
    
    #Are there still states to explore
    while len(exploring) != 0:
        current_state = exploring.pop(0)  #state to explore next: front of list/highest priority
        #Try all operators and examine the states they lead to for uniqueness
        #  and further processing
        for op in operators:
            operator_count += 1
    
            new_state = op.apply(current_state)

            if new_state not in solutions:
                #extend solution to include new state and this operator to reach it
                current_solution = solutions[current_state]
                new_solution = list(current_solution)
                new_solution.append(op)

                #if stop state, return solution
                if new_state == stop:
                    print('Found Solution: Operator applications = {}/states reached = {}'.format(operator_count,len(solutions)+1))
                    return new_solution

                #update solutions map and exploring queue
                solutions[new_state] = new_solution
                exploring.append(new_state)

   
    #Failed to find solution; return None.
    print('No Solutions: Operator applications = {}/states reached = {}'.format(operator_count,len(solutions)+1))
    return None


#Use breadth-first searching to find an "optimal" solution (the one
#  with the minimum number of operators needed to transform the initial
#  state to the final state).
def breadth_first_solution (problem: Problem):
    return solve_it(problem, []);



#Use the key_lambda function (returning the priority of any state; higher priority states are
#  considered heuristically closer to the stop state) to try to find a solution faster (search
#  the tree, looking at fewer internal states), but may not find an optimal solution (unless the
#  heuristic satisfies the A* property below).
#The above is a pure best-first algorithm. If the key_lambda function computes its result by
#  adding the following, then it has the A* property.
#    (a) the number of operators it takes to get to a state, and
#    (b) the heuristic does not over-estimate how many operators it takes to reach the next state
#  then the result will be an "optimal" solution, typically found by examining more operators
#  than a pure best-first search but fewer than a breadth-first search.
def best_first_solution (problem : Problem, key_lambda = lambda x : x, reverse = False):
    return solve_it(problem, PriorityQueue(key = key_lambda, reverse = reverse))