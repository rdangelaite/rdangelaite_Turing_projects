"""Calculator package"""

__version__ = "0.1.5"

from typing import Optional


class Calculator:

    """
    This is simple calculator with a memory.
    It can do addition, substraction, multiplication,
    division and find nth root of positive numbers.
    1 or 2 arguments can be entered: if 1 it will do
    calculations with number saved in memory.
    Memory can be reset or overwriden.
    """

    def __init__(self, memory: complex = 0) -> None:
        """
        Initializes attributes of calculator.
        The calculator has memory.
        Default memory value is 0.
        """

        self.memory = memory

    def add(self, argument1: complex, argument2: Optional[complex] = None) -> complex:
        """
        Takes number in the memory and adds provided argument to it:

            result = memory + argument

        If two arguments are provided, adds them together:

            result = argument1 + argument2

        Overwrites memory with the result and returns it.
        """

        if argument2:
            self.memory = argument1 + argument2
            return self.memory

        """If only one argument is provided:"""

        self.memory += argument1
        return self.memory

    def sub(self, argument1: complex, argument2: Optional[complex] = None) -> complex:
        """
        Takes number in the memory and subtracts provided argument from it.

            result = memory - argument

        If two arguments are provided, it subtracts second argument from
        first:

            result = argument1 - argument2

        Overwrites memory with the result and returns it.
        """

        if argument2:
            self.memory = argument1 - argument2
            return self.memory

        """If only one argument is provided:"""

        self.memory -= argument1
        return self.memory

    def mul(self, argument1: complex, argument2: Optional[complex] = None) -> complex:
        """
        Takes number in the memory and multiplies it by provided argument:

            result = memory * argument

        If two arguments are provided, it multiplies them:

            result = argument1 * argument2

        Overwrites memory with the result and returns it.
        """

        if argument2 or argument2 == 0:
            self.memory = argument1 * argument2
            return self.memory

        """If only one argument is provided:"""

        self.memory *= argument1
        return self.memory

    def div(
        self, argument1: complex, argument2: Optional[complex] = None
    ) -> Optional[complex]:
        """
        Takes number in the memory and divides it by provided argument:

            result = memory / argument

        If two arguments are provided, it divides first argument by the
        second one:

            result = argument1 / argument2

        Overwrites memory with the result and returns it.
        
        Does not divide by zero and returns error. Returning error does
        not overwrite memory.
        """

        if argument2 == 0:
            print("ZeroDivisionError: division by zero")
            return None

        if argument2:
            self.memory = argument1 / argument2
            return self.memory

        """If only one argument is provided:"""

        if argument1 == 0:
            print("ZeroDivisionError: division by zero")
            return None
        self.memory /= argument1
        return self.memory

    def nroot(
        self, argument1: complex, argument2: Optional[complex] = None
    ) -> Optional[complex]:
        """
        Takes number in the memory and nth roots it.
        Root level depends on provided argument

            result = memory ** 1 / argument

        If provided two arguments, takes root from first argument.
        Root depends on the second argument:

            result = argument1 ** 1 / argument2

        Or written in python:

            result = pow(memory, 1 / argument)
            result = pow(argument1, 1 / argument2)

        Overwrites memory with the result and returns it.


        Roots of negative numbers return complex numbers.

        Root level can be both positive and negative, but cannot be zero:

            pow(number, 0) -> returns error

        Cannot take negative or complex roots of 0:

            pow(0, negative or complex number) -> returns error

        Errors do not overwrite the memory
        """

        if argument2 == 0:
            print("ZeroDivisionError: division by zero: unable to make zeroth root")
            return None
        if argument2:
            if argument1 == 0 and isinstance(argument2, complex):
                print("ZeroDivisionError: 0.0 to a negative or complex power")
                return None
            elif argument1 == 0 and argument2 < 0:
                print("ZeroDivisionError: 0.0 cannot be raised to a negative power")
                return None
            self.memory = pow(argument1, 1 / argument2)
            return self.memory

        """If only one argument is provided:"""

        if argument1 == 0:
            print("ZeroDivisionError: division by zero: unable to make zeroth root")
            return None
        if self.memory == 0 and isinstance(argument2, complex):
            print("ZeroDivisionError: 0.0 to a negative or complex power")
            return None
        elif self.memory == 0 and argument1 < 0:
            print("ZeroDivisionError: 0.0 cannot be raised to a negative power")
            return None
        self.memory = pow(self.memory, 1 / argument1)
        return self.memory

    def reset(self) -> complex:
        """Resets memory to default value of 0."""

        self.memory = 0
        return self.memory

    def __call__(self, memory: Optional[complex] = None) -> complex:
        """
        Allows for the calculator to be called and
        can overwrite the memory if argument is provided.
        If no argument provided it prints what is stored in memory.
        """

        if memory or memory == 0:
            self.memory = memory
        return self.memory


if __name__ == "__main__":
    calculator = Calculator()
