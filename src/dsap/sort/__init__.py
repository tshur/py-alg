from .bubble_sort import bubble_sort
from .heap_sort import heap_sort
from .insertion_sort import insertion_sort
from .merge_sort import merge_sort
from .quick_sort import quick_sort
from .selection_sort import selection_sort
from .tree_sort import tree_sort
from .tim_sort import tim_sort

sort = merge_sort

__all__ = [
    "bubble_sort",
    "heap_sort",
    "insertion_sort",
    "merge_sort",
    "quick_sort",
    "selection_sort",
    "sort",
    "tree_sort",
    "tim_sort",
]
