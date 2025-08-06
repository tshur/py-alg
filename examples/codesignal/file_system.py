from dataclasses import dataclass
from typing import Optional

from dsap.hash import Map
from dsap.heap import MinHeap


@dataclass
class File:
    name: str
    size: int


class FileSystem:
    _files: Map[str, File]

    def __init__(self):
        self._files = Map()

    def upload(self, file_name: str, size: int) -> None:
        """Uploads the file to the remove storage server.

        Args:
            file_name (str): The file name to upload.
            size (int): The size (in bytes) of the uploaded file.

        Raises:
            ValueError: If the given file_name is empty, or the size is negative.
            ValueError: If a file with the same name already exists on the server.
        """
        if not file_name:
            raise ValueError("File name must be non-empty.")
        if size < 0:
            raise ValueError("File size must be non-negative.")
        if file_name in self._files:
            raise ValueError("A file with the same name already exists.")

        self._files[file_name] = File(file_name, size)

    def get(self, file_name: str) -> Optional[int]:
        """Returns the size of the file, or nothing if the file doesn't exist.

        Args:
            file_name (str): The file name to retrieve.

        Returns:
            Optional[int]: The size of the file. If the file is not found, returns None.
        """
        if file_name in self._files:
            return self._files[file_name].size
        return None

    def copy(self, source: str, dest: str) -> None:
        """Copies the source file to a new location on the server.

        After the copy, both the source and dest filenames will exist and hold the same
        information (overwriting if dest already exists).

        Args:
            source (str): The source file to be copied.
            dest (str): The destination file name to copy the source file into. If the
              destination file already exists, it will be overwritten.

        Raises:
            ValueError: If the source file doesn't exist.
        """
        if source not in self._files:
            raise ValueError("Source file does not exist.")
        self._files[dest] = self._files[source]

    def search(self, prefix: str) -> list[str]:
        """Return the top 10 files whose name starts with the provided prefix.

        Results will be ordered by size in decreasing order. In case of ties, file names
        will be sorted by file name (ascending).

        Complexity:
            - Time: O(n * k),
              n: number of files stored; k: length of the prefix

        Optimizations:
            - Can store the file names in a Trie data structure. Store the actual file
              contents at the terminal node. This makes prefix-matching faster.
                - Before: O(n * k) where k is the length of the prefix
                - After: O(nlogk) (?)
            - Instead of sorting the whole set of matching files, we can use a heap data
              structure to loosely sort the data, then only retrieve the top-10.

        Args:
            prefix (str): The prefix string to search for.
        """
        # Find matched-prefix files in O(n * k) time.
        matched_files = list(self._files.values())
        if prefix:
            matched_files = [
                file for file in matched_files if file.name.startswith(prefix)
            ]

        # Heapify in O(n) time (on average, n may be smaller after filtering by prefix).
        # Re-structure so that min-heap returns files in expected order.
        file_heap = MinHeap[tuple[int, str]].from_iterable(
            (-file.size, file.name) for file in matched_files
        )
        return [file[1] for file in file_heap.consume_all()][:10]
