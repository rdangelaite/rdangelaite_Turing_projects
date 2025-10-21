from hypothesis import settings, HealthCheck, given, assume, strategies as st
from calculator_rasadangelaite.calculator import Calculator


def test_calculator_assert():
    """
    Testing if all functions work as expected in connection with one
    another.
    """
    calculator = Calculator()
    assert calculator() == 0
    assert calculator.add(10) == 10
    assert calculator.sub(2) == 8
    assert calculator.mul(3) == 24
    assert calculator.div(3) == 8
    assert calculator.nroot(3) == 2
    assert calculator.reset() == 0
    assert calculator(5) == 5


def test_calculator_assert_two_arguments():
    """
    Testing if all two argument functions work as expected.
    """
    calculator = Calculator()
    assert calculator.add(10, 15.5) == 25.5
    assert calculator.sub(2, 9) == -7
    assert calculator.mul(3, 7) == 21
    assert calculator.div(3, 2) == 1.5
    assert calculator.nroot(4, 2) == 2


@given(
    memory=st.floats(),
    argument1=st.floats(),
    argument2=st.floats(),
)
@settings(
    suppress_health_check=[HealthCheck.filter_too_much, HealthCheck.too_slow],
    deadline=None,
)
def test_testing_using_hypothesis(memory, argument1, argument2):
    """
    Testing using hypothesis. First unit testing, then how operations work
    well with one another.
    """
    """
    Testing one argument functions with hypothesis separatelly from one
    another. Testing two argument functions to work.
    """
    assume(abs(memory) > 0.0001)
    assume(abs(argument1) > 0.0001)
    assume(abs(argument2) > 0.0001)

    calculator = Calculator()
    calculator(memory)
    calculator.add(argument1)
    calculator = Calculator(memory)
    calculator.sub(argument1)
    calculator = Calculator(memory)
    calculator.mul(argument1)
    calculator = Calculator(memory)
    calculator.div(argument1)
    calculator = Calculator(memory)
    calculator.nroot(argument1)

    calculator.add(argument1, argument2)
    calculator.sub(argument1, argument2)
    calculator.mul(argument1, argument2)
    calculator.div(argument1, argument2)
    calculator.nroot(argument1, argument2)

    """
    Testing how units work with one another
    """
    calculator(memory)
    calculator.add(argument1)
    calculator.sub(argument1)
    calculator.mul(argument1)
    calculator.div(argument1)
    calculator.nroot(argument1)


if __name__ == "__main__":
    test_calculator_assert()
    test_calculator_assert_two_arguments()
    test_testing_using_hypothesis()
