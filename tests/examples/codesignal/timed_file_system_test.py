import pytest

from examples.codesignal.timed_file_system import MaxSentinel, TimedFileSystem


class TestMaxSentinel:
    def test_always_greater_than_int(self):
        assert 10000 < MaxSentinel()
        assert 0 < MaxSentinel()
        assert MaxSentinel() > 10000
        assert not MaxSentinel() == 0
        assert not MaxSentinel() == -1

    def test_equal_to_other_max_sentinel(self):
        assert MaxSentinel() == MaxSentinel()
        assert not MaxSentinel() == 1000000

    def test_arithmetic_returns_max_sentinel(self):
        assert 0 + MaxSentinel() == MaxSentinel()
        assert MaxSentinel() + 1000 == MaxSentinel()
        assert MaxSentinel() - 1000000 == MaxSentinel()


class TestTimedFileSystem:
    def setup_method(self):
        self.file_system = TimedFileSystem()

    def test_upload_file_fails(self):
        with pytest.raises(ValueError, match="Timestamp must be non-negative."):
            self.file_system.upload_at(-10, "file.txt", 100)
        with pytest.raises(ValueError, match="File name must be non-empty."):
            self.file_system.upload_at(0, "", 100)
        with pytest.raises(ValueError, match="File size must be non-negative."):
            self.file_system.upload_at(0, "file.txt", -100)
        with pytest.raises(ValueError, match="File ttl must be positive or None."):
            self.file_system.upload_at(0, "file.txt", 100, -1)
        with pytest.raises(ValueError, match="File ttl must be positive or None."):
            self.file_system.upload_at(0, "file.txt", 100, 0)

        self.file_system.upload_at(0, "file.txt", 100)
        with pytest.raises(ValueError, match="File with the same name already exists."):
            self.file_system.upload_at(0, "file.txt", 200)

    def test_upload_file_succeeds(self):
        self.file_system.upload_at(0, "file.txt", 100)
        assert self.file_system.get_at(0, "file.txt") == 100
        assert self.file_system.get_at(1, "file.txt") == 100
        assert self.file_system.get_at(1000, "file.txt") == 100

    def test_get_file_fails(self):
        with pytest.raises(ValueError, match="Timestamp must be non-negative."):
            self.file_system.get_at(-10, "file.txt")

    def test_get_file_succeeds(self):
        assert self.file_system.get_at(0, "") is None
        assert self.file_system.get_at(10, "file.txt") is None

        self.file_system.upload_at(10, "file.txt", 100)
        assert self.file_system.get_at(0, "file.txt") is None
        assert self.file_system.get_at(9, "file.txt") is None
        assert self.file_system.get_at(0, "") is None

        assert self.file_system.get_at(10, "file.txt") == 100
        assert self.file_system.get_at(1000, "file.txt") == 100

    def test_upload_file_with_ttl(self):
        self.file_system.upload_at(10, "file.txt", 100, ttl=90)
        assert self.file_system.get_at(9, "file.txt") is None
        assert self.file_system.get_at(101, "file.txt") is None

        assert self.file_system.get_at(10, "file.txt") == 100
        assert self.file_system.get_at(99, "file.txt") == 100
        assert self.file_system.get_at(100, "file.txt") == 100  # Last second it exists.

        with pytest.raises(ValueError, match="File with the same name already exists."):
            self.file_system.upload_at(100, "file.txt", 100)  # Still exists
        assert self.file_system.get_at(101, "file.txt") is None

        self.file_system.upload_at(101, "file.txt", 200)
        assert self.file_system.get_at(100, "file.txt") == 100
        assert self.file_system.get_at(101, "file.txt") == 200
        assert self.file_system.get_at(1000, "file.txt") == 200

    def test_copy_file_fails(self):
        with pytest.raises(ValueError, match="Timestamp must be non-negative."):
            self.file_system.copy_at(-10, "source.txt", "dest.txt")
        with pytest.raises(ValueError, match="Source file does not exist."):
            self.file_system.copy_at(0, "source.txt", "dest.txt")
        with pytest.raises(ValueError, match="Source file does not exist."):
            self.file_system.copy_at(0, "source.txt", "source.txt")

        self.file_system.upload_at(10, "source.txt", 100, ttl=90)
        with pytest.raises(ValueError, match="Source file does not exist."):
            self.file_system.copy_at(101, "source.txt", "dest.txt")
        with pytest.raises(ValueError, match="Source file does not exist."):
            self.file_system.copy_at(101, "source.txt", "source.txt")

    def test_copy_file_succeeds(self):
        self.file_system.upload_at(10, "source.txt", 100)
        self.file_system.copy_at(20, "source.txt", "dest.txt")

        assert self.file_system.get_at(9, "source.txt") is None
        assert self.file_system.get_at(10, "source.txt") == 100
        assert self.file_system.get_at(19, "source.txt") == 100
        assert self.file_system.get_at(1000, "source.txt") == 100

        assert self.file_system.get_at(9, "dest.txt") is None
        assert self.file_system.get_at(19, "dest.txt") is None
        assert self.file_system.get_at(20, "dest.txt") == 100
        assert self.file_system.get_at(1000, "dest.txt") == 100

    def test_copy_file_overwrites(self):
        self.file_system.upload_at(10, "source.txt", 100)
        self.file_system.upload_at(10, "dest.txt", 999)
        self.file_system.copy_at(20, "source.txt", "dest.txt")

        assert self.file_system.get_at(9, "source.txt") is None
        assert self.file_system.get_at(10, "source.txt") == 100
        assert self.file_system.get_at(19, "source.txt") == 100
        assert self.file_system.get_at(1000, "source.txt") == 100

        assert self.file_system.get_at(9, "dest.txt") is None
        assert self.file_system.get_at(10, "dest.txt") == 999
        assert self.file_system.get_at(19, "dest.txt") == 999
        assert self.file_system.get_at(20, "dest.txt") == 100
        assert self.file_system.get_at(1000, "dest.txt") == 100

    def test_self_copy_file_has_no_effect(self):
        self.file_system.upload_at(10, "source.txt", 100)
        self.file_system.copy_at(20, "source.txt", "source.txt")

        assert self.file_system.get_at(9, "source.txt") is None
        assert self.file_system.get_at(10, "source.txt") == 100
        assert self.file_system.get_at(19, "source.txt") == 100
        assert self.file_system.get_at(1000, "source.txt") == 100

    def test_copy_file_with_ttl(self):
        self.file_system.upload_at(10, "source.txt", 100, ttl=90)
        self.file_system.upload_at(10, "dest.txt", 999)
        self.file_system.copy_at(50, "source.txt", "dest.txt")

        assert self.file_system.get_at(9, "source.txt") is None
        assert self.file_system.get_at(10, "source.txt") == 100
        assert self.file_system.get_at(49, "source.txt") == 100
        assert self.file_system.get_at(50, "source.txt") == 100
        assert self.file_system.get_at(100, "source.txt") == 100
        assert self.file_system.get_at(101, "source.txt") is None

        assert self.file_system.get_at(9, "dest.txt") is None
        assert self.file_system.get_at(10, "dest.txt") == 999
        assert self.file_system.get_at(49, "dest.txt") == 999
        assert self.file_system.get_at(50, "dest.txt") == 100
        assert self.file_system.get_at(100, "dest.txt") == 100
        assert self.file_system.get_at(101, "dest.txt") is None  # Preserves TTL.

    def test_copy_overwrites_file_with_ttl(self):
        self.file_system.upload_at(10, "source.txt", 100, ttl=90)
        self.file_system.upload_at(10, "dest.txt", 999, ttl=1000)
        # Overwrites the very long ttl in dest after copying.
        self.file_system.copy_at(50, "source.txt", "dest.txt")

        assert self.file_system.get_at(9, "source.txt") is None
        assert self.file_system.get_at(10, "source.txt") == 100
        assert self.file_system.get_at(49, "source.txt") == 100
        assert self.file_system.get_at(50, "source.txt") == 100
        assert self.file_system.get_at(100, "source.txt") == 100
        assert self.file_system.get_at(101, "source.txt") is None

        assert self.file_system.get_at(9, "dest.txt") is None
        assert self.file_system.get_at(10, "dest.txt") == 999
        assert self.file_system.get_at(49, "dest.txt") == 999
        assert self.file_system.get_at(50, "dest.txt") == 100
        assert self.file_system.get_at(100, "dest.txt") == 100
        assert self.file_system.get_at(101, "dest.txt") is None  # Preserves TTL.

    def test_search_fails(self):
        with pytest.raises(ValueError, match="Timestamp must be non-negative."):
            self.file_system.search_at(-10, "prefix")

    def test_search_succeeds(self):
        self.file_system.upload_at(1, "a.txt", 100)
        self.file_system.upload_at(2, "b.txt", 500)
        self.file_system.upload_at(3, "c.txt", 400)
        self.file_system.upload_at(4, "d.txt", 200)
        self.file_system.upload_at(5, "e.txt", 300)
        assert self.file_system.search_at(5, "") == [
            "b.txt",
            "c.txt",
            "e.txt",
            "d.txt",
            "a.txt",
        ]

        assert self.file_system.search_at(0, "") == []

        self.file_system.upload_at(5, "f.txt", 300)
        self.file_system.upload_at(6, "g.txt", 300)
        self.file_system.upload_at(7, "h.txt", 300)
        self.file_system.upload_at(8, "i.txt", 300)
        self.file_system.upload_at(9, "j.txt", 300)
        self.file_system.upload_at(10, "k.txt", 300)
        self.file_system.upload_at(11, "l.txt", 300)
        assert self.file_system.search_at(12, "") == [
            "b.txt",
            "c.txt",
            "e.txt",
            "f.txt",
            "g.txt",
            "h.txt",
            "i.txt",
            "j.txt",
            "k.txt",
            "l.txt",
        ]

        self.file_system.upload_at(10, "ab.txt", 500)
        self.file_system.upload_at(10, "ac.txt", 300)
        self.file_system.upload_at(10, "ad.txt", 400)
        self.file_system.upload_at(10, "ae.txt", 200)
        assert self.file_system.search_at(9, "a") == ["a.txt"]
        assert self.file_system.search_at(10, "a") == [
            "ab.txt",
            "ad.txt",
            "ac.txt",
            "ae.txt",
            "a.txt",
        ]

    def test_search_with_ttl(self):
        self.file_system.upload_at(1, "a.txt", 100)
        self.file_system.upload_at(2, "dir/a.txt", 100)
        self.file_system.upload_at(3, "dir/b.txt", 100)
        self.file_system.upload_at(4, "dir/c.txt", 100, ttl=96)
        self.file_system.upload_at(5, "dir/d.txt", 100, ttl=95)
        self.file_system.upload_at(6, "dir/e.txt", 100, ttl=150)
        assert self.file_system.search_at(10, "a") == ["a.txt"]
        assert self.file_system.search_at(3, "dir/") == [
            "dir/a.txt",
            "dir/b.txt",
        ]
        assert self.file_system.search_at(10, "dir/") == [
            "dir/a.txt",
            "dir/b.txt",
            "dir/c.txt",
            "dir/d.txt",
            "dir/e.txt",
        ]

        assert self.file_system.search_at(100, "dir/") == [
            "dir/a.txt",
            "dir/b.txt",
            "dir/c.txt",
            "dir/d.txt",
            "dir/e.txt",
        ]
        assert self.file_system.search_at(101, "dir/") == [
            "dir/a.txt",
            "dir/b.txt",
            "dir/e.txt",
        ]
        assert self.file_system.search_at(1000, "dir/") == [
            "dir/a.txt",
            "dir/b.txt",
        ]

    def test_search_with_copied_files(self):
        self.file_system.upload_at(1, "a.txt", 100)
        self.file_system.upload_at(2, "dir/a.txt", 100)
        self.file_system.upload_at(3, "dir/b.txt", 100)
        self.file_system.upload_at(4, "dir/c.txt", 100, ttl=96)
        self.file_system.copy_at(5, "dir/c.txt", "dir/d.txt")
        self.file_system.copy_at(6, "dir/a.txt", "dir/e.txt")
        assert self.file_system.search_at(10, "a") == ["a.txt"]
        assert self.file_system.search_at(3, "dir/") == [
            "dir/a.txt",
            "dir/b.txt",
        ]
        assert self.file_system.search_at(10, "dir/") == [
            "dir/a.txt",
            "dir/b.txt",
            "dir/c.txt",
            "dir/d.txt",
            "dir/e.txt",
        ]

        assert self.file_system.search_at(100, "dir/") == [
            "dir/a.txt",
            "dir/b.txt",
            "dir/c.txt",
            "dir/d.txt",
            "dir/e.txt",
        ]
        assert self.file_system.search_at(101, "dir/") == [
            "dir/a.txt",
            "dir/b.txt",
            "dir/e.txt",
        ]

    def test_rollback_fails(self):
        with pytest.raises(ValueError, match="Timestamp must be non-negative."):
            self.file_system.rollback(-1)

    def test_rollbacks_with_no_effect(self):
        self.file_system.upload_at(1, "a.txt", 100)
        self.file_system.upload_at(2, "dir/a.txt", 100)
        self.file_system.upload_at(3, "dir/b.txt", 100)
        self.file_system.upload_at(4, "dir/c.txt", 100, ttl=96)
        self.file_system.copy_at(5, "dir/c.txt", "dir/d.txt")
        self.file_system.copy_at(6, "dir/a.txt", "dir/e.txt")

        assert self.file_system.search_at(100, "dir/") == [
            "dir/a.txt",
            "dir/b.txt",
            "dir/c.txt",
            "dir/d.txt",
            "dir/e.txt",
        ]
        assert self.file_system.search_at(101, "dir/") == [
            "dir/a.txt",
            "dir/b.txt",
            "dir/e.txt",
        ]

        self.file_system.rollback(1000)  # In the future.
        assert self.file_system.search_at(100, "dir/") == [
            "dir/a.txt",
            "dir/b.txt",
            "dir/c.txt",
            "dir/d.txt",
            "dir/e.txt",
        ]
        assert self.file_system.search_at(101, "dir/") == [
            "dir/a.txt",
            "dir/b.txt",
            "dir/e.txt",
        ]

        self.file_system.rollback(6)  # All operations still have occurred.
        assert self.file_system.search_at(100, "dir/") == [
            "dir/a.txt",
            "dir/b.txt",
            "dir/c.txt",
            "dir/d.txt",
            "dir/e.txt",
        ]
        assert self.file_system.search_at(101, "dir/") == [
            "dir/a.txt",
            "dir/b.txt",
            "dir/e.txt",
        ]

    def test_rollbacks_with_effects(self):
        self.file_system.upload_at(1, "a.txt", 100)
        self.file_system.upload_at(2, "dir/a.txt", 100)
        self.file_system.upload_at(3, "dir/b.txt", 100)
        self.file_system.upload_at(4, "dir/c.txt", 100, ttl=96)
        self.file_system.copy_at(5, "dir/c.txt", "dir/d.txt")
        self.file_system.copy_at(6, "dir/a.txt", "dir/e.txt")

        assert self.file_system.search_at(100, "dir/") == [
            "dir/a.txt",
            "dir/b.txt",
            "dir/c.txt",
            "dir/d.txt",
            "dir/e.txt",
        ]
        assert self.file_system.search_at(101, "dir/") == [
            "dir/a.txt",
            "dir/b.txt",
            "dir/e.txt",
        ]

        self.file_system.rollback(5)  # Removes the copy-creation of e.txt.
        assert self.file_system.search_at(100, "dir/") == [
            "dir/a.txt",
            "dir/b.txt",
            "dir/c.txt",
            "dir/d.txt",
        ]
        assert self.file_system.search_at(101, "dir/") == [
            "dir/a.txt",
            "dir/b.txt",
        ]

        self.file_system.rollback(4)  # Removes the copy-creation of d.txt.
        assert self.file_system.search_at(100, "dir/") == [
            "dir/a.txt",
            "dir/b.txt",
            "dir/c.txt",
        ]
        assert self.file_system.search_at(101, "dir/") == [
            "dir/a.txt",
            "dir/b.txt",
        ]

        self.file_system.rollback(3)  # Removes the creation of c.txt.
        assert self.file_system.search_at(100, "dir/") == [
            "dir/a.txt",
            "dir/b.txt",
        ]
        assert self.file_system.search_at(101, "dir/") == [
            "dir/a.txt",
            "dir/b.txt",
        ]

        self.file_system.rollback(2)  # Removes the creation of b.txt.
        assert self.file_system.search_at(100, "dir/") == [
            "dir/a.txt",
        ]
        assert self.file_system.search_at(101, "dir/") == [
            "dir/a.txt",
        ]

        self.file_system.rollback(0)  # No data existed at this point.
        assert self.file_system.search_at(100, "dir/") == []
        assert self.file_system.search_at(101, "dir/") == []

    def test_rollbacks_on_copy_overwritten_ttl(self):
        self.file_system.upload_at(10, "source.txt", 100, ttl=90)
        self.file_system.upload_at(10, "dest.txt", 200, ttl=1000)
        self.file_system.copy_at(50, "source.txt", "dest.txt")

        assert self.file_system.get_at(9, "source.txt") is None
        assert self.file_system.get_at(10, "source.txt") == 100
        assert self.file_system.get_at(100, "source.txt") == 100
        assert self.file_system.get_at(101, "source.txt") is None

        assert self.file_system.get_at(9, "dest.txt") is None
        assert self.file_system.get_at(10, "dest.txt") == 200
        assert self.file_system.get_at(49, "dest.txt") == 200
        assert self.file_system.get_at(50, "dest.txt") == 100
        assert self.file_system.get_at(100, "dest.txt") == 100
        assert self.file_system.get_at(101, "dest.txt") is None  # ttl=90 preserved.

        self.file_system.rollback(49)  # Remove the copy-overwrite operation!
        assert self.file_system.get_at(9, "source.txt") is None
        assert self.file_system.get_at(10, "source.txt") == 100
        assert self.file_system.get_at(100, "source.txt") == 100
        assert self.file_system.get_at(101, "source.txt") is None

        assert self.file_system.get_at(9, "dest.txt") is None
        assert self.file_system.get_at(10, "dest.txt") == 200
        assert self.file_system.get_at(49, "dest.txt") == 200
        assert self.file_system.get_at(50, "dest.txt") == 200
        assert self.file_system.get_at(100, "dest.txt") == 200
        assert self.file_system.get_at(101, "dest.txt") == 200  # Original ttl=1000.
        assert self.file_system.get_at(1010, "dest.txt") == 200
        assert self.file_system.get_at(1011, "dest.txt") is None
