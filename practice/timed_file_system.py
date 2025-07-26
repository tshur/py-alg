from __future__ import annotations

import bisect
import functools
import heapq
import operator
from dataclasses import dataclass
from typing import Optional


# Create a type sentinel that always compares larger than any other integer.
@functools.total_ordering
class MaxSentinel:
    def __le__(self, other: int) -> bool:
        return False

    def __add__(self, other: int | MaxSentinel) -> MaxSentinel:
        return self

    def __radd__(self, other: int | MaxSentinel) -> MaxSentinel:
        return self

    def __sub__(self, other: int | MaxSentinel) -> MaxSentinel:
        return self

    def __rsub__(self, other: int | MaxSentinel) -> MaxSentinel:
        return self


@dataclass
class File:
    name: str
    size: int
    created_timestamp: int
    ttl: int | MaxSentinel = MaxSentinel()

    def get_last_valid_timestamp(self) -> int | MaxSentinel:
        return self.created_timestamp + self.ttl


class TimedFileSystem:
    # For each filename, store the resulting files in a sorted (ascending by timestamp)
    # list. This ensures that we can handle ttls, file existence, rollbacks, and queries
    # at specific timestamps.
    _files: dict[str, list[File]]

    def __init__(self):
        self._files = {}

    def upload_at(
        self,
        timestamp: int,
        file_name: str,
        file_size: int,
        ttl: int | MaxSentinel = MaxSentinel(),
    ) -> None:
        """Uploads the file to the remove storage server with a given ttl.

        The file is (attempted to be) uploaded at the given timestamp. The file will
        live for a maximum of ttl seconds.

        Args:
            timestamp (int): The timestamp (in seconds) to perform the operation.
            file_name (str): The file name to upload.
            size (int): The size (in bytes) of the uploaded file.
            ttl (Optional[int]): The number of seconds the file should remain for. After
              the time passes, the file will be treated as though it does not exist.
              Default is None, representing an infinite lifetime.

        Raises:
            ValueError: If the timestamp is negative.
            ValueError: If the given file_name is empty
            ValueError: If the given file_size is negative.
            ValueError: If a file with the same name already exists on the server.
            ValueError: If the ttl is non-positive (0 ttl files cannot be created).
        """
        if timestamp < 0:
            raise ValueError("File timestamp must be non-negative.")
        if not file_name:
            raise ValueError("File name must be non-empty.")
        if file_size < 0:
            raise ValueError("File size must be non-negative.")
        if ttl <= 0:
            raise ValueError("File ttl must be positive or None.")
        if self._retrieve_file(timestamp, file_name):
            raise ValueError("File with the same name already exists.")

        self._insert_file(File(file_name, file_size, timestamp, ttl))

    def get_at(self, timestamp: int, file_name: str) -> Optional[int]:
        """Returns the size of the file, or nothing if the file doesn't exist.

        Only files active at the given timestamp can be retrieved.

        Args:
            timestamp (int): The timestamp (in seconds) to perform the operation.
            file_name (str): The file name to retrieve.

        Returns:
            Optional[int]: The size of the file. If the file is not found, returns None.

        Raises:
            ValueError: If the timestamp is negative.
        """
        if timestamp < 0:
            raise ValueError("File timestamp must be non-negative.")

        file = self._retrieve_file(timestamp, file_name)
        if file:
            return file.size
        return None

    def copy_at(self, timestamp: int, source: str, dest: str) -> None:
        """Copies the source file to a new location on the server.

        After the copy, both the source and dest filenames will exist and hold the same
        information (overwriting if dest already exists). The files will still expire at
        the same time they would have before the copy.

        Args:
            timestamp (int): The timestamp (in seconds) to perform the operation.
            source (str): The source file to be copied.
            dest (str): The destination file name to copy the source file into. If the
              destination file already exists, it will be overwritten.

        Raises:
            ValueError: If the timestamp is negative.
            ValueError: If the source file doesn't exist.
        """
        if timestamp < 0:
            raise ValueError("File timestamp must be non-negative.")

        source_file = self._retrieve_file(timestamp, source)
        if not source_file:
            raise ValueError("Source file does not exist.")
        if source == dest:
            return  # Self-copy has no effect.

        # Treat the copy as though a new file (with shorter ttl) is being created now.
        self._insert_file(
            File(
                dest,
                source_file.size,
                timestamp,
                # Update the new TTL to be: source.ttl - (duration elapsed).
                source_file.ttl - (timestamp - source_file.created_timestamp),
            )
        )

    def search_at(self, timestamp: int, prefix: str) -> list[str]:
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
            timestamp (int): The timestamp (in seconds) to perform the operation.
            prefix (str): The prefix string to search for.

        Returns:
            Optional[int]: A list of filenames matching the given prefix.

        Raises:
            ValueError: If the timestamp is negative.
        """
        if timestamp < 0:
            raise ValueError("File timestamp must be non-negative.")

        # Filter active files by (optional) prefix.
        files = self._get_active_files(timestamp)
        if prefix:
            files = [file for file in files if file.name.startswith(prefix)]

        # Heapify in O(n) time (on average, n may be smaller after filtering by prefix).
        # Re-structure so that min-heap returns files in expected order.
        file_heap = [(-file.size, file.name) for file in files]
        heapq.heapify(file_heap)

        # Return the top-10 results from the heap in O(logn) time. Can we do better by
        # restricting the size of the heap to max 10 elements? Yes. Then, heapify will
        # take O(n * log10) time, and popping the top-10 take constant time.
        result: list[str] = []
        for _ in range(10):
            if not file_heap:
                break
            next_file = heapq.heappop(file_heap)
            result.append(next_file[1])  # Note: filename was moved to second index.
        return result

    def _insert_file(self, file: File) -> None:
        """Inserts the given file while maintaining sorted ordering.

        This assumes that the file is valid and should be inserted into storage. The
        File will be inserted according to its file.name and maintained sorted according
        to its file.created_timestamp. There should not already exist a valid file with
        the same name.

        Args:
            file (File): The file to be inserted into storage.
        """
        if file.name not in self._files:
            self._files[file.name] = []

        # We insort_right so that ties on created_timestamp go to the operation that
        # occurred second (e.g., for copying).
        bisect.insort(
            self._files[file.name], file, key=operator.attrgetter("created_timestamp")
        )

    def _retrieve_file(self, timestamp: int, file_name: str) -> Optional[File]:
        """Retrieves the active file with given file_name from storage.

        A file is considered active, if it is still available (non-expired) at the given
        timestamp. If no file with the given name is active, returns None.

        Returns:
            Optional[File]: An active, valid File at the timestamp with the given name.
              Returns None if no file with the given name is active or exists.

        Raises:
            ValueError: If the timestamp is negative.
        """
        if timestamp < 0:
            raise ValueError("File timestamp must be non-negative.")
        if file_name not in self._files or not self._files[file_name]:
            return None

        # We bisect_right by timestamp to handle cases of overwriting files with the
        # same timestamp (via copy). However, bisect_right gets us one index after the
        # target, so we need to check the previous index (note the -1).
        files = self._files[file_name]
        index = (
            bisect.bisect(
                files, timestamp, key=operator.attrgetter("created_timestamp")
            )
            - 1
        )
        if index < 0:
            return None

        target_file = files[index]
        if (
            target_file.created_timestamp
            <= timestamp
            <= target_file.get_last_valid_timestamp()
        ):
            return target_file
        return None

    def _get_active_files(self, timestamp: int) -> list[File]:
        """Retrieves all active files in storage at the given timestamp..

        A file is considered active, if it is still available (non-expired) at the given
        timestamp. If no file with the given name is active, returns None.

        Args:
            timestamp (int): The timestamp at which to perform the query.

        Returns:
            list[File]: A list of active, valid files in storage.

        Raises:
            ValueError: If the timestamp is negative.
        """
        if timestamp < 0:
            raise ValueError("File timestamp must be non-negative.")

        return [
            file
            for file_name in self._files
            if (file := self._retrieve_file(timestamp, file_name)) is not None
        ]
