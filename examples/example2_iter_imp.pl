atTime(T) :- Tprev is T - 1, Tprev >= 0, atTime_(Tprev), \+decrease(T).
atTime(T) :- increase(T).

% Add this to prevent errors of not defined clauses
decrease(false).
increase(false).
