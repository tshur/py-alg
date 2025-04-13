from typing import Iterable, Optional


class Stack[T]:
    """LIFO stack implementation using built-in list buffer.

    Basic operations:
      - push, O(1)
      - pop, O(1)
      - peek, O(1)
    """

    _buffer: list[T]
    _size: int

    def __init__(self):
        self._buffer = []
        self._size = 0

    @classmethod
    def from_iterable[U](cls, iterable: Iterable[U]) -> "Stack[U]":
        """Create a new stack from an iterable of values.

        Args:
            iterable (Iterable[U]): An iterable of values to add into the stack. The
              values will be pushed onto the stack in the order that they are given.

        Returns:
            Stack[U]: The newly constructed stack.

        Examples:
            >>> stack = Stack.from_iterable([1, 2, 3])
            >>> print(stack)
            [1, 2, 3]
        """
        stack: Stack[U] = Stack()
        for value in iterable:
            stack.push(value)
        return stack

    def push(self, value: T) -> None:
        """Push a value onto the top of the stack.

        Args:
            value (T): The value to be pushed.

        Examples:
            >>> stack = Stack()
            >>> stack.push(1)
            >>> print(stack)
            [1]
            >>> stack.push(2)
            >>> print(stack)
            [1, 2]
        """
        self._buffer.append(value)
        self._size += 1

    def pop(self) -> Optional[T]:
        """Pop a value (remove and return) off of the top of the stack.

        Returns:
            Optional[T]: The removed value. If the stack is empty, returns None.

        Examples:
            >>> stack = Stack.from_iterable([1, 2])
            >>> stack.pop()
            2
            >>> stack.pop()
            1
            >>> stack.pop()
        """
        if len(self) == 0:
            return None
        self._size -= 1
        return self._buffer.pop()

    def peek(self) -> Optional[T]:
        """Return the top value of the stack without modifying the stack.

        Returns:
            Optional[T]: The value at the top of the stack. If the stack is empty,
              return None.

        Examples:
            >>> stack = Stack.from_iterable([1, 2, 3])
            >>> stack.peek()
            3
            >>> stack = Stack()
            >>> stack.peek()
        """
        if len(self) == 0:
            return None
        return self._buffer[-1]

    def __contains__(self, value: T) -> bool:
        """Check whether a value is contained in the stack.

        Checks values one at a time in O(n) time.

        Args:
            value (T): The value to search for in the stack.

        Returns:
            bool: Whether or not the value appears in the stack.

        Examples:
            >>> stack = Stack.from_iterable([1, 2, 3])
            >>> 1 in stack
            True
            >>> 10 in stack
            False
        """
        return value in self._buffer

    def __len__(self) -> int:
        """Return the length of the stack (stored, O(1) time).

        Returns:
            int: The number of elements in the stack.

        Examples:
            >>> stack = Stack.from_iterable([1, 2, 3])
            >>> len(stack)
            3
        """
        return self._size

    def __str__(self) -> str:
        """Return a printable representation of the stack.

        Returns:
            str: A string view of the stack. This is formatted like a list. The top of
              the stack is at the right end of the printed sequence.

        Examples:
            >>> str(Stack.from_iterable([1, 2, 3]))
            '[1, 2, 3]'
            >>> str(Stack())
            '[]'
        """
        return str(self._buffer)
