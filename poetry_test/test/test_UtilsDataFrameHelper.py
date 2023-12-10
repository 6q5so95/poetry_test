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
from UtilsDataFrameHelper import calc_timedelta_to_totalseconds
from UtilsDataFrameHelper import add_staticvalue_to_dataframe
from UtilsDataFrameHelper import do_excel_eda
from UtilsDataFrameHelper import create_markdowntable_from_dataframe

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
@pytest.fixture(scope='session')
def datetime_data_001():
    col_start = pd.to_datetime(['2023-05-01 00:00:00','2023-05-01 00:00:00', '2023-05-01 00:00:00'])
    col_end =   pd.to_datetime(['2023-05-01 00:00:10','2023-05-01 00:01:00', '2023-05-01 01:00:00'])
    return col_start, col_end


@pytest.fixture(scope='session')
def datetime_data_002():
    col_start = pd.to_datetime(['2023-05-01 00:00:00','2023-05-01 00:00:00', '2023-05-01 00:00:00', '2023-05-01 00:00:00'])
    col_end =   pd.to_datetime(['2023-05-01 00:00:00','2023-05-01 00:00:01', '2025-05-01 00:00:00', '2099-05-01 00:00:00'])
    return col_start, col_end


@pytest.fixture(scope='function')
def datetime_resource_001(datetime_data_001)-> Union[pd.Series, pd.Series]:
    # テストデータ出力先定義
    col_start, col_end = datetime_data_001

    # setup
    logger.info(f"setup")

    # Exectute Test
    yield col_start, col_end

    # tear_down
    logger.info(f"tear down")


@pytest.fixture(scope='function')
def datetime_resource_002(datetime_data_002)-> pd.DataFrame:
    # テストデータ出力先定義
    col_start, col_end = datetime_data_002

    # setup
    logger.info(f"setup")

    # Exectute Test
    yield col_start, col_end

    # tear_down
    logger.info(f"tear down")


@pytest.fixture(scope='function')
def dataframe_resource_001()-> pd.DataFrame:
    # 検証用DataFrame生成
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': ['a', 'b', 'c']
    })

    # setup
    logger.info(f"setup")

    # Exectute Test
    yield df

    # tear_down
    logger.info(f"tear down")


@pytest.fixture(scope='function')
def dataframe_resource_002()-> pd.DataFrame:
    # 検証用DataFrame生成
    df = pd.DataFrame({
        'col1': ['a', 'b\n', 'c\r\n', 'd', 'e"f']})

    # setup
    logger.info(f"setup")

    # Exectute Test
    yield df

    # tear_down
    logger.info(f"tear down")

@pytest.fixture(scope='function')
def dataframe_resource_003()-> pd.DataFrame:
    # 検証用DataFrame生成
    df = pd.DataFrame(
        {"col1": [1, 2], "col2": [True, False]}
        )

    # setup
    logger.info(f"setup")

    # Exectute Test
    yield df

    # tear_down
    logger.info(f"tear down")


@pytest.fixture(scope='function')
def dataframe_resource_004()-> pd.DataFrame:
    # 検証用DataFrame生成
    df = pd.DataFrame(
        {"col1": [True, False], "col2": [True, True]}
    )

    # setup
    logger.info(f"setup")

    # Exectute Test
    yield df

    # tear_down
    logger.info(f"tear down")


###########################################
# テスト実施
############################################
# Important! C0, C1, C2観点でテスト範囲をカバーすること
# pytest -lsv xxxxxx

