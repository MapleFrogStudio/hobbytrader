import hobbytrader

def test_exists_FMPAD_API_KEY():
    key = hobbytrader.FMPAD_API_KEY
    assert key is not None

def test_exists_DB_SQL_LIMIT():
    # Values can be None or a POSITIVE INT
    db_limit = hobbytrader.DB_SQL_LIMIT
    assert db_limit >= 0