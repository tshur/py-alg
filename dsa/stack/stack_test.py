from .stack import Stack


class TestStack:
    def test_empty_stack(self) -> None:
        stack: Stack[int] = Stack()
        assert len(stack) == 0
        assert str(stack) == "[]"

    def test_from_iterable(self) -> None:
        stack = Stack.from_iterable([1, 2, 3])
        assert len(stack) == 3
        assert str(stack) == "[1, 2, 3]"

    def test_push(self) -> None:
        stack: Stack[int] = Stack()

        stack.push(1)
        assert len(stack) == 1
        assert str(stack) == "[1]"
        stack.push(2)
        assert len(stack) == 2
        assert str(stack) == "[1, 2]"
        stack.push(3)
        assert len(stack) == 3
        assert str(stack) == "[1, 2, 3]"

    def test_pop(self) -> None:
        stack = Stack.from_iterable([1, 2, 3])

        assert stack.pop() == 3
        assert stack.pop() == 2
        assert stack.pop() == 1
        assert stack.pop() is None
        assert stack.pop() is None

    def test_peek(self) -> None:
        stack = Stack.from_iterable([1, 2, 3])

        assert stack.peek() == 3
        assert stack.peek() == 3
        assert str(stack) == "[1, 2, 3]"

        stack2: Stack[int] = Stack()
        assert stack2.peek() is None

    def test_contains(self) -> None:
        stack = Stack.from_iterable([1, 2, 3])

        assert 1 in stack
        assert 2 in stack
        assert 3 in stack
        assert 4 not in stack
        assert 0 not in stack
