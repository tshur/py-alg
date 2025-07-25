from typing import Optional


class FileSystem:
    _files: dict[str, int]

    def __init__(self):
        self._files = {}

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

        self._files[file_name] = size

    def get(self, file_name: str) -> Optional[int]:
        """Returns the size of the file, or nothing if the file doesn't exist.

        Args:
            file_name (str): The file name to retrieve.

        Returns:
            Optional[int]: The size of the file. If the file is not found, returns None.
        """
        return self._files.get(file_name)

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
