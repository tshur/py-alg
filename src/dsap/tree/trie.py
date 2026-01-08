# 2026 Akash Katir, Hand written except docstrings and functions specified

class TrieNode:
    """A node in the Trie data structure.

    Each node represents a single character and contains references to child nodes
    for subsequent characters. A special "*" child indicates the end of a complete word.

    Attributes:
        val (str): The character stored in this node.
        children (dict[str, TrieNode]): Mapping from characters to child nodes.
    """

    val: str
    children: dict[str, "TrieNode"]

    def __init__(self, letter: str):
        """Initialize a TrieNode with the given character.

        Args:
            letter (str): The character to store in this node.
        """
        self.val = letter
        self.children: dict[str, TrieNode] = {}


class Trie:
    """Trie (prefix tree) data structure for efficient string operations.

    A trie is a tree-like data structure used for storing strings where each node
    represents a character. Words sharing common prefixes share the same path from
    the root. End-of-word markers ("*") indicate complete words in the trie.

    Basic operations:
      - insert, O(m) where m is the length of the word.
      - search, O(m) where m is the length of the word.
      - starts_with, O(m) where m is the length of the prefix.

    Examples:
        >>> trie = Trie()
        >>> trie.insert("apple")
        >>> trie.search("apple")
        True
        >>> trie.search("app")
        False
        >>> trie.starts_with("app")
        True
    """

    def __init__(self):
        """Initialize an empty Trie with a root node."""
        self.trie: TrieNode = TrieNode("")

    def insert(self, word: str) -> None:
        """Insert a word into the trie.

        Traverses the trie character by character, creating new nodes as needed.
        Marks the end of the word with a special "*" child node.

        Complexity:
            Time: O(m), where m is the length of the word.
            Space: O(m), for creating new nodes in the worst case.

        Args:
            word (str): The word to insert into the trie.

        Examples:
            >>> trie = Trie()
            >>> trie.insert("hello")
            >>> trie.search("hello")
            True
            >>> trie.insert("help")
            >>> trie.starts_with("hel")
            True
        """
        if not word:
            raise ValueError("word cannot be empty")
        
        current_node = self.trie
        
        for char in word:
            if char not in current_node.children:
                current_node.children[char] = TrieNode(char)
            
            current_node = current_node.children[char]
        current_node.children["*"] = TrieNode("*")

    def search(self, word: str) -> bool:
        """Search for a complete word in the trie.

        Traverses the trie character by character. Returns True only if the entire
        word exists and is marked as a complete word (has "*" marker).

        Complexity:
            Time: O(m), where m is the length of the word.
            Space: O(1)

        Args:
            word (str): The word to search for in the trie.

        Returns:
            bool: True if the word exists as a complete word in the trie,
              False otherwise.

        Examples:
            >>> trie = Trie()
            >>> trie.insert("apple")
            >>> trie.search("apple")
            True
            >>> trie.search("app")
            False
            >>> trie.search("application")
            False
        """
        current_node = self.trie
        for char in word:
            if char not in current_node.children:
                return False
            current_node = current_node.children[char]

        return "*" in current_node.children

    def starts_with(self, prefix: str) -> bool:
        """Check if any word in the trie starts with the given prefix.

        Traverses the trie character by character. Returns True if the prefix
        path exists, regardless of whether it forms a complete word.

        Complexity:
            Time: O(m), where m is the length of the prefix.
            Space: O(1)

        Args:
            prefix (str): The prefix to search for in the trie.

        Returns:
            bool: True if any word in the trie starts with the given prefix,
              False otherwise.

        Examples:
            >>> trie = Trie()
            >>> trie.insert("apple")
            >>> trie.starts_with("app")
            True
            >>> trie.starts_with("apl")
            False
            >>> trie.starts_with("apple")
            True
        """
        current_node = self.trie
        for char in prefix:
            if char not in current_node.children:
                return False
            current_node = current_node.children[char]
        return True

    def print(self) -> None:
        """Print a visual representation of the trie structure.

        Displays the trie as a tree with branches showing the hierarchical
        relationship between characters. Uses "|--" and "`--" to indicate
        branches and last children respectively.

        Function written by claude 3.5 sonnet

        Complexity:
            Time: O(n), where n is the total number of nodes in the trie.
            Space: O(h), where h is the height of the trie (recursion depth).

        Examples:
            >>> trie = Trie()
            >>> trie.insert("app")
            >>> trie.insert("apple")
            >>> trie.print()
            Trie
            `-- a
                `-- p
                    `-- p
                        |-- *
                        `-- l
                            `-- e
                                `-- *
        """

        def _print(node: TrieNode, prefix: str) -> None:
            children: list[TrieNode] = sorted(
                node.children.values(), key=lambda n: n.val
            )
            num_children = len(children)
            for idx, child in enumerate(children):
                is_last = idx == num_children - 1
                branch = "`-- " if is_last else "|-- "
                print(prefix + branch + child.val)
                extension = "    " if is_last else "|   "
                _print(child, prefix + extension)

        print("Trie")
        _print(self.trie, "")
