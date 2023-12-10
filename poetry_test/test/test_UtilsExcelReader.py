# library
import csv
import inspect
import os
import pandas as pd
import pytest
import re
import shutil
import sys

from pandas.testing import assert_frame_equal
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
from UtilsExcelReader import import_excel_onesheet_to_dataframe
from UtilsExcelReader import import_excel_sheets_to_dataframe

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
def excel_result_001()-> Optional[pd.DataFrame]:

    # setup
    logger.info(f"setup")
    df = pd.DataFrame(
        {
            "A": [1, 2, 3, 4],
            "B": [5, 6, 7, 8],
            "C": [9, 10, 11, 12],
            "D": [13, 14, 15, 16],
        },
    )
    return df.iloc[:, [0,3]]

@pytest.fixture(scope='function')
def excel_result_002()-> Optional[pd.DataFrame]:

    # setup
    logger.info(f"setup")
    df = pd.DataFrame(
        {
            "A": [1, 2, 3, 4],
            "B": [5, 6, 7, 8],
            "C": [9, 10, 11, 12],
            "D": [13, 14, 15, 16],
        },
    )
    return df

@pytest.fixture(scope='function')
def excel_result_003()-> Optional[pd.DataFrame]:

    # setup
    logger.info(f"setup")
    df = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5, 6, 7, 8, 9],
            "col2": ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'],
        },
    )
    return df

@pytest.fixture(scope='function')
def excel_result_004()-> Optional[pd.DataFrame]:

    # setup
    logger.info(f"setup")
    df = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5, 6],
            "col2": ['a', 'b', 'c', 'd', 'e', 'f'],
        },
    )
    return df

@pytest.fixture(scope='function')
def excel_result_005()-> Optional[pd.DataFrame]:

    # setup
    logger.info(f"setup")
    df = pd.DataFrame(
        {
            "col1": [1, 2, 3],
            "col2": ['a', 'b', 'c'],
        },
    )
    return df


@pytest.fixture(scope='function')
def excel_result_006()-> Optional[pd.DataFrame]:

    # setup
    logger.info(f"setup")
    df = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, -1, -2],
            "col2": ['a', 'b', 'c', 'd', 'e', 'f','g','h', 'i', 'j', 'k', 'l'],
        },
    )
    return df

@pytest.fixture(scope='function')
def excel_resource_001()-> Optional[Path]:
    # テストデータ出力先定義
    outfile = PREFIX_TMP / 'test_UtilsExcelReader_temp_N001.xlsx'

    # setup
    logger.info(f"setup")
    df = pd.DataFrame(
        {
            "A": [1, 2, 3, 4],
            "B": [5, 6, 7, 8],
            "C": [9, 10, 11, 12],
            "D": [13, 14, 15, 16],
        },
    )
    df.to_excel(outfile, index=False)

    # Exectute Test
    yield outfile

    # tear_down
    logger.info(f"tear down")
    outfile.chmod(0o755)
    if outfile.exists():
        logger.info(f"shutil.rmtree: {outfile.parent}")
        #shutil.rmtree(f"{outfile.parent}")


@pytest.fixture(scope='function')
def excel_resource_002()-> Optional[Path]:
    # テストデータ出力先定義
    outfile = PREFIX_TMP / 'test_UtilsExcelReader_temp_N002.xlsx'

    # setup
    logger.info(f"setup")
    sample_data = {
        'Sheet1': {'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']},
        'Sheet2': {'col1': [4, 5, 6], 'col2': ['d', 'e', 'f']},
        'Sheet3': {'col1': [7, 8, 9], 'col2': ['g', 'h', 'i']},
    }
    with pd.ExcelWriter(outfile) as writer:
        for sheet_name, data in sample_data.items():
            pd.DataFrame(data).to_excel(writer, sheet_name=sheet_name, index=False)

    # Exectute Test
    yield outfile

    # tear_down
    logger.info(f"tear down")
    outfile.chmod(0o755)
    if outfile.exists():
        logger.info(f"shutil.rmtree: {outfile.parent}")
        #shutil.rmtree(f"{outfile.parent}")


