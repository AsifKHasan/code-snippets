a2b([], []).
a2b([a|La], [b|Lb]) :- a2b(La, Lb).

second(X, List) :- List = [_,X|_].

tran(eins,one).
tran(zwei,two).
tran(drei,three).
tran(vier,four).
tran(fuenf,five).
tran(sechs,six).
tran(sieben,seven).
tran(acht,eight).
tran(neun,nine).

listtran([], []).
listtran([E|Le], [G|Lg]) :- (tran(E, G) ; tran(G, E)),
    listtran(Le, Lg).
