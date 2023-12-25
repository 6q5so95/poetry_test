# conftest.py

# テストパッケージ毎に出力ファイル名変更が可能なfixture
# テストパッケージ毎に配置

# 使い方
# test_xxx.py

# conftest.pyのfixtureを呼び出し
# def test_func(change_log_file):
#    logger = logging.getLogger("test_logger") 
#    logger.info("テストログ")


import pytest
import logging

@pytest.fixture(scope="function")
def change_log_file(request):
    log_file = request.param
    logger = logging.getLogger("test_logger")
    old_handler = logger.handlers[0]
    new_handler = logging.FileHandler(log_file)
    logger.addHandler(new_handler)
    logger.removeHandler(old_handler)
    yield 
    logger.addHandler(old_handler)
    logger.removeHandler(new_handler)
