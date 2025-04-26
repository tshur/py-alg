from .map import Map


class TestMap:
    def test_empty_map(self) -> None:
        hm = Map[str, int]()

        assert not hm
        assert len(hm) == 0
        assert str(hm) == ""
        assert list(hm) == []
