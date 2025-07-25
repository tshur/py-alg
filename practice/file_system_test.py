import pytest

from .file_system import FileSystem


class TestNextInSequence:
    # Note: We should be testing unit behaviors, not functions. However, grouping tests
    # for closer to 1:1 mapping with the implementation.
    def test_upload_file(self):
        file_system = FileSystem()

        with pytest.raises(ValueError, match="File name must be non-empty."):
            file_system.upload("", 100)
        with pytest.raises(ValueError, match="File size must be non-negative."):
            file_system.upload("file.txt", -100)

        file_system.upload("file.txt", 100)
        with pytest.raises(
            ValueError, match="A file with the same name already exists."
        ):
            file_system.upload("file.txt", 200)

    def test_get_file(self):
        file_system = FileSystem()

        assert file_system.get("file.txt") is None
        assert file_system.get("") is None

        file_system.upload("file.txt", 100)
        assert file_system.get("file.txt") == 100
        assert file_system.get("not_found.txt") is None

        assert file_system.get("") is None

    def test_copy_file(self):
        file_system = FileSystem()

        with pytest.raises(ValueError, match="Source file does not exist."):
            file_system.copy("source.txt", "dest.txt")

        # Copy files and copy copies.
        file_system.upload("source.txt", 100)
        file_system.copy("source.txt", "dest.txt")
        file_system.copy("dest.txt", "third.txt")
        assert file_system.get("dest.txt") == 100
        assert file_system.get("third.txt") == 100

        # Should support self-copy.
        file_system.copy("source.txt", "source.txt")
        assert file_system.get("source.txt") == 100

        # Copy will overwrite.
        file_system.upload("file.txt", 200)
        file_system.copy("source.txt", "file.txt")
        assert file_system.get("file.txt") == 100
