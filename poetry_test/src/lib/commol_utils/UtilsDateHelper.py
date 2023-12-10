# library
import sys
import time

from datetime import datetime
from datetime import timedelta
from dateutil import parser
from dateutil import tz
from dateutil.relativedelta import relativedelta
from pprint import pprint
from pytz import timezone
from typing import Optional

# tz生成
UTC = tz.tzutc()
JST = tz.gettz('Azia/Tokyo')

# 関数定義
def parse_date_string(date_string: str) -> Optional[datetime]:
    """文字列→dataframe parse 共通関数

    Args:
        date_string (str): 変換対象文字列

    Returns:
        Optional[datetime]: datetime

    """
    if not isinstance(date_string, str):
        print(f"{date_string}: 入力データがstrではありません")
        return None

    try:
        return parser.parse(date_string)
    except Exception as e:
        print(f"{e}: データ日付変換エラー: {date_string}")
        return None


def convert_utc_with_timezone_to_jst(date_string: str) -> Optional[datetime]:
    """UTC文字列をJSTのdatetimeに変換する

    Args:
        date_string (str): 変換対象文字列 TZなし

    Returns:
        Optional[datetime]: JST変換後のdatetime
    """
    if not isinstance(date_string, str):
        print(f"{date_string}: 入力データがstrではありません")
        return None

    dt = parse_date_string(date_string)
    if dt is None:
        return None

    dt_jst = dt.replace(tzinfo=UTC).astimezone(JST)
    return dt_jst


def convert_utc_with_no_timezone_to_jst(date_string: str) -> Optional[datetime]:
    """UTC文字列をJSTのdatetimeに変換する

    Args:
        date_string (str): 変換対象文字列 TZあり

    Returns:
        Optional[datetime]: JST変換後のdatetime
    """
    if not isinstance(date_string, str):
        print(f"{date_string}: 入力データがstrではありません")
        return None

    dt = parse_date_string(date_string)
    if dt is None:
        return None

    dt_jst = dt.astimezone(UTC).astimezone(JST)
    return dt_jst


def convert_unixtime_to_jst(unixtime_string: str) -> Optional[datetime]:
    """UNIXTIMEをJSTのdatetimeに変換する

    Args:
        unixtime_string (str): unixtime 文字列

    Returns:
        Optional[datetime]: JST変換後のdatetime
    """
    if not isinstance(unixtime_string, str):
        print(f"{unixtime_string}: 入力データがstrではありません")
        return None

    if len(unixtime_string) == 10:
        unixtime = int(unixtime_string)
    elif len(unixtime_string) == 13:
        unixtime = int(unixtime_string) // 1000
    elif len(unixtime_string) == 16:
        unixtime = int(unixtime_string) // 1000000
    else:
        print(f"unixtime_stringは10/13/16桁のいずれかでなければなりません {len(unixtime_string)}桁")
        return None

    dt_utc = datetime.utcfromtimestamp(unixtime)
    dt_jst = dt_utc + timedelta(hours=9)
    return dt_jst