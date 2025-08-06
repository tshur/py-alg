from typing import Optional

from dsap.linked_list import SinglyLinkedList


class ReverseLinkedList(SinglyLinkedList[int]):
    def reverse_iterative(self):
        prev = None
        curr = self._head
        while curr:
            next = curr.next
            curr.next = prev

            prev, curr = curr, next

        self._head, self._tail = self._tail, self._head

    def reverse_recursive(self):
        def helper(
            head: Optional[SinglyLinkedList._Node[int]],
            tail: Optional[SinglyLinkedList._Node[int]],
        ) -> tuple[
            Optional[SinglyLinkedList._Node[int]],
            Optional[SinglyLinkedList._Node[int]],
        ]:
            if not head or not head.next:
                return head, tail

            new_head, _ = helper(head.next, tail)
            head.next.next = head
            head.next = None
            new_tail = head
            return new_head, new_tail

        self._head, self._tail = helper(self._head, self._tail)
