from dsap.tree import Trie


class TestTrie:
    def test_init(self) -> None:
        trie = Trie()

        assert trie.search("hello") is False
        assert trie.starts_with("hello") is False
