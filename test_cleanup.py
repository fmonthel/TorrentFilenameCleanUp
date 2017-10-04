import cleanup as script

def test_string_cleanup():
    assert script.string_cleanup('test.Toto') == 'test-toto'