class Test_calc_timedelta_to_totalseconds:
    """calc_timedelta_to_totalsecondsテスト全体をまとめたClass

    C0: 命令カバレッジ
        有効な入力に対して正しい出力が返されることを確認する
        異常系の入力に対して例外が発生する

    C1: 分岐カバレッジ
        引数にともにNoneを設定する
        引数の片方にNoneを設定する（Start)
        引数の片方にNoneを設定する（End)
        引数にともに空のDataFrameを設定する
        引数の片方に空のDataFrameを設定する（Start)
        引数の片方に空のDataFrameを設定する（End)

    C2: 条件カバレッジ
        end > start
        極端に離れた2つの時間
        極端に近い2つの時間

    """

    def test_C0_Normal_UT_set_10s_60s_3600s_timediff_records(self, datetime_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: datetime型データを格納したSeriesをもとに差分時間を取得 10s, 60s, 3600s
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        col_start, col_end = datetime_resource_001
        result = calc_timedelta_to_totalseconds(col_start, col_end)
        expected = pd.Index([10, 60, 3600])
        logger.info(f"result : {result}")
        logger.info(f"result: {result}")

        # assert
        assert str(type(result)) == "<class 'pandas.core.indexes.numeric.Int64Index'>"
        assert result[0]== expected[0]
        assert result[1]== expected[1]
        assert result[2]== expected[2]


    def test_C0_Error_UT_set_both_non_numeric_raise_exception(self, datetime_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: 減算が不可能な値を設定、Exception発生, Noneが戻る
            引き算でのException発生が困難なので異例値によりException発生させている
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        col_start, col_end = 'AAAAAAAAAA' , 'BBBBBBBBBBBBB'
        result = calc_timedelta_to_totalseconds(col_start, col_end)
        logger.info(f"result: {result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"


    def test_C1_Error_UT_set_both_None(self, datetime_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: ともにNoneを設定
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        col_start, col_end = None, None
        result = calc_timedelta_to_totalseconds(col_start, col_end)
        logger.info(f"result: {result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"


    def test_C1_Error_UT_set_start_None(self, datetime_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: StartにNoneを設定
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        col_start, col_end = datetime_resource_001
        col_start = None
        result = calc_timedelta_to_totalseconds(col_start, col_end)
        logger.info(f"result: {result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"


    def test_C1_Error_UT_set_end_None(self, datetime_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: EndにNoneを設定
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        col_start, col_end = datetime_resource_001
        col_end = None
        result = calc_timedelta_to_totalseconds(col_start, col_end)
        logger.info(f"result: {result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"


    def test_C1_Error_UT_set_both_empty_list(self, datetime_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: []を与える start, end
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        col_start, col_end = datetime_resource_001
        col_start = []
        col_end = []
        result = calc_timedelta_to_totalseconds(col_start, col_end)
        logger.info(f"result: {result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"


    def test_C1_Error_UT_set_start_empty_list(self, datetime_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: 片方に[]を与える start
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        col_start, col_end = datetime_resource_001
        col_start = []
        result = calc_timedelta_to_totalseconds(col_start, col_end)
        logger.info(f"result: {result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"


    def test_C1_Error_UT_set_end_empty_list(self, datetime_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: 片方に[]を与える end
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        col_start, col_end = datetime_resource_001
        col_end = []
        result = calc_timedelta_to_totalseconds(col_start, col_end)
        logger.info(f"result: {result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"


    def test_C2_Error_UT_set_bigger_than_start(self, datetime_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: start > end を与える
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        col_end, col_start = datetime_resource_001
        result = calc_timedelta_to_totalseconds(col_start, col_end)
        expected = pd.Index([86390, 86340, 82800])
        logger.info(f"expected: {result}")
        logger.info(f"expected: {expected}")

        # assert
        assert str(type(result)) == "<class 'pandas.core.indexes.numeric.Int64Index'>"
        assert result[0]== expected[0]
        assert result[1]== expected[1]
        assert result[2]== expected[2]


    def test_C2_Normal_UT_set_short_range_and_long_range(self, datetime_resource_002):
        """
        テスト定義：
        - テストカテゴリ: C2
        - テスト区分: 正常系/UT
        - テストシナリオ: 差がわずか、大きく離れたを設定
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        col_start, col_end = datetime_resource_002
        result = calc_timedelta_to_totalseconds(col_start, col_end)
        expected = pd.Index([0, 1, 0, 0])
        logger.info(f"expected: {expected}")
        logger.info(f"result: {result}")

        # assert
        assert str(type(expected)) == "<class 'pandas.core.indexes.numeric.Int64Index'>"
        assert result[0]== expected[0]
        assert result[1]== expected[1]
        assert result[2]== expected[2]
        assert result[3]== expected[3]


class Test_add_staticvalue_to_dataframe:
    """calc_timedelta_to_totalsecondsテスト全体をまとめたClass

    C0: 命令カバレッジ
        有効な入力に対して正しい出力が返されることを確認する
        入力に対して元のDataFrameに影響が出ていないことを示す
        DataFrame以外の入力に対して例外発生、Noneが返る
        カラム名がstrでない, Noneが返る

    C1: 分岐カバレッジ
        dataframeにNone指定, Noneが返る
        col_nameにNone指定, Noneが返る
        static_valueにNone指定, Noneが返る

    C2: 条件カバレッジ
        入力DataFrameが空でも関数が正しく挙動することを示す

    """

    def test_C0_Normal_UT_no_effect_to_input_dataframe_and_return_valid_dataframe(self, dataframe_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: 入力DataFrameに対して処理前後で影響を与えていない,指定した列名で一律指定値が設定されている
            C列に一律0を設定
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        df_org = dataframe_resource_001
        result = add_staticvalue_to_dataframe(df_org, 'C', 0)
        expected = pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c'], 'C': [0, 0, 0]})
        logger.info(f"result: \n{tb(result, headers='keys')}")
        logger.info(f"expected: \n{tb(expected, headers='keys')}")

        # assert
        assert str(type(result)) == "<class 'pandas.core.frame.DataFrame'>"
        assert_frame_equal(df_org, dataframe_resource_001)


    def test_C0_Error_UT_input_to_non_dataframe(self, dataframe_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: dataframe以外の属性をインプットとして渡す、例外発生、Noneが返る 
            C列に一律0を設定
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        df_org = dataframe_resource_001
        result = add_staticvalue_to_dataframe('AAAAAAAAAAAAAAAAA', 'C', 0)
        expected = pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c'], 'C': [0, 0, 0]})
        logger.info(f"result: \n{tb(result, headers='keys')}")
        logger.info(f"expected: \n{tb(expected, headers='keys')}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"


    def test_C0_Error_UT_set_df_non_dataframe(self, dataframe_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: 入力DataFrameに対して処理前後で影響を与えていない,指定した列名で一律指定値が設定されている
            C列に一律0を設定
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        df_org = "AAAAAAAAAAAAAAAAAAAAA"
        result = add_staticvalue_to_dataframe(df_org, 'C', 0)
        expected = None
        logger.info(f"result: \n{tb(result, headers='keys')}")
        logger.info(f"expected: \n{tb(expected, headers='keys')}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"


    def test_C0_Error_UT_set_add_col_name_to_non_str(self, dataframe_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: col_nameにstrを設定していない
            C列に一律0を設定
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        df_org = dataframe_resource_001
        result = add_staticvalue_to_dataframe(df_org, 1111111111111111111, 0)
        expected = None
        logger.info(f"result: \n{tb(result, headers='keys')}")
        logger.info(f"expected: \n{tb(expected, headers='keys')}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"


    def test_C1_Error_UT_set_col_name_to_none(self, dataframe_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: col_nameにNoneを設定
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        df_org = dataframe_resource_001
        result = add_staticvalue_to_dataframe(df_org, None, 0)
        expected = None
        logger.info(f"result: \n{tb(result, headers='keys')}")
        logger.info(f"expected: \n{tb(expected, headers='keys')}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"


    def test_C1_Normal_UT_set_static_value_to_none(self, dataframe_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 正常系/UT
        - テストシナリオ: static_valueにNoneを設定, None値がカラムに設定される
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        df_org = dataframe_resource_001
        result = add_staticvalue_to_dataframe(df_org, "cols", None)
        expected = pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c'], 'cols': [None, None ,None ]})
        logger.info(f"result: \n{tb(result, headers='keys')}")
        logger.info(f"expected: \n{tb(expected, headers='keys')}")

        # assert
        assert str(type(result)) == "<class 'pandas.core.frame.DataFrame'>"
        assert_frame_equal(df_org, dataframe_resource_001)


    def test_C2_Normal_UT_input_to_empty_dataframe(self, dataframe_resource_001):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: 空のDataFrameを渡す、指定カラムをcolumnsに持つ空のDataFrameが生成される
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        df_org = dataframe_resource_001
        result = add_staticvalue_to_dataframe(pd.DataFrame(), 'C', 0)
        expected = pd.DataFrame(columns=['C'])
        logger.info(f"result: \n{tb(result, headers='keys')}")
        logger.info(f"expected: \n{tb(expected, headers='keys')}")

        # assert
        assert str(type(result)) == "<class 'pandas.core.frame.DataFrame'>"
        assert_frame_equal(df_org, dataframe_resource_001)
        assert result.columns == expected.columns
        assert len(result) == len(expected)


class Test_do_excel_eda:
    """do_excel_eda テスト全体をまとめたClass

    C0: 命令カバレッジ
        入力に対して元のDataFrameに影響が出ていないことを示す
        有効な入力に対して正しい出力が返されることを確認する
        DataFrame以外の入力に対して、Noneが返る
        mockerを用いてdf.replace()で例外発生させる

    C1: 分岐カバレッジ

    C2: 条件カバレッジ
        入力DataFrameが空でも関数が正しく挙動することを示す
        #\n及び\rのバリエーション組み合わせ検証 -> C0で実施済

    """
    def test_C0_Normal_UT_no_effect_to_input_dataframe_and_return_valid_dataframe(self, dataframe_resource_002):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: 入力DataFrameに対して処理前後で影響を与えていない, 指定文字が置換されている
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        df_org = dataframe_resource_002
        result = do_excel_eda(df_org)
        expected = pd.DataFrame({ 'col1': ['a', 'b', 'c', 'd', 'ef'] })
        logger.info(f"result: \n{tb(result, headers='keys')}")
        logger.info(f"expected: \n{tb(expected, headers='keys')}")

        # assert
        assert str(type(result)) == "<class 'pandas.core.frame.DataFrame'>"
        assert result.equals(expected)
        assert_frame_equal(df_org, dataframe_resource_002)


    def test_C0_Error_UT_input_to_non_dataframe(self, dataframe_resource_002):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: dfにpd.DataFrame以外を渡す
            C列に一律0を設定
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        df_org = dataframe_resource_002
        result = do_excel_eda('AAAAAAAAAAAAAAAAA')
        expected = None

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == expected


    def test_C0_Error_UT_raise_exception_replace_by_moker(self, mocker, dataframe_resource_002):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: 例外発生させる、Noneが戻る、mockerによる
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        # mockerにて例外発生させる
        ## pd.DataFrameオブジェクトのreplaceを置き換えるという考え方をする。
        mocker.patch.object(pd.DataFrame, "replace", side_effect=Exception)

        df_org = dataframe_resource_002
        result = do_excel_eda(df_org)
        expected = None

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == expected
        assert_frame_equal(df_org, dataframe_resource_002)


    def test_C2_Normal_UT_input_to_empty_dataframe(self, dataframe_resource_002):
        """
        テスト定義：
        - テストカテゴリ: C2
        - テスト区分: 正常系/UT
        - テストシナリオ: 空のDataFrameを渡す、指定カラムをcolumnsに持つ空のDataFrameが生成される
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        df_org = dataframe_resource_002
        result = do_excel_eda(pd.DataFrame())
        expected = pd.DataFrame()
        logger.info(f"result: \n{tb(result, headers='keys')}")
        logger.info(f"expected: \n{tb(expected, headers='keys')}")

        # assert
        assert str(type(result)) == "<class 'pandas.core.frame.DataFrame'>"
        assert_frame_equal(result, expected)
        assert_frame_equal(df_org, dataframe_resource_002)


class Test_create_markdowntable_from_dataframe:
    """do_excel_eda テスト全体をまとめたClass

    C0: 命令カバレッジ
        関数に渡されたDataFrameに対して正しくMarkdownテーブルが出力されることを確認する
        dfがDataFrame以外の場合にNoneを返す
        mokerを用いてdf.shape処理で例外発生させる, Noneが返る

    C1: 分岐カバレッジ

    C2: 条件カバレッジ
        DataFrameの列数が0の場合に適切なエラーメッセージを返すことを確認する
        DataFrameにbool属性が含まれている場合、OK/Failに変換されることを確認する

    """

    def test_C0_Normal_UT_no_effect_to_input_dataframe_and_return_valid_table(self, dataframe_resource_003):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: 入力DataFrameに対して処理前後で影響を与えていない, 指定文字が置換されている
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        df_org = dataframe_resource_003
        result = create_markdowntable_from_dataframe(df_org)
        expected = "|**col1**|**col2**|\n|---|---|\n|1|OK|\n|2|Fail|\n"
        logger.info(f"result: \n{tb(result, headers='keys')}")
        logger.info(f"expected: \n{tb(expected, headers='keys')}")

        # assert
        assert str(type(result)) == "<class 'str'>"
        assert result == expected
        assert_frame_equal(df_org, dataframe_resource_003)


    def test_C0_Error_UT_input_to_non_dataframe(self, dataframe_resource_003):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: dataframe以外の属性をインプットとして渡す、例外発生、Noneが返る
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        df_org = dataframe_resource_003
        result = create_markdowntable_from_dataframe('AAAAAAAAAAAAAAAAA')
        expected = "|**col1**|**col2**|\n|---|---|\n|1|OK|\n|2|Fail|\n"
        logger.info(f"result: \n{tb(result, headers='keys')}")
        logger.info(f"expected: \n{tb(expected, headers='keys')}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert_frame_equal(df_org, dataframe_resource_003)


    def test_C0_Error_UT_raise_exception_pd_shape_by_moker(self, mocker, dataframe_resource_003):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: 例外を発生させる、Noneが返る mockerによる
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        # mockerにて例外発生させる
        ## pd.DataFrameオブジェクトのshapeを置き換えるという考え方をする。
        mocker.patch.object(pd.DataFrame, "shape", side_effect=Exception)

        df_org = dataframe_resource_003
        result = create_markdowntable_from_dataframe(df_org)
        expected = None

        # assert
        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == expected
        assert_frame_equal(df_org, dataframe_resource_003)


    def test_C2_Normal_UT_input_to_empty_dataframe(self, dataframe_resource_003):
        """
        テスト定義：
        - テストカテゴリ: C2
        - テスト区分: 正常系/UT
        - テストシナリオ: 空のDataFrameを渡す、空文字列向けのMarkdownテーブルが返る
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        df_org = dataframe_resource_003
        result = create_markdowntable_from_dataframe(pd.DataFrame())
        expected = "|\n|\n"
        logger.info(f"result: \n{tb(result, headers='keys')}")
        logger.info(f"expected: \n{tb(expected, headers='keys')}")

        # assert
        assert str(type(result)) == "<class 'str'>"
        assert result == expected
        assert_frame_equal(df_org, dataframe_resource_003)


    def test_C2_Normal_UT_no_effect_to_input_dataframe_and_return_valid_str_with_bool_value(self, dataframe_resource_004):
        """
        テスト定義：
        - テストカテゴリ: C2
        - テスト区分: 正常系/UT
        - テストシナリオ: 入力DataFrameに対して処理前後で影響を与えていない, 指定文字が置換されている bool
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        df_org = dataframe_resource_004
        result = create_markdowntable_from_dataframe(df_org)
        expected = "|**col1**|**col2**|\n|---|---|\n|OK|OK|\n|Fail|OK|\n"
        logger.info(f"result: \n{tb(result, headers='keys')}")
        logger.info(f"expected: \n{tb(expected, headers='keys')}")

        # assert
        assert str(type(result)) == "<class 'str'>"
        assert result == expected
        assert_frame_equal(df_org, dataframe_resource_004)