import pytest
from dsap.tree import Trie


class TestTrie:
    def test_init(self, capsys: pytest.CaptureFixture[str]) -> None:
        trie = Trie()

        assert len(trie) == 0
        assert trie._trie.val == ""
        assert trie._trie.children == {}
        assert trie.search("dharma") is False
        assert trie.starts_with("dharma") is False

        trie.print()
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_insert(self) -> None:
        """Test the insert function of the trie with creative Sanskrit words."""
        trie = Trie()

        # Basic insertion
        trie.insert("dharma")
        assert trie.search("dharma") is True
        assert len(trie) == 6

        # Insertion with shared prefix
        trie.insert("dharmasala")
        assert trie.search("dharmasala") is True
        assert len(trie) == 10  # d-h-a-r-m-a (6) + s-a-l-a (4)

        # Another branch
        trie.insert("karma")
        assert trie.search("karma") is True
        assert len(trie) == 15  # 10 + 5

        # Same word multiple times
        trie.insert("karma")
        assert len(trie) == 15
        assert trie.search("karma") is True

        # Empty string should raise ValueError
        with pytest.raises(ValueError):
            trie.insert("")

    def test_search(self) -> None:
        """Test the search function of the trie with various combinations."""
        trie = Trie()

        # Search for words not in trie
        assert trie.search("shanti") is False

        # Insert words and search
        trie.insert("namaste")
        trie.insert("namaskar")
        assert trie.search("namaste") is True
        assert trie.search("namaskar") is True

        # Search for prefixes that are not complete words
        assert trie.search("nama") is False
        assert trie.search("namas") is False

        # Search for empty string
        assert trie.search("") is False

        # Search for word that is a prefix of another word
        trie.insert("guru")
        trie.insert("gurudeva")
        assert trie.search("guru") is True
        assert trie.search("gurudeva") is True
        assert trie.search("gurudev") is False

    def test_starts_with(self) -> None:
        """Test the starts_with function of the trie."""
        trie = Trie()

        # Starts with on empty trie
        assert trie.starts_with("yoga") is False

        # Insert and test starts_with
        trie.insert("nirvana")
        assert trie.starts_with("nir") is True
        assert trie.starts_with("nirvana") is True
        assert trie.starts_with("nirvanas") is False

        # Test with multiple branches
        trie.insert("nirvikalpa")
        assert trie.starts_with("nirvi") is True
        assert trie.starts_with("nirva") is True

        # Starts with empty string should be True
        assert trie.starts_with("") is True

    def test_print(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test the print function of the trie."""
        trie = Trie()
        trie.insert("satguru")
        trie.insert("guru")
        trie.insert("gurudeva")
        trie.print()
        captured = capsys.readouterr()
        expected = (
            "|-- g\n"
            "|   `-- u\n"
            "|       `-- r\n"
            "|           `-- u\n"
            "|               |-- *\n"
            "|               `-- d\n"
            "|                   `-- e\n"
            "|                       `-- v\n"
            "|                           `-- a\n"
            "|                               `-- *\n"
            "`-- s\n"
            "    `-- a\n"
            "        `-- t\n"
            "            `-- g\n"
            "                `-- u\n"
            "                    `-- r\n"
            "                        `-- u\n"
            "                            `-- *\n"
        )
        assert captured.out == expected



