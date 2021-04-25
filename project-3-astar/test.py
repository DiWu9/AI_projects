"""Testing of 8 puzzle"""
from eightPuzzle import *
from informedSearch import *
from pq import *

def assert_state_equals(msg, expected, actual):
    """
    Check whether code being tested produces
    the correct result for a specific test
    case. Prints a message indicating whether
    it does.
    :param: msg is a message to print at the beginning.
    :param: expected is the correct result
    :param: actual is the result of the
    code under test.
    """
    print(msg)

    global num_pass, num_fail

    if expected.equals(actual):
        print("PASS")
        num_pass += 1
    else:
        print("**** FAIL")
        print("expected: " + str(expected))
        print("actual: " + str(actual))
        num_fail += 1

    print("")

def assert_equals(msg, expected, actual):
    """
    Check whether code being tested produces
    the correct result for a specific test
    case. Prints a message indicating whether
    it does.
    :param: msg is a message to print at the beginning.
    :param: expected is the correct result
    :param: actual is the result of the
    code under test.
    """
    print(msg)

    global num_pass, num_fail

    if expected == actual:
        print("PASS")
        num_pass += 1
    else:
        print("**** FAIL")
        print("expected: " + str(expected))
        print("actual: " + str(actual))
        num_fail += 1

    print("")

def start_tests(header):
    """
    Initializes summary statistics so we are ready to run tests using
    assert_equals.
    :param header: A header to print at the beginning
    of the tests.
    """
    global num_pass, num_fail, initialState1, initialState2
    print(header)
    for i in range(0,len(header)):
        print("=",end="")
    print("")
    num_pass = 0
    num_fail = 0
    initialState1 = EightPuzzle([1,2,3,4,None,5,6,7,8])
    initialState2 = EightPuzzle([None,1,2,3,4,8,7,6,5])

def finish_tests():
    """
    Prints summary statistics after the tests are complete.
    """
    print("Passed %d/%d" % (num_pass, num_pass+num_fail))
    print("Failed %d/%d" % (num_fail, num_pass+num_fail))

def test_moveRight():
    expected = EightPuzzle([1,2,3,4,5,None,6,7,8])
    assert_state_equals("Test operator: move right (normal case):", expected, initialState1.moveRight())
    initialState = EightPuzzle([1,2,None,3,4,8,7,6,5])
    expected = EightPuzzle([1,2,None,3,4,8,7,6,5])
    assert_state_equals("Test operator: move right (when space is at rightmost, " +
    "moveRight does not change anything)", expected, initialState.moveRight())
    original = EightPuzzle([1,2,3,4,None,5,6,7,8])
    expected = original.clone()
    original.moveRight()
    assert_state_equals("Test operator: move right does not change the original state", expected,
    original)
def test_moveLeft():
    expected = EightPuzzle([1,2,3,None,4,5,6,7,8])
    assert_state_equals("Test operator: move left (normal case):", expected, initialState1.moveLeft())
    expected = EightPuzzle([None,1,2,3,4,8,7,6,5])
    assert_state_equals("Test operator: move left (when space is at leftmost, " +
    "moveLeft is does not change anything)", expected, initialState2.moveLeft())
    original = EightPuzzle([1,2,3,4,None,5,6,7,8])
    expected = original.clone()
    original.moveLeft()
    assert_state_equals("Test operator: move left does not change the original state", expected,
    original)
def test_moveUp():
    expected = EightPuzzle([1,None,3,4,2,5,6,7,8])
    assert_state_equals("Test operator: move up (normal case):", expected, initialState1.moveUp())
    initialState = EightPuzzle([1,None,2,3,4,5,6,7,8])
    expected = EightPuzzle([1,None,2,3,4,5,6,7,8])
    assert_state_equals("Test operator: move up (when space is at the upmost, "+
    "moveUp does not change anything)", expected, initialState.moveUp())
    original = EightPuzzle([1,2,3,None,4,5,6,7,8])
    expected = original.clone()
    original.moveUp()
    assert_state_equals("Test operator: move up does not change the original state", expected,
    original)
def test_moveDown():
    expected = EightPuzzle([1,2,3,4,7,5,6,None,8])
    assert_state_equals("Test operator: move up (normal case):", expected, initialState1.moveDown())
    initialState = EightPuzzle([1,2,3,4,5,6,None,7,8])
    expected = EightPuzzle([1,2,3,4,5,6,None,7,8])
    assert_state_equals("Test operator: move down (when space is at the downmost, "+
    "moveDown does not change anything)", expected, initialState.moveDown())
    original = EightPuzzle([1,2,3,None,4,5,6,7,8])
    expected = original.clone()
    original.moveDown()
    assert_state_equals("Test operator: move down does not change the original state", expected,
    original)
def test_equals():
    expected = False
    assert_equals("Test equals() function:", expected, initialState1.equals(initialState2))
    expected = True
    assert_equals("Test equals() function:", expected, initialState1.equals(initialState1.clone()))
def test_heuristics():
    expected = 6
    initialState = EightPuzzle([1,2,3,7,8,5,4,6,None])
    finalState = EightPuzzle([1,2,3,4,5,6,7,8,None])
    assert_equals("Test heuristic: manhattan distance:", expected, initialState.heuristic(finalState))
    expected = 0
    assert_equals("Test heuristic: manhattan distance yields 0 when two states are equivalent:",
    expected, initialState.heuristic(initialState))


if __name__ == '__main__':
    start_tests("8 puzzle test begins: ")
    test_moveRight()
    test_moveLeft()
    test_moveUp()
    test_moveDown()
    test_equals()
    test_heuristics()
    finish_tests()
