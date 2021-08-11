from backtracking import *
from stopwatch import Stopwatch
import prompt
from goody import safe_open, implements_protocol, ProtocolError

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def profile_of(word : str) -> [int]:
    prof = 26*[0]
    for c in word.lower():
        prof[alphabet.index(c)] += 1
    return prof

def word_of(profile : [int]) -> str:
    return ''.join(profile[i]*alphabet[i] for i in range(26))

def can_use(word : [int], remaining : [int]) -> bool:
    return all(wc<=rc for wc,rc in zip(word,remaining))

def subtract(word : [int], remaining : [int]) -> [int]:
    return [rc-wc for wc,rc in zip(word,remaining)]

def done(remaining : [int]) -> bool:
    return all(c == 0 for c in remaining)

def focus(profile : {str:[int]}, prof : [int]) -> {str:[int]}:
    return {w:p for w,p in profile.items() if can_use(p,prof)}
     

class Aspect:
    def __hash__(self):
        return self.word_count
    
    def __init__(self, remaining, word_count, problem):
        self.word_count = word_count
        self.problem    = problem
        self.ok_words   = (w for w,p in problem.profiles.items() if can_use(p,remaining))

    def __repr__(self):
        return 'Aspect[word_count={}]'.format(self.word_count)
                
    def __iter__ (self):
        for c in self.ok_words:
            yield c

    def __eq__(self, right):
        return self is right or (self.word_count == right.word_count)



class Problem:
    def __init__(self, profiles, remaining, word_count):
        self.profiles    = profiles
        self.remaining   = remaining
        self.word_count  = word_count
        self.assignments = {}

    def __repr__(self):
        return 'Problem[profiles=<too big>;remaining={};word_count={};assignments={}]'.format(word_of(self.remaining),self.word_count,self.assignments)

    def reduce (self):
        remaining     = subtract(profile_of(self.value),self.remaining)
        profiles      = focus(self.profiles,remaining)
        p             = Problem(profiles,remaining,self.word_count-1)
        p.assignments = dict(self.assignments)
        return p

    def choose_and_exclude_aspect(self):
        if done(self.remaining):
            raise BacktrackSucceed
        if self.word_count == 0:
            raise BacktrackFail
        return Aspect(self.remaining, self.word_count, self)

    def bind_aspect_value (self, aspect, value):
        self.value = value
        self.assignments[aspect] = value

    def unbind_aspect_value (self, aspect):
        del self.assignments[aspect]

    def get_solution (self):
        return self.assignments




full_profile = {}
for word in safe_open('Dictionary file','r','File not found','dict.txt'):
    word = word.rstrip()
    full_profile[word.lower()] = profile_of(word)

phrase = prompt.for_string('\nEnter string to process').lower()
max    = prompt.for_int('Enter maximum number of words (-1 for any number)',-1, lambda x : x > 0 or x == -1)

phrase = ''.join(c for c in phrase if c in alphabet)
phrase_prof = profile_of(phrase)

problem = Problem(focus(full_profile,phrase_prof),phrase_prof,max)
if not implements_protocol(problem, protocol):
    print('Problem class does not implement protocol: missing one or more methods')
    raise ProtocolError
 
timer = Stopwatch(running_now=True)
solution = solve_it(problem)
print('\n\nTime to search for single solution =',timer.read(),'secs')
print('Single Solution to:\n', problem, sep='')
print(illustrate_solution(solution))


problem = Problem(full_profile,phrase_prof,max)
if not implements_protocol(problem, protocol):
    print('Problem class does not implement protocol: missing one or more methods')
    raise ProtocolError

solutions = []
timer.reset(running_now=True)
solve_all(problem, solutions)
print('\n\nTime to search for all solutions =',timer.read(),'secs')
 
#print('All Solutions to: ', problem)
if solutions == None:
    print('No solutions')
else:
    print('\n# Solutions = ', len(solutions))
    for c,s in enumerate(solutions, 1):
        print('\nSolution #', c, ' ' + illustrate_solution(s))


    
    
# while True:
#     phrase = prompt.for_string('\nEnter string to process',default=phrase).lower()
#     if phrase == '':
#         break;
#     phrase = ''.join(c for c in phrase if c in alphabet)
#     phrase_prof = profile_of(phrase)
#     
#     max    = prompt.for_int('Enter maximum number of words (-1 for any number)',-1, lambda x : x > 0 or x == -1)
#     
#     timer = Stopwatch()
#     timer.start()
#     answer = anagram(phrase_prof,max,focus(full_profile,phrase_prof))
#     timer.stop()
#     if answer:
#         for a in answer:
#             print(a)
#         print(len(answer),'results in',timer.read(),'seconds')
#     else:
#         print(None)
        
        
        