# library
import csv
import dateutil
import inspect
import os
import pandas as pd
import pytest
import pytz
import re
import shutil
import sys

from datetime import datetime
from datetime import timedelta
from datetime import timezone
from dateutil.parser import parse
from dateutil import tz
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


# tz生成
UTC = tz.tzutc()

#######################################################
# テスト対象ライブラリパス追加/ロード
#######################################################
TARGET_PREFIX = Path(__file__).parent.parent.parent / 'src'
TARGET_PREFIX_LIB = TARGET_PREFIX / 'lib'
sys.path.append(str(TARGET_PREFIX_LIB))
from UtilsDateHelper import parse_date_string
from UtilsDateHelper import convert_utc_with_timezone_to_jst
from UtilsDateHelper import convert_utc_with_no_timezone_to_jst
from UtilsDateHelper import convert_unixtime_to_jst

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

# tz生成
#UTC = tz.tzutc()
#JST = tz.gettz('Azia/Tokyo')

############################################
# Helper 関数
############################################


############################################
# fixture
############################################


###########################################
# テスト実施
############################################
# Important! C0, C1, C2観点でテスト範囲をカバーすること
# pytest -lsv xxxxxx

class Test_parse_date_string:
    """parse_date_string テスト全体をまとめたClass

    C0: 命令カバレッジ
        日付文字列をdatetimeに変換する(TZなし、あり)
        入力がstrでない、Noneが返る
        parse処理で例外発生、mockerで対応

    C1: 分岐カバレッジ
    C2: 条件カバレッジ
        -

    """

    def test_C0_Normal_UT_no_timezone_UTC_format_date(self):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: 正常系:timezoneを持たないUTC文字列が渡されるが期待値のUTCに変換できる
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        date_string = '2022-01-01 00:00:00'
        expected = datetime(
        year=2022,
        month=1,
        day=1,
        hour=0,
        minute=0,
        )
        result = parse_date_string(date_string)
        logger.info(f"input : {date_string}")
        logger.info(f"expected : {expected}")
        logger.info(f"result : {result}")
        assert result == expected


    def test_C0_Normal_UT_timezone_UTC_format_date(self):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: 正常系:timezoneを持たないUTC文字列が渡されるが期待値のUTCに変換できる
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        date_string = '2022-01-01T00:00:00Z'
        expected = datetime(
        year=2022,
        month=1,
        day=1,
        hour=0,
        minute=0,
        tzinfo=UTC,
        )
        result = parse_date_string(date_string)
        logger.info(f"input : {date_string}")
        logger.info(f"expected : {expected}")
        logger.info(f"result : {result}")
        assert result == expected


    def test_C0_Error_UT_not_UTC_format_date(self):
        """
        テスト定義：
        - テストカテゴリ: C0
        異常系/UT
        - テストシナリオ: 異常系：正しくない時刻文字列が渡される,Noneが返る
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        date_string = '20xx-01-01 00:00:00'
        expected = None
        result = parse_date_string(date_string)
        logger.info(f"input : {date_string}")
        logger.info(f"expected : {expected}")
        logger.info(f"result : {result}")
        assert result == expected


    def test_C0_Error_UT_not_str(self):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: 異常系：文字列以外を渡す、Noneが返る
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        date_string = Path('.')
        expected = None
        result = parse_date_string(date_string)
        logger.info(f"input : {date_string}")
        logger.info(f"expected : {expected}")
        logger.info(f"result : {result}")
        assert result == expected

    def test_C0_Error_UT_raise_parse_exception_by_mock(self, mocker):
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
        mocker.patch.object(dateutil.parser, "parse", side_effect=Exception)

        date_string = '2022-01-01T00:00:00Z'
        expected = None
        result = parse_date_string(date_string)
        logger.info(f"result: \n{result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == expected



class Test_convert_utc_with_timezone_to_jst:
    """convert_utc_with_timezone_to_jst テスト全体をまとめたClass

    C0: 命令カバレッジ
        TZ持ちのUTC文字列をJST datetimeに変換する,想定値と比較
        TZなしのUTC文字列をJST datetimeに変換する,想定値と比較
        正しくないUTC文字列を渡す、Noneを返す
        与えた文字列がstrでない,Noneが返る

    C1: 分岐カバレッジ
    C2: 条件カバレッジ
        -

    """

    def test_C0_Normal_UT_UTC_format_data(self):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: 正常系：timezoneを持つUTC文字列が渡され、期待値のJSTに変換できる
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        date_string = '2022-01-01T00:00:00Z'
        expected = datetime(
        year=2022,
        month=1,
        day=1,
        hour=9,
        minute=0,
        tzinfo=timezone(timedelta(seconds=32400), 'JST')
        )
        result = convert_utc_with_timezone_to_jst(date_string)
        logger.info(f"input : {date_string}")
        logger.info(f"expected : {expected}")
        logger.info(f"result : {result}")
        assert result == expected


    def test_C0_Normal_UT_no_timezone_UTC_format_date(self):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: 正常系：timezoneを持たないUTC文字列が渡されるが期待値のJSTに変換できる
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        date_string = '2022-01-01 00:00:00'
        expected = datetime(
        year=2022,
        month=1,
        day=1,
        hour=9,
        minute=0,
        tzinfo=timezone(timedelta(seconds=32400), 'JST')
        )
        result = convert_utc_with_timezone_to_jst(date_string)
        logger.info(f"input : {date_string}")
        logger.info(f"expected : {expected}")
        logger.info(f"result : {result}")
        assert result == expected


    def test_C0_Error_UT_not_UTC_format_date(self):
        """
        テスト定義：
        - テストカテゴリ: C0
        異常系/UT
        - テストシナリオ: 異常系：正しくないUTC文字列が渡される,Noneが返る
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        date_string = '20xx-01-01 00:00:00'
        expected = None
        result = convert_utc_with_timezone_to_jst(date_string)
        logger.info(f"input : {date_string}")
        logger.info(f"expected : {expected}")
        logger.info(f"result : {result}")
        assert result == expected


    def test_C0_Error_UT_not_str(self):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: 異常系：文字列以外を渡す、Noneが返る
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        date_string = Path('.')
        expected = None
        result = convert_utc_with_timezone_to_jst(date_string)
        logger.info(f"input : {date_string}")
        logger.info(f"expected : {expected}")
        logger.info(f"result : {result}")
        assert result == expected