@pytest.fixture(scope='function')
def excel_resource_003()-> Optional[Path]:
    # テストデータ出力先定義
    outfile = PREFIX_TMP / 'test_UtilsExcelReader_temp_N003.xlsx'

    # setup
    logger.info(f"setup")
    sample_data = {
        'Sheet1': {'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']},
    }
    with pd.ExcelWriter(outfile) as writer:
        for sheet_name, data in sample_data.items():
            pd.DataFrame(data).to_excel(writer, sheet_name=sheet_name, index=False)

    # Exectute Test
    yield outfile

    # tear_down
    logger.info(f"tear down")
    outfile.chmod(0o755)
    if outfile.exists():
        logger.info(f"shutil.rmtree: {outfile.parent}")
        #shutil.rmtree(f"{outfile.parent}")


@pytest.fixture(scope='function')
def excel_resource_004()-> Optional[Path]:
    # テストデータ出力先定義
    outfile = PREFIX_TMP / 'test_UtilsExcelReader_temp_N003.xlsx'

    # setup
    logger.info(f"setup")
    sample_data = {
        'Sheet1': {'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']},
        'Sheet2': {'col1': [4, 5, 6], 'col2': ['d', 'e', 'f']},
        'Sheet3': {'col1': [7, 8, 9], 'col2': ['g', 'h', 'i']},
        'Sheet4': {'col1': [0, -1, -2], 'col2': ['j', 'k', 'l'], 'col3':['x1', 'x2', 'x3']},
    }
    with pd.ExcelWriter(outfile) as writer:
        for sheet_name, data in sample_data.items():
            pd.DataFrame(data).to_excel(writer, sheet_name=sheet_name, index=False)

    # Exectute Test
    yield outfile

    # tear_down
    logger.info(f"tear down")
    outfile.chmod(0o755)
    if outfile.exists():
        logger.info(f"shutil.rmtree: {outfile.parent}")
        #shutil.rmtree(f"{outfile.parent}")

###########################################
# テスト実施
############################################
# Important! C0, C1, C2観点でテスト範囲をカバーすること
# pytest -lsv xxxxxx

