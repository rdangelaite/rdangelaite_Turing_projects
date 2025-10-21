### Calculator with a memory

Creates a basic calculator class object, with a memory.

This calculator can do addition, substraction, multiplication, division and find nth roots.

The calculator can accept one or two arguments. If one argument is provided the calculator will do operations with number in memory. If two arguments are provided it will do operations with them and overwrite memory with the result.

To call this calculator simply assign it to a variable:

```
from calculator_rasadangelaite import Calculator
calc = calculator.Calculator()
calc()                                            #returns the number in memory it currently holds - in this case 0
```

Default value is 0, but you can specify a starting number in ().
The calculator holds the number in memory, to which above mentioned operations can be done.

The memory can be reset back to 0 or overwriden with another number:

```
calculator.reset() #sets memory value to 0
calculator(10)     #sets memory value to 10
```

## Class methods

### add

Adds a provided argument to the number in memory:

calc.add(argument)

example:
```
calc = calculator.Calculator() #the calculator is initialized and 0 is stored in memory
calc.add(10)                   #returns 10
calc()                         #returns what it is stored in memory - 10
```

Two arguments can also be provided.

calc.add(argument1, argument2)

example:
```
calc = calculator.Calculator()
calc.add(10, 15)                # returns 15 and stores the result in memory
```

Results overwrite number in memory.

following operations are analogous to add

### sub

Subtracts provided argument from the number in memory or subtracts argument2 from argument1. Results overwrite the memory:

calc.sub(argument1, argument2)

```
calc = calculator.Calculator()
calc(10)                        # stores 10 in memory
calc.sub(7)                     # returns 3

calc.sub(8, 9)                  # returns -1 and stores the result in memory
```


### mul

Multiplies number in memory by provided argument or multiplies two provided arguments. Results overwrite the memory:

calc.mul(argument1, argument2)

```
calc = calculator.Calculator()
calc(10)                        
calc.mul(2)                     # returns 20

calc.mul(5, 9)                  # returns 45
```

### div

Divides number in memory by provided argument. If two argument provided first argument is divided by the second one. Results overwrite the memory:

calc.div(argument1, argument2)

```
calc = calculator.Calculator()
calc(6)                        
calc.div(2)                     # returns 3

calc.div(25, 2)                 # returns 12.5
```

It does not divide by 0 and returns error instead:

```
calc.div(0)           #prints out "ZeroDivisionError: division by zero"
calc.div(12, 0)       #prints out "ZeroDivisionError: division by zero"
```

Errors do not reset or overwrite memory:

```
calc = calculator.Calculator()
calc(8)                        
calc.div(2)                     
calc()                          # returns 4
calc.div(0)                     # prints out "ZeroDivisionError: division by zero"
calc()                          # returns 4
```

### nroot

Takes number in the memory and nth root of depending on provided argument. If two arguments provided, it takes the first argument and takes its root, then root level depends on second provided argument. Results overwrite the memory.

calc.nroot(argument1, argument2)

How it works:

memory = memory ** 1 / argument
memory = argument1 ** 1 / argument2

Or written in python:

memory = pow(memory, 1/argument)
memory = pow(argument1, 1/argument2)

Example:

```
calc = calculator.Calculator()
calc(8)                        
calc.nroot(3)                   # returns 2

calc.nroot(9, 2)                # returns 3
```

There are following restrictionswhich raises errors:
*Cannot make 0th roots as it is not defined:
```
calc.nroot(0)     # prints out ZeroDivisionError: division by zero: unable to make zeroth root
calc.nroot(2, 0)  # prints out ZeroDivisionError: division by zero: unable to make zeroth root
```

*Does not take negavite and complex roots of 0.
```
calc(0)           
calc.nroot(-1)    # ZeroDivisionError: 0.0 cannot be raised to a negative power
calc.nroot(0, -1) # ZeroDivisionError: 0.0 cannot be raised to a negative power
calc.nroot(0, 1j) # ZeroDivisionError: 0.0 to a negative or complex power
```

Errors do not reset or overwrite memory.

## Limitations

The calculator is only as accurate as python itself. It will always return complex numbers for roots of negative numbers. 
It does not deal well with very small numbers (less than 0.001 absolute value), especially when they are added to roots, as it would try to return numbers which are bigger than maximum value allowed in python. 

## Installation

This module needs python 3.10 or higher to run
and hypothesis version 6.81.2

to install in terminal write:

pip install -i https://test.pypi.org/simple/ calculator-rasadangelaite


https://test.pypi.org/project/calculator-rasadangelaite/#description

