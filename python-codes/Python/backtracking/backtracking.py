# Classes for signaling success or failure to find a solution on the current path

class BacktrackFail(Exception):
    pass

class BacktrackSucceed(Exception):
    pass

Aspect,Value,Problem = object,object,object   # Names for parmeter annotations

protocol = ['reduce','choose_and_exclude_aspect','bind_aspect_value','unbind_aspect_value','get_solution']

#Given a solution (a dict mapping aspects to their values), return the solution
#  as a nicely formatted string (typically, this result is printed).
def illustrate_solution (assignments : {Aspect:Value}) -> str:
    if len(assignments) == 0:
        return "No solution"
    else:
        return 'Bindings:\n  ' +\
               '\n  '.join('{} -> {}'.format(k,v) for k,v in assignments.items())



#Find the first solution to a problem and return it.
#The body of solve_it and solve_all are very similar.

def solve_it (problem : Problem) -> {Aspect:Value}:
    try:
        #Choose an aspect (and exclude it from being chosen again)
        aspect = problem.choose_and_exclude_aspect();
    
        #For every possible value for that aspect, recursively attempt to
        #  solve a reduced problem with that aspect bound to that value
        #If a solution is found, return it; if not, unbind the aspect and
        #  continue looping (finding a new value to bind to the aspect).
        #If BacktrackSucceed or BacktrackFail is thrown, return the answer or
        #  {} appropriately
        for v in aspect:#.choices():
            problem.bind_aspect_value(aspect, v)
            temp = solve_it(problem.reduce())
            if len(temp) != 0:
                return temp
            problem.unbind_aspect_value(aspect)

    except BacktrackSucceed:
        return problem.get_solution()
    except BacktrackFail:
        return {}               # Possibly no aspect can be chosen 
    
    return {}                   # Tried every value for aspect, but all failed




#Find all solutions to a problem and return a set of them.
#The body of solve_it and solve_all are very similar
def solve_all (problem, solutions : [{Aspect:Value}]) -> None:
    try:
        #Choose an aspect (and exclude it from being chosen again)
        aspect = problem.choose_and_exclude_aspect();
    
        #For every possible value for that aspect, recursively attempt to
        #  solve a reduced problem with that aspect bound to that value
        #If a solution is found, add it to solutions and continue finding
        #  solutions; if not, unbind the aspect and continue looping (finding
        #  a new value to bind to the aspect).
        #If BacktrackFail is thrown, return the answer or null appropriately)
        for v in aspect:
            problem.bind_aspect_value(aspect, v)
            solve_all(problem.reduce(), solutions)
            problem.unbind_aspect_value(aspect)
    except BacktrackSucceed:
        solutions.append(problem.get_solution())
    except BacktrackFail:
        pass                    # Skip this aspect/value binding 
    
    return None
