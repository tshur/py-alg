print("aum")


class TrieNode:
    def __init__(self, letter: str):
        self.val = letter
        self.children: dict[str, TrieNode] = {}


class Trie:
    def __init__(self):
        self.trie: TrieNode = TrieNode("")

    def insert(self, word: str) -> None:
        current_node = self.trie

        for char in word:
            if char not in current_node.children:
                current_node.children[char] = TrieNode(char)
            current_node = current_node.children[char]

    def search(self, word: str) -> bool:
        current_node = self.trie
        for char in word:
            #             print(
            #                 f"Checking character: {char}, current node: {current_node.val}, children: {list(current_node.children.keys())}"
            # )
            if char not in current_node.children:
                return False
            current_node = current_node.children[char]
        return True

    def starts_with(self, prefix: str) -> bool:
        current_node = self.trie
        for char in prefix:
            if char not in current_node.children:
                return False
            current_node = current_node.children[char]
        return True

    def print(self) -> None:
        import builtins

        def _print(node: TrieNode, prefix: str) -> None:
            children: list[TrieNode] = sorted(
                node.children.values(), key=lambda n: n.val
            )
            num_children = len(children)
            for idx, child in enumerate(children):
                is_last = idx == num_children - 1
                branch = "└── " if is_last else "├── "
                builtins.print(prefix + branch + child.val)
                extension = "    " if is_last else "│   "
                _print(child, prefix + extension)

        builtins.print("Trie")
        _print(self.trie, "")


def main():
    trie = Trie()
    trie.insert("apple")
    print(trie.search("apple"))
    trie.insert("app")
    print(trie.search("app"))
    trie.insert("banana")
    trie.insert("bandana")
    trie.print()
    print("aum")


if __name__ == "__main__":
    main()
