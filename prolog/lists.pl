/*
use_module(library(clpfd)).

list_length([], 0).
list_length([_|Ls], N) :-
    N #> 0,
    N #= N0 + 1,
    list_length(Ls, N0).
*/

len([], 0).
len([_|T], N) :- len(T, X), N is X + 1.

% Tail recursion version
accLen([_|T], A, L) :-  Anew is A + 1, accLen(T, Anew, L).
accLen([], A, A).
leng(List, Length) :- accLen(List, 0, Length).


accMax([H|T], A, Max) :-
   H > A,
   accMax(T, H, Max).

accMax([H|T], A, Max) :-
   H =< A,
   accMax(T, A, Max).

accMax([], A, A).

max(List,Max) :-
     List = [H|_],
     accMax(List, H, Max).
