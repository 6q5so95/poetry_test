# library
import pandas as pd
import sys

from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta

from pathlib import Path
from typing import Optional

def calc_timedelta_to_totalseconds(col_start: pd.Series, col_end: pd.Series) -> Optional[pd.Series]:
    """2つのdatetime型のSeries感の差分時間を秒を返す

    Args:
        col_start (pd.Series[datetime]): 評価開始時間
        col_end (pd.Series[datetime]): 評価終了時間

    Returns:
        pd.Series: 差分時間を秒で返す
    """
    try:
        _timedelta: timedelta = col_end - col_start
        #return _timedelta.totalseconds()
        return _timedelta.seconds
    except Exception as e:
        print(f"{e}: 例外が発生しました")
        return None


def add_staticvalue_to_dataframe(df: pd.DataFrame, add_col_name: str, static_value) -> pd.DataFrame:
    """指定した列に固定値を一律設定する

    Args:
        df (pd.DataFrame): 処理対象DataFrame
        add_col_name (str): DataFrameに追加するcol名
        static_value (_type_): DataFrameに追加するcolに設定する固定値

    Returns:
        pd.DataFrame: _description_
    """
    if not isinstance(df, pd.DataFrame):
        print(f"dfがpd.DataFrameではありません {df}")
        return None

    if not isinstance(add_col_name, str):
        print(f"add_col_nameがstrではありません {add_col_name}")
        return None

    try:
        _df = df.copy()
        return _df.assign(add_col_name=static_value).rename(columns={'add_col_name': add_col_name})
    except Exception as e:
        print(f"{e} 例外が発生しました")
    return None


def do_excel_eda(df:pd.DataFrame) -> Optional[pd.DataFrame]:
    """Excelから取り込んだDataFrameからよくある困った文字列を取り除く

    Args:
        df (pd.DataFrame):処理対象のDataFrame

    Returns:
        pd.DataFrame: EDA処置済のDataFrame
    """
    if not isinstance(df, pd.DataFrame):
        print(f"dfにDataFrameが設定されていません {df}")
        return None

    try:
        _df = df.copy()
        # セル内改行文字取り除き（想定外の問題を引き起こす）
        _df = _df.replace({'\n': '', '\r': ''}, regex=True)
        # ダブルクオート取り除き（じゃま）
        _df = _df.replace({r'"': ''}, regex=True)
        return _df
    except Exception as e:
        print(f"{e} 例外が発生しました")
        return None


def create_markdowntable_from_dataframe(df: pd.DataFrame) -> str:
    """DataFrameをMarkdownTable構成にテキスト変換する
    bool属性に対してはOK,Fail（ともに文字列）に変換する
    項目は全て文字列に変換する

    Args:
        df (pd.DataFrame): 変換対象のDataFrame

    Returns:
        str: 変換後のMarkdown構成Table
    """
    if not isinstance(df, pd.DataFrame):
        print(f"dfがDataFrameではありません {df}")
        return None

    try:
        # テーブル構造情報取得
        shape_x, shape_y = df.shape
        issue: str = ''

        # table title column
        for i in range(shape_y):
            issue += '|**' + str(df.columns[i]) + '**'
        issue += '|' + '\n'

        # table title separator
        for i in range(shape_y):
            issue += '|---'
        issue += '|' + '\n'

        # table data
        for i in range(shape_x):
            for j in range(shape_y):
                # 何らかの判定列（True/False）があればOK／Failに置換する
                if df.iloc[:, j].dtypes == "bool":
                    if df.iloc[i, j]:
                        value = "OK"
                    else:
                        value = "Fail"
                else:
                # bool属性以外はstr変換
                    value = str(df.iloc[i, j])
                issue += "|" + value
            issue += "|" + "\n"

        return issue
    except Exception as e:
        print(f"{e} 例外が発生しました")
        return None