increment(X, Y) :- Y is X + 1.

sum(A, B, S) :- S is A + B.

addone([], []).
addone([A|La], [B|Lb]) :- B is A + 1, addone(La, Lb).