class Test_convert_utc_without_timezone_to_jst:
    """convert_utc_with_timezone_to_jst テスト全体をまとめたClass

    C0: 命令カバレッジ
        TZ持ちのUTC文字列をJST datetimeに変換する,想定値と比較
        TZなしのUTC文字列をJST datetimeに変換する,想定値と比較
        正しくないUTC文字列を渡す、Noneを返す
        与えた文字列がstrでない,Noneが返る

    C1: 分岐カバレッジ
    C2: 条件カバレッジ
        -

    """
    def test_C0_Normal_UT_UTC_format_data(self):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: 正常系：timezoneを持つUTC文字列が渡され、期待値のJSTに変換できる
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        date_string = '2022-01-01T00:00:00Z'
        expected = datetime(
        year=2022,
        month=1,
        day=1,
        hour=9,
        minute=0,
        tzinfo=timezone(timedelta(seconds=32400), 'JST')
        )
        result = convert_utc_with_no_timezone_to_jst(date_string)
        logger.info(f"input : {date_string}")
        logger.info(f"expected : {expected}")
        logger.info(f"result : {result}")
        assert result == expected


    def test_C0_Normal_UT_no_timezone_UTC_format_date(self):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: 正常系：timezoneを持たないUTC文字列が渡されるが期待値のJSTに変換できる
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        JST = timezone(timedelta(hours=+9), 'JST')
        date_string = '2022-01-01 00:00:00'
        expected = datetime(
        year=2022,
        month=1,
        day=1,
        hour=0,
        minute=0,
        tzinfo=JST,
        )
        result = convert_utc_with_no_timezone_to_jst(date_string)
        logger.info(f"input : {date_string}")
        logger.info(f"expected : {expected}")
        logger.info(f"result : {result}")
        assert result == expected


    def test_C0_Error_UT_not_UTC_format_date(self):
        """
        テスト定義：
        - テストカテゴリ: C0
        異常系/UT
        - テストシナリオ: 異常系：正しくないUTC文字列が渡される,Noneが返る
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        date_string = '20xx-01-01 00:00:00'
        expected = None
        result = convert_utc_with_no_timezone_to_jst(date_string)
        logger.info(f"input : {date_string}")
        logger.info(f"expected : {expected}")
        logger.info(f"result : {result}")
        assert result == expected


    def test_C0_Error_UT_not_str(self):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: 異常系：文字列以外を渡す、Noneが返る
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        date_string = Path('.')
        expected = None
        result = convert_utc_with_no_timezone_to_jst(date_string)
        logger.info(f"input : {date_string}")


class Test_convert_unixtime_to_jst:
    """convert_unixtime_to_jst テスト全体をまとめたClass

    C0: 命令カバレッジ
        UNIXTIMEをJST datetimeに変換する
        規定でないUNIXTIMEをJST datetimeに変換する,Noneが返る

    C1: 分岐カバレッジ
    C2: 条件カバレッジ

    """
    @pytest.mark.parametrize("unixtime_string_normal, expected_value", [
        ("1631366383", datetime(2021, 9, 11, 22, 19, 43)),
        ("1631366383000", datetime(2021, 9, 11, 22, 19, 43)),
        ("1631366383000000", datetime(2021, 9, 11, 22, 19, 43)),
    ])
    def test_C0_Normal_UT_unixtime_format_data(self, unixtime_string_normal, expected_value):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: 正常系 UNIXTIMEをJSTに変換する、規定のフォーマット 10/13/16桁をparameterで一括実施
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        logger.info(f"input : {unixtime_string_normal}")
        logger.info(f"expected : {expected_value}")
        result =  convert_unixtime_to_jst(unixtime_string_normal)
        assert result == expected_value


    @pytest.mark.parametrize("unixtime_string_error, expected_none", [
        ("163136638", None),
        ("16313663830000", None),
        ("1631366383000000000", None),
        (1234567890, None),
    ])
    def test_C0_Error_UT_unixtime_format_data(self, unixtime_string_error, expected_none):
        """
        テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: 異常系 UNIXTIMEをJSTに変換する、規定のフォーマットではない、parameterで一括実施
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        logger.info(f"input : {unixtime_string_error}")
        logger.info(f"expected : {expected_none}")
        result =  convert_unixtime_to_jst(unixtime_string_error)
        assert result == expected_none