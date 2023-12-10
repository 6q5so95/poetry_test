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
from UtilsSqlite3 import Sqlite3Manager

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
def database_resource_001()-> None:
    # テストデータ出力先定義
    db_file = PREFIX_TMP / 'sqltite3_tmp_replace.db'
    df = pd.DataFrame({
        'col1': [1, 2],
        'col2': [3, 4]
    })

    # setup
    logger.info(f"setup")

    # Exectute Test
    yield db_file, df

    # tear_down
    logger.info(f"tear down")


@pytest.fixture(scope='function')
def database_resource_002()-> None:
    # テストデータ出力先定義
    db_file = PREFIX_TMP / 'sqltite3_tmp_append.db'
    df = pd.DataFrame({
        'col1': [1, 2],
        'col2': [3, 4]
    })

    # setup
    logger.info(f"setup")

    # Exectute Test
    yield db_file, df

    # tear_down
    logger.info(f"tear down")


@pytest.fixture(scope='function')
def database_resource_003()-> None:
    # テストデータ出力先定義
    db_file = PREFIX_TMP / 'sqltite3_tmp_execute.db'
    df = pd.DataFrame({
        'col1': [1, 2],
        'col2': [3, 4]
    })

    # setup
    logger.info(f"setup")

    # Exectute Test
    yield db_file, df

    # tear_down
    logger.info(f"tear down")


@pytest.fixture(scope='function')
def database_resource_004()-> None:
    # テストデータ出力先定義
    db_file = PREFIX_TMP / 'sqltite3_tmp_fetch.db'
    df = pd.DataFrame({
        'col1': [1, 2],
        'col2': [3, 4]
    })

    # setup
    logger.info(f"setup")

    # Exectute Test
    yield db_file, df

    # tear_down
    logger.info(f"tear down")


###########################################
# テスト実施
############################################
# Important! C0, C1, C2観点でテスト範囲をカバーすること
# pytest -lsv xxxxxx

