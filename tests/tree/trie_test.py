import pytest
from dsap.tree import Trie


class TestTrie:
    def test_init(self) -> None:
        trie = Trie()

        assert trie.search("hello") is False
        assert trie.starts_with("hello") is False
        # insert app and search apple
        trie.insert("app")
        assert trie.search("app") is True
        # insert app and search app
        trie.insert("apple")
        assert trie.search("apple") is True
        # insert banana and search banana
        trie.insert("banana")
        assert trie.search("banana") is True
        # insert bandana and search bandana
        trie.insert("bandana")
        assert trie.search("bandana") is True

    def test_print(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test the print function of the trie."""
        trie = Trie()
        trie.insert("app")
        trie.insert("apple")
        trie.print()
        captured = capsys.readouterr()
        expected = (
            "Trie\n"
            "`-- a\n"
            "    `-- p\n"
            "        `-- p\n"
            "            |-- *\n"
            "            `-- l\n"
            "                `-- e\n"
            "                    `-- *\n"
        )
        assert captured.out == expected

    def test_search_prefix_not_word(self) -> None:
        """Test that searching for a prefix doesn't return True when only the longer word was inserted."""
        trie = Trie()

        # Insert "apple", then search for "app" - should be False
        trie.insert("apple")
        assert trie.search("app") is False  # This will currently fail because the trie has no end-of-word marker

        # Insert "car", then search for "c" - should be False
        trie.insert("car")
        assert trie.search("c") is False  # This will currently fail

        # Insert "hello", then search for "hell" - should be False
        trie.insert("hello")
        assert trie.search("hell") is False  # This will currently fail

    def test_search_complete_words_vs_prefixes(self) -> None:
        """Test various combinations of complete words and prefixes."""
        trie = Trie()

        # Insert both "app" and "apple"
        trie.insert("app")
        trie.insert("apple")

        # Both should be searchable as complete words
        assert trie.search("app") is True
        assert trie.search("apple") is True

        # But prefixes of complete words should not be searchable if not inserted
        trie2 = Trie()
        trie2.insert("apple")
        assert trie2.search("app") is False  # This will currently fail
        assert trie2.search("appl") is False  # This will currently fail
        assert trie2.search("a") is False  # This will currently fail

    def test_empty_string_insert(self) -> None:
        """Test that inserting an empty string raises a ValueError."""
        trie = Trie()
        with pytest.raises(ValueError):
            trie.insert("")

    def test_search_empty_string(self) -> None:
        """Test that searching for an empty string returns False."""
        trie = Trie()
        assert trie.search("") is False

    def test_starts_with_empty_string(self) -> None:
        """Test that starts_with for an empty string returns True."""
        trie = Trie()
        assert trie.starts_with("") is True

    def test_len(self) -> None:
        """Test that the length of the trie is correct."""
        trie = Trie()
        trie.insert("app")
        assert trie.search("app") is True
        # insert app and search app
        trie.insert("apple")
        assert trie.search("apple") is True
        # insert banana and search banana
        trie.insert("banana")
        assert trie.search("banana") is True
        # insert bandana and search bandana
        trie.insert("bandana")
        assert trie.search("bandana") is True
        assert len(trie) == 15

        trie = Trie()
        trie.insert("karma")
        trie.insert("karnataka")
        assert len(trie) == 11
        
    def test_insert_same_word_multiple_times(self) -> None:
        """Test that inserting the same word multiple times doesn't raise an error."""
        trie = Trie()
        trie.insert("apple")
        trie.insert("apple")
        trie.insert("apple")
        assert trie.search("apple") is True
        assert len(trie) == 5



