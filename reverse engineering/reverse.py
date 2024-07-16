from z3 import *
def funcy(s):
    summa = sum(ord(char) for char in s)
    stre = summa/2
    
    return stre
print(funcy(input()))

flagged = 580.0
solver = Solver()
s = str('what is this')
x = 260
solver.add(2*x == sum(ord(char) for char in s))
if solver.check() == sat:
        model = solver.model()
        # Extract and print the string that produces the target_sum
        result_string = model[s].as_string()
        print(f"Found string: '{result_string}'")
else:
        print("Failed to find a string.")







