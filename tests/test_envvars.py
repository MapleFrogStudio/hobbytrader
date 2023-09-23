import hobbytrader

def test_exists_FMPAD_API_KEY():
    key = hobbytrader.FMPAD_API_KEY
    assert key is not None