class Test_import_excel_onesheet_to_dataframe:
    """import_excel_onesheet_to_dataframeのテスト全体をまとめたClass

    【C0】
        関数に渡される引数file_pathが存在する、かつ読み込み権限がある、usecols指定あり、対象シートがBookにある
        関数に渡される引数file_pathがPathObjectでない
        関数に渡される引数file_pathが存在しない場合、Noneが返却される。
        関数に渡される引数file_pathが存在するが、読み込み権限がない場合、Noneが返却される。
        関数に渡される引数use_colsを指定せずデフォルト値のまま
        関数に渡される引数use_colsをint型でないlistを設定する
        pd.Excel処理での例外発生、Mock
        parse処理での例外発生、Mock

    【C1】
        関数に渡される引数target_sheet_nameをNone指定

    【C2】
        ファイルが存在しないシート名を指定した場合、Noneが返却される。
        -
    """

    def test_C0_Normal_UT_set_param_usecols_is_int_list(self, excel_resource_001, excel_result_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: パラメータ use_colsにint要素以外のlistを設定、None戻り
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        logger.info(f"param set use_cols to Non int list")
        expected = excel_result_001
        result = import_excel_onesheet_to_dataframe(
            excel_resource_001,
            'Sheet1',
            skiprows=0,
            usecols=[0, 3],
            )
        logger.info(f"result: \n{tb(result, headers='keys')}")
        logger.info(f"result.shape: \n{result.shape}")
        logger.info(f"expected: \n{tb(expected, headers='keys')}")

        # assert
        assert type(result) == pd.DataFrame
        logger.info(f"expected/result 一致確認(Noneが一致): {assert_frame_equal(expected, result)}")


    def test_C1_Error_UT_path_is_not_Path_instance(self, excel_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: Pathインスタンス以外を渡す,None戻り確認
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_excel_onesheet_to_dataframe(
            "AAAAAAAAAAAAA",
            'Sheet1',
            skiprows=0,
            usecols=[0, 3],
            )
        logger.info(f"result: \n{result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == None


    def test_C1_Error_UT_path_is_not_exists(self, excel_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: PathObjectに存在しない適当なファイルパスを設定、None戻り確認
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_excel_onesheet_to_dataframe(
            Path("AAAAAAAAAAAAA"),
            'Sheet1',
            skiprows=0,
            usecols=[0, 3],
            )
        logger.info(f"result: \n{result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == None


    def test_C1_Error_UT_file_exitsts_with_no_write_permission(self, excel_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: ファイルが存在するがファイルに読み込み権限がない
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        excel_resource_001.chmod(0o111)
        logger.info(f"target_file has write permission: {os.access(excel_resource_001, os.R_OK)}")
        expected = None
        result = import_excel_onesheet_to_dataframe(
            excel_resource_001,
            'Sheet1',
            skiprows=0,
            usecols=[0, 3],
            )
        logger.info(f"result: \n{result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == expected


    def test_C1_Error_UT_set_param_use_cols_None(self, excel_resource_001, excel_result_002):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: パラメータ use_colsにNoneをセット（デフォルト）、None戻り
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        logger.info(f"param set use_cols to None")
        expected = excel_result_002
        result = import_excel_onesheet_to_dataframe(
            excel_resource_001,
            'Sheet1',
            skiprows=0,
            #usecols=None,
            )
        logger.info(f"result: \n{result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == None


    def test_C0_Error_UT_set_param_use_cols_is_not_int_list(self, excel_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: パラメータ use_colsにint要素以外のlistを設定、None戻り
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        logger.info(f"param set use_cols to Non int list")
        expected = None
        result = import_excel_onesheet_to_dataframe(
            excel_resource_001,
            'Sheet1',
            skiprows=0,
            usecols=["A", "C"],
            )
        logger.info(f"result: \n{result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == expected


    def test_C0_Error_UT_raise_pd_Excel_exception_by_mock(self, mocker, excel_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: パラメータ mockによりException発生させる, 戻りはNone
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        logger.info(f"by Mock except Exception")

        # mockerにて例外発生させる
        mocker.patch.object(pd, "ExcelFile", side_effect=Exception)

        expected = None
        result = import_excel_onesheet_to_dataframe(
            excel_resource_001,
            'Sheet1',
            skiprows=0,
            usecols=[0, 3],
            )
        logger.info(f"result: \n{result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == expected


    def test_C0_Error_UT_raise_parse_exception_by_mock(self, mocker, excel_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: パラメータ mockによりException発生させる, 戻りはNone
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        logger.info(f"by Mock except Exception")

        # mockerにて例外発生させる
        mocker.patch.object(pd.ExcelFile, "parse", side_effect=Exception)

        expected = None
        result = import_excel_onesheet_to_dataframe(
            excel_resource_001,
            'Sheet1',
            skiprows=0,
            usecols=[0, 3],
            )
        logger.info(f"result: \n{result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == expected


    def test_C1_Error_UT_set_param_target_sheet_name_is_none(self, excel_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: パラメータ target_sheet_nameにNone指定,None戻り
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        logger.info(f"param set target_sheet_name is not exists name")
        expected = None
        result = import_excel_onesheet_to_dataframe(
            excel_resource_001,
            None,
            skiprows=0,
            usecols=[0, 3],
            )
        logger.info(f"result: \n{result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == expected


    def test_C2_Error_UT_set_param_target_sheet_name_is_not_exists(self, excel_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C2
        - テスト区分: 異常系/UT
        - テストシナリオ: パラメータ target_sheet_nameに存在しないSheet名を設定, None戻り
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        logger.info(f"param set target_sheet_name is not exists name")
        expected = None
        result = import_excel_onesheet_to_dataframe(
            excel_resource_001,
            'Sheet9999999999999999999999',
            skiprows=0,
            usecols=[0, 3],
            )
        logger.info(f"result: \n{result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == expected



class Test_import_excel_sheets_to_dataframe:
    """import_excel_sheets_to_dataframeのテスト全体をまとめたClass

    【C0】
        複数のシートに対してDataFrameへの取り込みができる,関数に渡される引数file_pathが存在する、かつ読み込み権限がある場合
        関数に渡される引数file_pathがPathObject出ない場合、Noneが返却される。
        関数に渡される引数file_pathが存在しない場合、Noneが返却される。
        関数に渡される引数file_pathが存在するが、読み込み権限がない場合、Noneが返却される。
        関数に渡される引数use_colsを指定せずデフォルト値のまま
        関数に渡される引数use_colsをint型でないlistを設定する
        pd.Excel処理での例外発生、Mock
        parse処理での例外発生、Mock

    【C1】
        関数に渡される引数exclustionをNone指定する

    【C2】
        exclutionを指定して該当シートのデータは取り込まれていないことを確認する
        exclutionに全てのシートを指定して取り込まれていないことを確認する
        1シートだけの場合,かつExclution指定なし
        レイアウトの異なるSheetに対して指定列をCum取り込み 

    """

    def test_C0_Normal_UT_set_param_usecols_is_int_list(self, excel_resource_002, excel_result_003):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: use_colsを正しく指定してデータ取り込み、exclusion設定なし
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        logger.info(f"param set use_cols to Non int list")
        expected = excel_result_003
        result = import_excel_sheets_to_dataframe(
            excel_resource_002,
            skiprows=0,
            usecols=[0, 1],
            )
        logger.info(f"expected: \n{tb(expected, headers='keys')}")
        logger.info(f"result: \n{tb(result, headers='keys')}")

        # assert
        assert type(result) == pd.DataFrame
        logger.info(f"expected/result 一致確認(Noneが一致): {assert_frame_equal(expected, result)}")


    def test_C1_Error_UT_path_is_not_Path_instance(self, excel_resource_002, excel_result_003):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: Pathインスタンス以外を渡す,None戻り確認
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_excel_sheets_to_dataframe(
            "AAAAAAAAAAAAA",
            skiprows=0,
            usecols=[0, 1],
            )
        logger.info(f"result: \n{result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == None


    def test_C1_Error_UT_path_is_not_exists_Path(self, excel_resource_002, excel_result_003):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: ファイルが存在するがファイルに読み込み権限がない
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        expected = None
        excel_resource_002.chmod(0o755)
        result = import_excel_sheets_to_dataframe(
            Path("AAAAAAAAAAAAA"),
            skiprows=0,
            usecols=[0, 1],
            )
        logger.info(f"result: \n{result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == expected


    def test_C1_Error_UT_file_exitsts_with_no_write_permission(self, excel_resource_002, excel_result_003):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: ファイルが存在するがファイルに読み込み権限がない
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        excel_resource_002.chmod(0o111)
        logger.info(f"target_file has write permission: {os.access(excel_resource_002, os.R_OK)}")
        expected = None
        excel_resource_002.chmod(0o755)
        result = import_excel_sheets_to_dataframe(
            "AAAAAAAAAAAAA",
            skiprows=0,
            usecols=[0, 1],
            )
        logger.info(f"result: \n{result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == expected


    def test_C1_Error_UT_set_param_use_cols_None(self, excel_resource_002, excel_result_003):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: パラメータ use_colsにNoneをセット（デフォルト）、None戻り
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        logger.info(f"param set use_cols to None")
        expected = None
        result = import_excel_sheets_to_dataframe(
            excel_resource_002,
            skiprows=0,
            )
        logger.info(f"expected: \n{expected}")
        logger.info(f"result: \n{result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == expected


    def test_C1_Error_UT_set_param_use_cols_is_not_int_list(self, excel_resource_002, excel_result_003):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: パラメータ use_colsにint要素以外のlistを設定、None戻り
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        logger.info(f"param set use_cols to Non int list")
        expected = None
        result = import_excel_sheets_to_dataframe(
            excel_resource_002,
            skiprows=0,
            usecols=["A", "C"],
            )
        logger.info(f"result: \n{result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == expected


    def test_C0_Error_UT_raise_pd_Excel_exception_by_mock(self, mocker, excel_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: パラメータ mockによりException発生させる, 戻りはNone
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        logger.info(f"by Mock except Exception")

        # mockerにて例外発生させる
        mocker.patch.object(pd, "ExcelFile", side_effect=Exception)

        expected = None
        result = import_excel_sheets_to_dataframe(
            excel_resource_002,
            skiprows=0,
            usecols=[0, 3],
            )
        logger.info(f"result: \n{result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == expected


    def test_C0_Error_UT_raise_parse_exception_by_mock(self, mocker, excel_resource_002, excel_result_003):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: パラメータ mockによりException発生させる, 戻りはNone
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        logger.info(f"by Mock except Exception")

        # mockerにて例外発生させる
        ## Pathオブジェクトのunlinkを置き換えるという考え方をする。
        ## Path.unlinkを置き換える、という扱いではないので留意。
        mocker.patch.object(pd.ExcelFile, "parse", side_effect=Exception)

        expected = None
        result = import_excel_sheets_to_dataframe(
            excel_resource_002,
            skiprows=0,
            usecols=[0, 3],
            )
        logger.info(f"result: \n{result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == expected


    def test_C1_Normal_UT_set_exclution_None(self, excel_resource_002, excel_result_003):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 正常系/UT
        - テストシナリオ: exclutionにNoneを指定
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        logger.info(f"param set exclution Sheet3")
        expected = excel_result_003
        result = import_excel_sheets_to_dataframe(
            excel_resource_002,
            skiprows=0,
            exclusion_sheet_names=None,
            usecols=[0, 1],
            )
        logger.info(f"expected: \n{tb(expected, headers='keys')}")
        logger.info(f"result: \n{tb(result, headers='keys')}")

        # assert
        assert type(result) == pd.DataFrame
        logger.info(f"expected/result 一致確認(Noneが一致): {assert_frame_equal(expected, result)}")


    def test_C2_Normal_UT_set_exclution_sheet_name(self, excel_resource_002, excel_result_004):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: exclutionに存在するSheet3を指定し該当データが取り込まれていないことを確認する
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        logger.info(f"param set exclution Sheet3")
        expected = excel_result_004
        result = import_excel_sheets_to_dataframe(
            excel_resource_002,
            skiprows=0,
            exclusion_sheet_names=['Sheet3'],
            usecols=[0, 1],
            )
        logger.info(f"expected: \n{tb(expected, headers='keys')}")
        logger.info(f"result: \n{tb(result, headers='keys')}")

        # assert
        assert type(result) == pd.DataFrame
        logger.info(f"expected/result 一致確認(Noneが一致): {assert_frame_equal(expected, result)}")


    def test_C2_Normal_UT_set_exclution_all_sheet_name(self, excel_resource_002, excel_result_004):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: exclutionに全シート名を指定し該当データが取り込まれていないことを確認する
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        logger.info(f"param set exclution Sheet3")
        expected = pd.DataFrame(index=[])
        result = import_excel_sheets_to_dataframe(
            excel_resource_002,
            skiprows=0,
            exclusion_sheet_names=['Sheet1', 'Sheet2', 'Sheet3'],
            usecols=[0, 1],
            )
        logger.info(f"expected: \n{tb(expected, headers='keys')}")
        logger.info(f"result: \n{tb(result, headers='keys')}")

        # assert
        assert type(result) == pd.DataFrame
        #logger.info(f"expected/result 一致確認(Noneが一致): {assert_frame_equal(expected, result)}")
        assert list(result) == list(expected)



    def test_C2_Normal_UT_one_Sheet(self, excel_resource_003, excel_result_005):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: データは１シートのみ
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        logger.info(f"param set exclution Sheet3")
        expected = excel_result_005
        result = import_excel_sheets_to_dataframe(
            excel_resource_003,
            skiprows=0,
            exclusion_sheet_names=None,
            usecols=[0, 1],
            )
        logger.info(f"expected: \n{tb(expected, headers='keys')}")
        logger.info(f"result: \n{tb(result, headers='keys')}")

        # assert
        assert type(result) == pd.DataFrame
        logger.info(f"expected/result 一致確認(Noneが一致): {assert_frame_equal(expected, result)}")


    def test_C2_Normal_UT_one_Sheet(self, excel_resource_004, excel_result_006):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: Sheetのレイアウトが異なる
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        logger.info(f"param set layout is differ")
        expected = excel_result_006
        result = import_excel_sheets_to_dataframe(
            excel_resource_004,
            skiprows=0,
            exclusion_sheet_names=None,
            usecols=[0, 1],
            )
        logger.info(f"expected: \n{tb(expected, headers='keys')}")
        logger.info(f"result: \n{tb(result, headers='keys')}")

        # assert
        assert type(result) == pd.DataFrame
        logger.info(f"expected/result 一致確認(Noneが一致): {assert_frame_equal(expected, result)}")