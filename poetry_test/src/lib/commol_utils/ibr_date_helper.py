# library
"""_summary_

_type_: _description_
"""

from datetime import (
    datetime,
    timedelta,
)

from dateutil import (
    parser,
    tz,
)

# TODO ibr loggerライブラリを読みこむ

####################################
# logger
####################################
# TODO ibr logger を導入

####################################
# tz生成
####################################
UTC = tz.tzutc()
JST = tz.gettz('Azia/Tokyo')

####################################
# function
####################################
def parse_date_string(date_string: str) -> datetime|None:
    """文字列→dataframe parse 共通関数

    Args:
    ----
        date_string (str): 変換対象文字列

    Returns:
    -------
        Optional[datetime]: datetime

    """
    if not isinstance(date_string, str):
        # TODO log_msgで差し替え
        print(f"{date_string}: 入力データがstrではありません")
        return None

    try:
        return parser.parse(date_string)
    except Exception as e: # noqa: BLE001 parseエラーでは様々可能性があるため
        # TODO log_msgで差し替え
        print(f"{e}: データ日付変換エラー: {date_string}")
        return None


def convert_utc_with_timezone_to_jst(date_string: str) -> datetime|None:
    """UTC文字列をJSTのdatetimeに変換する

    Args:
    ----
        date_string (str): 変換対象文字列 TZなし

    Returns:
    -------
        Optional[datetime]: JST変換後のdatetime
    """
    if not isinstance(date_string, str):
        # TODO log_msgで差し替え
        print(f"{date_string}: 入力データがstrではありません")
        return None

    dt = parse_date_string(date_string)
    if dt is None:
        return None

    return dt.replace(tzinfo=UTC).astimezone(JST)


def convert_utc_with_no_timezone_to_jst(date_string: str) -> datetime|None:
    """UTC文字列をJSTのdatetimeに変換する

    Args:
    ----
        date_string (str): 変換対象文字列 TZあり

    Returns:
    -------
        Optional[datetime]: JST変換後のdatetime
    """
    if not isinstance(date_string, str):
        # TODO log_msgで差し替え
        print(f"{date_string}: 入力データがstrではありません")
        return None

    dt = parse_date_string(date_string)
    if dt is None:
        return None

    return dt.astimezone(UTC).astimezone(JST)


def convert_unixtime_to_jst(unixtime_string: str) -> datetime|None:
    """UNIXTIMEをJSTのdatetimeに変換する

    Args:
    ----
        unixtime_string (str): unixtime 文字列

    Returns:
    -------
        Optional[datetime]: JST変換後のdatetime
    """
    const_10 = 10
    const_13 = 13
    const_16 = 16
    if not isinstance(unixtime_string, str):
        # TODO log_msgで差し替え
        print(f"{unixtime_string}: 入力データがstrではありません")
        return None

    if len(unixtime_string) == const_10:
        unixtime = int(unixtime_string)
    elif len(unixtime_string) == const_13:
        unixtime = int(unixtime_string) // 1000
    elif len(unixtime_string) == const_16:
        unixtime = int(unixtime_string) // 1000000
    else:
        # TODO log_msgで差し替え
        print(f"unixtime_stringは10/13/16桁のいずれかでなければなりません {len(unixtime_string)}桁")
        return None

    dt_utc = datetime.fromtimestamp(unixtime, tz=UTC)
    return dt_utc + timedelta(hours=9)
