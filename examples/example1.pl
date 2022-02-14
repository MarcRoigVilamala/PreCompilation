twoHeads(T) :- heads1(T), heads2(T).

someHeads(T) :- heads1(T).
someHeads(T) :- heads2(T).

aHead(T, 1) :- heads1(T), \+heads2(T).
aHead(T, 2) :- heads2(T), \+heads1(T).