class Test_load_dataframe_to_sqlite3_replace:
    """load_dataframe_to_sqlite3_replace テスト全体をまとめたClass

    【C0】
        1回実施、テーブルロード確認
        2回実施、テーブルロード確認,replaceのため1回目と件数変わらず
        table名がstrでない、Falseが返る
        dataframeでない、Falseが返る
        parse処理での例外発生、Mock
        databaseファイルに対して読み取り権限なし、Falseが返る

    【C1】
        -

    【C2】
        空のDataFrameを渡す、0件テーブル生成

    """

    def test_C0_Normal_UT_df_to_sqlite3_table_once(self, database_resource_001):
        """
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        db_file, df = database_resource_001
        TABLE_NAME = 'Normal_UT_001'

        ## インスタンス生成
        db_handler = Sqlite3Manager(db_file)
        result = db_handler.load_dataframe_to_sqlite3_replace(df, TABLE_NAME)
        expected = True
        logger.info(f"result : {result}")

        # table件数チェック
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
            expected_record = 2
            result_record = cursor.fetchone()[0]

        # assert
        assert result == expected
        assert result_record == expected_record


    def test_C0_Normal_UT_df_to_sqlite3_table_twice(self, database_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: dfを指定したsqlite3 tableへ2回ロードする, replaceなので件数同じ
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        db_file, df = database_resource_001
        TABLE_NAME = 'Normal_UT_002'

        ## インスタンス生成
        db_handler = Sqlite3Manager(db_file)
        result = db_handler.load_dataframe_to_sqlite3_replace(df, TABLE_NAME)
        result = db_handler.load_dataframe_to_sqlite3_replace(df, TABLE_NAME)
        expected = True
        logger.info(f"result : {result}")

        # table件数チェック
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
            expected_record = 2
            result_record = cursor.fetchone()[0]

        # assert
        assert result == expected
        assert result_record == expected_record


    def test_C0_Error_UT_df_to_sqlite3_tablename_is_not_str(self, database_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: table名がstrでない, Falseが戻る
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        db_file, df = database_resource_001
        TABLE_NAME = 0000000000000000

        ## インスタンス生成
        db_handler = Sqlite3Manager(db_file)
        result = db_handler.load_dataframe_to_sqlite3_replace(df, TABLE_NAME)
        expected = False
        logger.info(f"result : {result}")

        # assert
        assert result == expected


    def test_C0_Error_UT_df_to_sqlite3_dataframe_is_not_valid(self, database_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: dfがpd.DataFrameでない Falseが戻る
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        db_file, df = database_resource_001
        TABLE_NAME = 'ERROR_table'

        ## インスタンス生成
        db_handler = Sqlite3Manager(db_file)
        result = db_handler.load_dataframe_to_sqlite3_replace("invalid_df", TABLE_NAME)
        expected = False
        logger.info(f"result : {result}")

        # assert
        assert result == expected


    def test_C0_Error_UT_lost_db_handler_read_permission(self, database_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: instance生成後db_pathへの読み取り権限失う
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        db_file, df = database_resource_001
        TABLE_NAME = 'ERROR_table'

        ## インスタンス生成
        db_handler = Sqlite3Manager(db_file)

        db_file.chmod(0o111)
        result = db_handler.load_dataframe_to_sqlite3_replace(df, TABLE_NAME)
        db_file.chmod(0o755)

        expected = False
        logger.info(f"result : {result}")

        # assert
        assert result == expected


    def test_C0_Error_UT_sqlite3_connect_raise_exception_by_mock(self, mocker, database_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: mockによりsqlite3.connect処理で例外発生
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        # mockerにて例外発生させる
        ## sqlite3オブジェクトのconnectを置き換えるという考え方をする。
        mocker.patch.object(sqlite3, "connect", side_effect=Exception)

        db_file, df = database_resource_001
        TABLE_NAME = 'ERROR_table'

        ## インスタンス生成
        db_handler = Sqlite3Manager(db_file)
        result = db_handler.load_dataframe_to_sqlite3_replace(df, TABLE_NAME)

        expected = False
        logger.info(f"result : {result}")

        # assert
        assert result == expected


    def test_C2_Normal_UT_record_empty(self, database_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: 空のDataFrameを渡す
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        db_file, df = database_resource_001
        TABLE_NAME = 'Normal_UT_003'

        ## インスタンス生成
        db_handler = Sqlite3Manager(db_file)
        result = db_handler.load_dataframe_to_sqlite3_replace(pd.DataFrame(), TABLE_NAME)
        expected = True
        logger.info(f"result : {result}")

        # table件数チェック
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
            expected_record = 0
            result_record = cursor.fetchone()[0]

        # assert
        assert result == expected
        assert result_record == expected_record


class Test_load_dataframe_to_sqlite3_append:
    """load_dataframe_to_sqlite3_append テスト全体をまとめたClass

    【C0】
        1回実施、テーブルロード確認
        2回実施、テーブルロード確認,appendのため1回目と2回目を積み上げ
        table名がstrでない、Falseが返る
        dataframeでない、Falseが返る
        databaseファイルに対して読み取り権限なし、Falseが返る
        parse処理での例外発生、Mock

    【C1】
        -

    【C2】
        空のDataFrameを渡す、0件テーブル生成

    """

    def test_C0_Normal_UT_df_to_sqlite3_table_once(self, database_resource_002):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: dfを指定したsqlite3 tableへappendロードする
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        db_file, df = database_resource_002
        TABLE_NAME = 'Normal_UT_001'

        # appendのため一旦テーブルを消す
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
        conn.commit()

        ## インスタンス生成
        db_handler = Sqlite3Manager(db_file)
        result = db_handler.load_dataframe_to_sqlite3_append(df, TABLE_NAME)
        expected = True
        logger.info(f"result : {result}")

        # table件数チェック
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
            expected_record = 2
            result_record = cursor.fetchone()[0]

        # assert
        assert result == expected
        assert result_record == expected_record


    def test_C0_Normal_UT_df_to_sqlite3_table_twice(self, database_resource_002):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: dfを指定したsqlite3 tableへappendロードする,２回実施なので２回分件数
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        db_file, df = database_resource_002
        TABLE_NAME = 'Normal_UT_002'

        # appendのため一旦テーブルを消す
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
        conn.commit()

        ## インスタンス生成
        db_handler = Sqlite3Manager(db_file)
        result = db_handler.load_dataframe_to_sqlite3_append(df, TABLE_NAME)
        result = db_handler.load_dataframe_to_sqlite3_append(df, TABLE_NAME)
        expected = True
        logger.info(f"result : {result}")

        # table件数チェック
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
            expected_record = 4
            result_record = cursor.fetchone()[0]
        logger.info(f"expected_record {expected_record}")
        logger.info(f"result_record {result_record}")

        # assert
        assert result == expected
        assert result_record == expected_record


    def test_C0_Error_UT_df_to_sqlite3_tablename_is_not_str(self, database_resource_002):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: table名がstrでない, Falseが戻る
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        db_file, df = database_resource_002
        TABLE_NAME = 000000000000000000

        ## インスタンス生成
        db_handler = Sqlite3Manager(db_file)
        result = db_handler.load_dataframe_to_sqlite3_append(df, TABLE_NAME)
        expected = False
        logger.info(f"result : {result}")

        # assert
        assert result == expected


    def test_C0_Error_UT_df_to_sqlite3_dataframe_is_not_valid(self, database_resource_002):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: dataframeを渡していない、Falseが返る
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        db_file, df = database_resource_002
        TABLE_NAME = 'ERROR_table'
        ## インスタンス生成
        db_handler = Sqlite3Manager(db_file)
        result = db_handler.load_dataframe_to_sqlite3_append("invalid_df", TABLE_NAME)
        expected = False
        logger.info(f"result : {result}")

        # assert
        assert result == expected


    def test_C0_Error_UT_lost_db_handler_read_permission(self, database_resource_002):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: instance生成後db_pathへの読み取り権限失う
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        db_file, df = database_resource_002
        TABLE_NAME = 'ERROR_table'

        ## インスタンス生成
        db_handler = Sqlite3Manager(db_file)

        db_file.chmod(0o111)
        result = db_handler.load_dataframe_to_sqlite3_append(df, TABLE_NAME)
        db_file.chmod(0o755)

        expected = False
        logger.info(f"result : {result}")

        # assert
        assert result == expected


    def test_C0_Error_UT_sqlite3_connect_raise_exception_by_mock(self, mocker, database_resource_002):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: mockによりsqlite3.connect処理で例外発生
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        # mockerにて例外発生させる
        ## sqlite3オブジェクトのconnectを置き換えるという考え方をする。
        mocker.patch.object(sqlite3, "connect", side_effect=Exception)

        db_file, df = database_resource_002
        TABLE_NAME = 'ERROR_table'

        ## インスタンス生成
        db_handler = Sqlite3Manager(db_file)
        result = db_handler.load_dataframe_to_sqlite3_append(df, TABLE_NAME)

        expected = False
        logger.info(f"result : {result}")

        # assert
        assert result == expected


    def test_C2_Normal_UT_record_empty(self, database_resource_002):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: 空のDataFrameを渡す
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        db_file, df = database_resource_002
        TABLE_NAME = 'Normal_UT_003'

        ## インスタンス生成
        db_handler = Sqlite3Manager(db_file)
        result = db_handler.load_dataframe_to_sqlite3_replace(pd.DataFrame(), TABLE_NAME)
        expected = True
        logger.info(f"result : {result}")

        # table件数チェック
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
            expected_record = 0
            result_record = cursor.fetchone()[0]

        # assert
        assert result == expected
        assert result_record == expected_record


class Test_execute_sql_sqlite3:
    """execute_sql_sqlite3 テスト全体をまとめたClass

    【C0】
        CREATE TABLE など基本的なSQLを実行する
        parse処理での例外発生、Mock

    【C1】
        SQLが文字列でない/空文字、Falseが返る
        SQLがSQLの体をなしていないSQL/存在しないテーブルを参照するSQL、Falseが返る

    【C2】
        -

    """
    def test_C0_Normal_UT_valid_sql(self, database_resource_003):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: 基本的なSQLを実行確認する
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        db_file, df = database_resource_003
        TABLE_NAME = 'VALID_UT_002'

        ## インスタンス生成
        db_handler = Sqlite3Manager(db_file)

        # appendのため一旦テーブルを消す
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
        conn.commit()
        assert db_handler.execute_sql_sqlite3(f"CREATE TABLE {TABLE_NAME}(id INTEGER PRIMARY KEY, name TEXT);") == True
        assert db_handler.execute_sql_sqlite3(f"INSERT INTO {TABLE_NAME}(id, name) VALUES (1, 'John');") == True
        assert db_handler.execute_sql_sqlite3(f"SELECT * FROM {TABLE_NAME};") == True


    def test_C0_Error_UT_exception_by_mocker(self, mocker, database_resource_003):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: mockによる例外発生、False戻りを確認
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        db_file, df = database_resource_003

        ## インスタンス生成
        db_handler = Sqlite3Manager(db_file)

        # Execute test
        # mockerにて例外発生させる
        ## sqlite3オブジェクトのconnectを置き換えるという考え方をする。
        mocker.patch.object(sqlite3, "connect", side_effect=Exception)

        # sqlite3エラー、その他例外発生を確認（ログから）
        assert db_handler.execute_sql_sqlite3("INVALID SQL") == False


    def test_C1_Error_UT_invalid_sql(self, database_resource_003):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: 渡すSQLがstrではない、空文字など
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        db_file, df = database_resource_003

        ## インスタンス生成
        db_handler = Sqlite3Manager(db_file)
        assert db_handler.execute_sql_sqlite3(None) == False
        assert db_handler.execute_sql_sqlite3(111) == False
        assert db_handler.execute_sql_sqlite3("") == False


    def test_C1_Error_UT_exception_by_invalid_sql(self, database_resource_003):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: 不正SQLによる例外発生を確認、戻りはFalse
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        db_file, df = database_resource_003
        TABLE_NAME = 'invalid_table'
        ## インスタンス生成

        db_handler = Sqlite3Manager(db_file)

        # 不正なSQLを渡す
        assert db_handler.execute_sql_sqlite3("INVALID SQL") == False
        # 存在しないテーブルを参照するSQLを渡す
        assert db_handler.execute_sql_sqlite3(f"SELECT * FROM {TABLE_NAME};") == False


class Test_fetch_sql_sqlite3:
    """fetch_sql_sqlite3 テスト全体をまとめたClass

    C0におけるケース:
        sqlText が str 型である場合、SQLのクエリが正常に実行できる場合は、その結果が適切であるかどうかを確認する。
        mockにより例外発生、Falseが返る

    C1におけるケース:
        sqlText が str 型でない場合、False を返す。
        SQLのクエリが実行できなかった場合、None を返す。

    C2におけるケース:
        -

    """
    def test_C0_Normal_UT_valid_sql(self, database_resource_004):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: fetch取り出し
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        db_file, df = database_resource_004
        TABLE_NAME = 'test_table_fetch'

        ## インスタンス生成
        db_handler = Sqlite3Manager(db_file)

        ## dfをロード
        db_handler.load_dataframe_to_sqlite3_replace(df, TABLE_NAME)

        ## fetch処理
        result = db_handler.fetch_sql_sqlite3(f"SELECT * FROM {TABLE_NAME}")
        logger.info(f"result: {result}")
        assert result != False
        assert len(result) == len(df)
        assert all(isinstance(row, tuple) for row in result)


    def test_C0_Error_UT_exception_by_mocker(self, mocker, database_resource_004):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: mockerでの例外発生
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        db_file, df = database_resource_004
        TABLE_NAME = 'test_table_fetch'

        ## インスタンス生成
        db_handler = Sqlite3Manager(db_file)

        ## dfをロード
        db_handler.load_dataframe_to_sqlite3_replace(df, TABLE_NAME)

        # Execute test
        # mockerにて例外発生させる
        ## sqlite3オブジェクトのconnectを置き換えるという考え方をする。
        mocker.patch.object(sqlite3, "connect", side_effect=Exception)

        ## fetch処理
        result = db_handler.fetch_sql_sqlite3("SELECT * FROM not_exists_table")
        logger.info(f"result: {result}")
        assert result == False


    def test_C1_Error_UT_invalid_sql_type(self, database_resource_004):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: 渡すSQLがstrではない
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        db_file, df = database_resource_004
        TABLE_NAME = 'test_table_fetch'

        ## インスタンス生成
        db_handler = Sqlite3Manager(db_file)

        ## dfをロード
        db_handler.load_dataframe_to_sqlite3_replace(df, TABLE_NAME)

        ## fetch処理
        invalid_query = 1234
        assert db_handler.fetch_sql_sqlite3(invalid_query) == False
        assert db_handler.fetch_sql_sqlite3('') == False


    def test_C1_Error_UT_invalid_sql(self, database_resource_004):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: fetch取り出し、存在しないテーブルを指定
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        db_file, df = database_resource_004
        TABLE_NAME = 'test_table_fetch'

        ## インスタンス生成
        db_handler = Sqlite3Manager(db_file)

        ## dfをロード
        db_handler.load_dataframe_to_sqlite3_replace(df, TABLE_NAME)

        ## fetch処理
        result = db_handler.fetch_sql_sqlite3("SELECT * FROM not_exists_table")
        logger.info(f"result: {result}")
        assert result == False


