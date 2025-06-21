from .next_in_sequence import next_in_sequence


class TestNextInSequence:
    def test_one_character(self):
        assert next_in_sequence('s') == 's'
        assert next_in_sequence('a') == 'a'
    
    def test_two_character(self):
        assert next_in_sequence('ab') == 'ba'
        assert next_in_sequence('ba') == 'ab'
    
    def test_three_character(self):
        assert next_in_sequence('abc') == 'acb'
        assert next_in_sequence('acb') == 'bac'
        assert next_in_sequence('bac') == 'bca'
        assert next_in_sequence('bca') == 'cab'
        assert next_in_sequence('cab') == 'cba'
        assert next_in_sequence('cba') == 'abc'
    
    def test_same_character(self):
        assert next_in_sequence('aaa') == 'aaa'

        assert next_in_sequence('aab') == 'aba'
        assert next_in_sequence('aba') == 'baa'
        assert next_in_sequence('baa') == 'aab'

    def test_four_character(self):
        assert next_in_sequence('abcd') == 'abdc'
        assert next_in_sequence('dcba') == 'abcd'
