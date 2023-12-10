# library
import csv
import inspect
import os
import sqlite3
import pandas as pd
import pytest
import re
import shutil
import sys
import yaml

from pathlib import Path
from pprint import pprint
from tabulate import tabulate as tb
from typing import Any
from typing import List
from typing import Optional
from typing import Union

# logger
import logging
import logging.config

#######################################################
# テスト対象ライブラリパス追加/ロード
#######################################################
TARGET_PREFIX = Path(__file__).parent.parent.parent / 'src'
TARGET_PREFIX_LIB = TARGET_PREFIX / 'lib'
sys.path.append(str(TARGET_PREFIX_LIB))
from UtilsYamlloader import YamlParser

############################################
# 実行環境PREFIX 生成
############################################
PREFIX = Path(__file__).parent.parent
PREFIX_DEF = PREFIX / 'def'
PREFIX_LOG = PREFIX / 'log'
PREFIX_TMP = PREFIX / 'tmp'
LOGGINIG_INI = PREFIX_DEF / 'logging.ini'
LOGGINIG_LOG = PREFIX_LOG / 'app.log'

############################################
# logger 定義
############################################
logging.config.fileConfig(LOGGINIG_INI)
logger = logging.getLogger(__name__)

############################################
# Helper 関数
############################################

############################################
# fixture
############################################
@pytest.fixture(scope='function')
def yaml_resource_001()-> None:
    # テストデータ出力先定義
    yaml_file = PREFIX_TMP / 'yamlloader_test.yaml'
    data = {
        'name': 'John',
        'age': 25,
        'pets': [
            {'name': 'Fido', 'type': 'dog'},
            {'name': 'Mittens', 'type': 'cat'}
        ]
    }
    with open(yaml_file, 'w') as f:
        yaml.dump(data, f)

    # setup
    logger.info(f"setup")

    # Exectute Test
    yield yaml_file 

    # tear_down
    logger.info(f"tear down")


###########################################
# テスト実施
############################################
# Important! C0, C1, C2観点でテスト範囲をカバーすること
# pytest -lsv xxxxxx

class Test_YamlParser:
    """YamlPaser テスト全体をまとめたClass

    【C0】
        条件を満たすyamlファイルを指定して実行、listが戻る
        parse処理での例外発生、Mock
        yaml_pathがPathオブジェクトでない、Noneが返る
        yaml_pathが存在しないPathオブジェクト、Noneが返る
        yaml_pathにNone、Noneが返る
        yaml_pathに読み取り権限なし、Noneが返る

    【C1】
        -

    【C2】
        -

    """
    def test_C0_Normal_UT_(self, yaml_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ:条件を満たすyamlファイルを読み込む
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = YamlParser.parse_yaml_file(yaml_resource_001)
        expected = True
        logger.info(f"result : {result}")

        # assert
        assert isinstance(result, dict)  == expected


    def test_C0_Error_UT_Exception_by_mock(self, mocker, yaml_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: mockによる例外、Noneが返る
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # openコマンド実行時にExceptionが発生するようMocker定義を行う
        mocker.patch("builtins.open", side_effect=Exception)

        # Execute test
        result = YamlParser.parse_yaml_file(yaml_resource_001)
        expected = None
        logger.info(f"result : {result}")

        # assert
        assert result == expected


    def test_C0_Error_UT_file_path_is_not_Path(self, yaml_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: PathObjectでないものを渡す、Noneが返る
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = YamlParser.parse_yaml_file('AAAAAAAAAAAAAAAAAA')
        expected = None
        logger.info(f"result : {result}")

        # assert
        assert result == expected


    def test_C0_Error_UT_file_path_is_not_exists_Path(self, yaml_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: 存在しないテキトーなPathオブジェクトを渡す
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = YamlParser.parse_yaml_file(Path('AAAAAAAAAAAAAAAAAA'))
        expected = None
        logger.info(f"result : {result}")

        # assert
        assert result == expected


    def test_C0_Error_UT_file_path_is_None(self, yaml_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: PathにNoneを渡す、Noneが返る
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = YamlParser.parse_yaml_file(None)
        expected = None
        logger.info(f"result : {result}")

        # assert
        assert result == expected


    def test_C0_Error_UT_file_path_has_not_read_permission(self, yaml_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: Pathに読み取り権限なし、Noneが返る
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        yaml_resource_001.chmod(0o111)
        result = YamlParser.parse_yaml_file(None)
        expected = None
        yaml_resource_001.chmod(0o755)
        logger.info(f"result : {result}")

        # assert
        assert result == expected

