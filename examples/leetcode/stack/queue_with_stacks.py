from typing import Iterable, Self

from dsap.stack import Stack


class QueueWithStacks:
    """CTCI implementation of a queue using two stacks.

    Primary operations:
     - add (to back) in O(1)
     - remove (from front)
     - peek (from front)
     - is_empty in O(1)
    """

    _in_stack: Stack[int]
    _out_stack: Stack[int]

    def __init__(self) -> None:
        self._in_stack = Stack()
        self._out_stack = Stack()

    @classmethod
    def from_iterable(cls, iterable: Iterable[int]) -> Self:
        queue = cls()
        for value in iterable:
            queue.enqueue(value)
        return queue

    def enqueue(self, value: int) -> None:
        """Add value to the back of the queue.

        Implementation details:
            in_stack = [1, 2, 3, 4] <-- add here
            out_stack = [] --> pop from here

            We can always add new elements to the in_stack.
        """
        self._in_stack.push(value)

    def dequeue(self) -> int:
        """Remove (and return) value from the front of the queue.

        Implementation details:
            Maintain an in_stack and out_stack. When removing, if there are any elements
            in the out_stack, just remove/peek from there.
              in_stack = [3, 4]  <-- new added elements, can be removed after out_stack.
              out_stack = [2, 1]  --> remove/peek from here, if there are elements

            If the out_stack ever becomes empty, we need to take elements from the
            in_stack. Since these were added in stack order, we need to reverse them, by
            transferring to the out_stack.
              in_stack = [3, 4]
              out_stack = []
            becomes
              in_stack = []
              out_stack = [4, 3]  --> remove/peek from here
        """
        if not self._out_stack:
            self._transfer_stacks()

        value = self._out_stack.pop()
        if value is None:
            raise IndexError("remove called on empty queue")
        return value

    def peek(self) -> int:
        if not self._out_stack:
            self._transfer_stacks()

        value = self._out_stack.peek()
        if value is None:
            raise IndexError("peek called on empty queue")
        return value

    def is_empty(self) -> bool:
        return len(self) == 0

    def _transfer_stacks(self) -> None:
        """Transfer elements from in_stack to out_stack.

        Should never be called with elements in the out_stack. The purpose of this
        transfer is to invert the in_stack to subsequently peek/pop elements from the
        out_stack in reverse order. See implementation details in
        `QueueWithStacks.dequeue`.

        Examples:
            >>> stack = QueueWithStacks.from_iterable([1, 2, 3])
            >>> stack._transfer_stacks()
            >>> print(stack._out_stack)
            [3, 2, 1]
        """
        while self._in_stack:
            element = self._in_stack.pop()

            # This if statement is redundant since the popped element should always
            # exist here. Kept to avoid a type checker warning.
            if element is not None:
                self._out_stack.push(element)

    def __len__(self) -> int:
        return len(self._in_stack) + len(self._out_stack)
