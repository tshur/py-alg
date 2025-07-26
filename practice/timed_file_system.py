from dataclasses import dataclass
from typing import Optional


@dataclass
class File:
    name: str
    size: int
    created_timestamp: int
    ttl: Optional[int] = None


class TimedFileSystem:
    _files: dict[str, File]

    def __init__(self):
        self._files = {}

    def upload_at(
        self, timestamp: int, file_name: str, file_size: int, ttl: Optional[int] = None
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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError
