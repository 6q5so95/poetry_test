# library
import csv
import inspect
import os
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
from UtilsDataHelper import check_file_read_permission
from UtilsDataHelper import check_file_write_permission
from UtilsDataHelper import delete_file

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
def data_helper_resource_001() -> Path:
    # テストデータ出力先定義
    ## ここでのテストは中身は何でも良い
    outfile = PREFIX_TMP / 'test_UtilsDataHelper_temp_N001.csv'
    if not outfile.exists():
        with open(outfile, 'w') as f:
            f.write('title1|title2|title3\n')
            f.write('aaaaaa|10|11\n')
            f.write('bbbbbb|20|21\n')
            f.write('cccccc|30|31\n')
    # setup
    logger.info(f"setup")

    # Exectute Test
    yield outfile

    # tear_down
    logger.info(f"tear down")


###########################################
# テスト実施
############################################
# Important! C0, C1, C2観点でテスト範囲をカバーすること
# pytest -lsv xxxxxx

class Test_check_file_read_permission:
    """check_file_read_permission テスト全体をまとめたClass

    C0: 命令カバレッジ
        ファイルが存在し、読み取り可能である場合にTrueを返すことを確認する
        ファイルが存在し、読み取り権限を付与した状況でTrueを返すことを確認する
        PathObject以外を渡す
        存在しないファイルPathを指定、Falseが返る
        file以外を指定する（ディレクトリを指定）
        指定ファイルの読み取り権限を外す、Falseが返る

    C1: 分岐カバレッジ
    C2: 条件カバレッジ
        -
    """
    def test_C0_Normal_UT_file_exists(self, data_helper_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: 存在するファイルパスを指定する
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = check_file_read_permission(data_helper_resource_001)
        expected = True
        logger.info(f"result : {result}")

        # assert
        assert str(type(result)) == "<class 'bool'>"
        assert result == expected


    def test_C0_Normal_UT_target_path_is_readable(self, data_helper_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: 存在するディレクトリ指定する 読み取り権限付与する
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        data_helper_resource_001.chmod(0o444)
        result = check_file_read_permission(data_helper_resource_001)
        expected = True
        data_helper_resource_001.chmod(0o777)
        logger.info(f"result : {result}")

        # assert
        assert str(type(result)) == "<class 'bool'>"
        assert result == expected


    def test_C0_Error_UT_not_PathObject(self, data_helper_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ:  PathObject以外を渡す
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = check_file_read_permission('AAAAAAAAAAAAAAAAAAAAA')
        expected = False
        logger.info(f"result : {result}")

        # assert
        assert str(type(result)) == "<class 'bool'>"
        assert result == expected


    def test_C0_Error_UT_file_not_exists(self, data_helper_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: 存在しないファイルパスObjectを指定する
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = check_file_read_permission(Path('AAAAAAAAAAAAAAAAAAAAAAAAAAAAA'))
        expected = False
        logger.info(f"result : {result}")

        # assert
        assert str(type(result)) == "<class 'bool'>"
        assert result == expected


    def test_C0_Error_UT_target_is_directory(self, data_helper_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: 存在するディレクトリ指定する
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        parent_path = data_helper_resource_001.parent
        logger.info(Path(parent_path))
        result = check_file_read_permission(parent_path)
        expected = False
        logger.info(f"result : {result}")

        # assert
        assert str(type(result)) == "<class 'bool'>"
        assert result == expected


    def test_C0_Error_UT_target_path_is_not_readable(self, data_helper_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: 指定ファイルの読み取り権限を外す
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        data_helper_resource_001.chmod(0o000)
        result = check_file_read_permission(data_helper_resource_001)
        expected = False
        data_helper_resource_001.chmod(0o777)
        logger.info(f"result : {result}")

        # assert
        assert str(type(result)) == "<class 'bool'>"
        assert result == expected


class Test_check_file_write_permission:
    """check_fileWritePermission テスト全体をまとめたClass

    C0: 命令カバレッジ
        ファイルが存在し書き込み権限がある場合にTrueを返す
        1つ上階層のディレクトリに書き込み権限がある場合にTrueを返す(ファイルあり）
        1つ上階層のディレクトリに書き込み権限がある場合にTrueを返す(ファイルなし）
        file_pathがPathオブジェクトでない場合、Falseを返す
        file_pathが存在しないPathオブジェクトの場合、Trueを返す
        file_pathの親ディレクトリが存在しない場合、Falseを返す
        file_pathの親ディレクトリに書き込み権限がない場合、Falseを返す
        file_pathがファイルがある場合で書き込み権限がない場合、Falseを返す

    C1: 分岐カバレッジ
    C2: 条件カバレッジ
        -
    """
    def test_C0_Normal_UT_file_exists(self, data_helper_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: 存在するファイルパスを指定する
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        data_helper_resource_001.chmod(0o755)
        result = check_file_write_permission(data_helper_resource_001)
        expected = True
        logger.info(f"result : {result}")

        # assert
        assert str(type(result)) == "<class 'bool'>"
        assert result == expected


    def test_C0_Normal_UT_target_parent_path_exists_and_file_exitsts_with_write_permission(self, data_helper_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: 親ディレクトリに書き込み権限がありファイルが存在する
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        parent_path = data_helper_resource_001.parent
        parent_path.chmod(0o755)
        logger.info(f"parent dir has write permission: {os.access(parent_path, os.W_OK)}")
        logger.info(f"target file is exists: {data_helper_resource_001.exists()}")
        result = check_file_write_permission(data_helper_resource_001)
        expected = True

        # assert
        assert str(type(result)) == "<class 'bool'>"
        assert result == expected


    def test_C0_Normal_UT_target_parent_path_exists_and_file_not_exitsts(self, data_helper_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: 親ディレクトリに書き込み権限がありファイルが存在しない
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        parent_path = data_helper_resource_001.parent
        parent_path.chmod(0o755)
        logger.info(f"parent dir has write permission: {os.access(parent_path, os.W_OK)}")
        logger.info(f"target file is not exists: {(parent_path / 'not_exists_file_aaaaaaaaaaaaaa').exists()}")
        result = check_file_write_permission(parent_path / 'not_exists_file_aaaaaaaaaaaaaa')
        expected = True

        # assert
        assert str(type(result)) == "<class 'bool'>"
        assert result == expected


    def test_C1_Error_UT_target_path_is_not_PathObject(self, data_helper_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: 指定ファイルパスがPathオブジェクトでない
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = check_file_write_permission('AAAAAAAAAAAAAAAAAAAA')
        expected = False
        logger.info(f"result : {result}")

        # assert
        assert str(type(result)) == "<class 'bool'>"
        assert result == expected


    def test_C1_Error_UT_target_path_is_not_exists_PathObject(self, data_helper_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: 指定ファイルパスが存在しないPathObject
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = check_file_write_permission(Path('/AAAA/AAAAAAAAAAAAAAAA'))
        expected = False
        logger.info(f"result : {result}")

        # assert
        assert str(type(result)) == "<class 'bool'>"
        assert result == expected


    def test_C1_Error_UT_target_parent_path_has_not_write_permission(self, data_helper_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 正常系/UT
        - テストシナリオ: 親ディレクトリに書き込み権限がない
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        parent_path = data_helper_resource_001.parent
        parent_path.chmod(0o444)
        logger.info(f"parent dir has write permission: {os.access(parent_path, os.W_OK)}")
        expected = False
        result = check_file_write_permission(data_helper_resource_001)
        parent_path.chmod(0o755)

        # assert
        assert str(type(result)) == "<class 'bool'>"
        assert result == expected


    def test_C1_Normal_UT_target_parent_path_exists_and_file_exitsts_with_no_write_permission(self, data_helper_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: 親ディレクトリに書き込み権限がありファイルが存在するがファイルに書き込み権限がない
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        parent_path = data_helper_resource_001.parent
        parent_path.chmod(0o755)
        logger.info(f"parent dir has write permission: {os.access(parent_path, os.W_OK)}")
        data_helper_resource_001.chmod(0o444)
        logger.info(f"target_file has not write permission: {os.access(data_helper_resource_001, os.W_OK)}")
        expected = False
        result = check_file_write_permission(data_helper_resource_001)
        data_helper_resource_001.chmod(0o755)

        # assert
        assert str(type(result)) == "<class 'bool'>"
        assert result == expected


class Test_delete_file:
    """delete_file テスト全体をまとめたClass

    C0: 命令カバレッジ
        1つ上階層のディレクトリに書き込み権限がありファイルを消す
        file_pathに指定したファイル削除中に例外が発生する mockで実現する
        file_pathがPathオブジェクトでない場合、Falseを返す
        file_pathが存在しないPathObjectの場合、Falseを返す
        file_pathに指定した親ディレクトリに書き込み権限がない
        file_pathがファイルではない
        1つ上階層のディレクトリに書き込み権限がありファイルには書き込み権限なし、だがファイルは消せる

    C1: 分岐カバレッジ
    C2: 条件カバレッジ
    """

    def test_C0_Normal_UT_file_exists(self, data_helper_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: 存在するファイルパスを指定する,親ディレクトリに書き込み権限あり
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        parent_path = data_helper_resource_001.parent
        parent_path.chmod(0o755)
        logger.info(f"parent dir has write permission: {os.access(parent_path, os.W_OK)}")
        result = delete_file(data_helper_resource_001)
        expected = True
        logger.info(f"result : {result}")

        # assert
        assert str(type(result)) == "<class 'bool'>"
        assert result == expected


    def test_C0_Error_UT_open_error_by_mock(self, mocker, data_helper_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: データ操作処理のtry-catchでのexceptionをmockでシミュレート
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # check
        assert data_helper_resource_001.exists()

        # mockerにて例外発生させる
        ## Pathオブジェクトのunlinkを置き換えるという考え方をする。
        ## Path.unlinkを置き換える、という扱いではないので留意。
        mocker.patch.object(Path, "unlink", side_effect=Exception)

        # Execute test
        result = delete_file(data_helper_resource_001)
        logger.info(f"result: \n{result}")

        # assert
        assert str(type(result)) == "<class 'bool'>"
        expected = False


    def test_C1_Error_UT_target_path_is_not_PathObject(self, data_helper_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: 指定ファイルパスがPathオブジェクトでない
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = delete_file('AAAAAAAAAAAAAAAAAAAA')
        expected = False
        logger.info(f"result : {result}")

        # assert
        assert str(type(result)) == "<class 'bool'>"
        assert result == expected


    def test_C1_Error_UT_target_path_is_not_exists_PathObject(self, data_helper_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: 指定ファイルパスが存在しないPathオブジェクト
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = delete_file(Path('AAAAAAAAAAAAAAAAAAAA'))
        expected = False
        logger.info(f"result : {result}")

        # assert
        assert str(type(result)) == "<class 'bool'>"
        assert result == expected


    def test_C1_Error_UT_target_parent_path_has_not_write_permission(self, data_helper_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: 親ディレクトリに書き込み権限がない
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        parent_path = data_helper_resource_001.parent
        logger.info(f"create file: {data_helper_resource_001}")
        parent_path.chmod(0o444)
        logger.info(f"parent dir has write permission: {os.access(parent_path, os.W_OK)}")
        expected = False
        result = delete_file(data_helper_resource_001)
        parent_path.chmod(0o755)

        # assert
        assert str(type(result)) == "<class 'bool'>"
        assert result == expected


    def test_C1_Error_UT_target_is_directory(self, data_helper_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: 存在するディレクトリ指定する,ファイルを指定していない
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        parent_path = data_helper_resource_001.parent
        logger.info(f"target is: {parent_path}")
        result = delete_file(parent_path)
        expected = False
        logger.info(f"result : {result}")

        # assert
        assert str(type(result)) == "<class 'bool'>"
        assert result == expected


    def test_C2_Error_UT_target_parent_path_has_write_permission_file_not_has_write_permission(self, data_helper_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C2
        - テスト区分: 異常系/UT
        - テストシナリオ: 親ディレクトリに書き込み権限あり、ファイルに書き込み権限なし、だがファイルは消せる
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        parent_path = data_helper_resource_001.parent
        logger.info(f"create file: {data_helper_resource_001}")
        data_helper_resource_001.chmod(0o111)
        parent_path.chmod(0o755)
        logger.info(f"file has not write permission: {os.access(data_helper_resource_001, os.W_OK)}")
        logger.info(f"parent dir has write permission: {os.access(parent_path, os.W_OK)}")
        expected = True
        result = delete_file(data_helper_resource_001)
        if data_helper_resource_001.exists():
            data_helper_resource_001.chmod(0o755)

        # assert
        assert str(type(result)) == "<class 'bool'>"
        assert result == expected
