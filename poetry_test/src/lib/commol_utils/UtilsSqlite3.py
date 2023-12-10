# library
from pathlib import Path
from pprint import pprint
from typing import Optional

import csv
import numpy as np
import os
import pandas as pd
import re
import sqlite3
import sys
import yaml

class Sqlite3Manager:
    """dbへのパスを指定してインスタンス生成する

    """
    def __init__(self, db_path: str):
        self.db_path = db_path


    def load_dataframe_to_sqlite3_replace(self, df: pd.DataFrame, tablename: str) -> bool:
        """dataframeを指定したテーブルへreplaceロードする

        Args:
            tablename (str): テーブル名
            df (pd.DataFrame): ロードするdataframe

        Returns:
            bool:
        """
        if not isinstance(df, pd.DataFrame):
            return False

        if not isinstance(tablename ,str):
            return False

        _flg:bool = False
        try:
            with sqlite3.connect(self.db_path) as conn:
                df.to_sql(tablename, conn, if_exists='replace')
                _flg = True
        except (sqlite3.Error, Exception) as e:
            print(f"{e}: sqlite3エラー、その他例外発生")
            return False

        return _flg


    def load_dataframe_to_sqlite3_append(self, df:pd.DataFrame, tablename: str) -> bool:
        """dataframeを指定したテーブルへappendロードする

        Args:
            tablename (str): テーブル名
            df (pd.DataFrame): ロードするdataframe

        Returns:
            bool:
        """
        if not isinstance(df, pd.DataFrame):
            return False

        if not isinstance(tablename ,str):
            return False

        _flg:bool = False
        try:
            with sqlite3.connect(self.db_path) as conn:
                df.to_sql(tablename, conn, if_exists='append')
                _flg = True
        except (sqlite3.Error, Exception) as e:
            print(f"{e}: sqlite3エラー、その他例外発生")
            return False

        return _flg


    def execute_sql_sqlite3(self, sqlText: str) -> bool:
        """指定してたSQLを実行する

        Args:
            sqlText (str): 実行するSQL

        Returns:
            bool:
        """

        if not isinstance(sqlText ,str):
            return False

        if not sqlText:
            return False

        _flg = False
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(sqlText)
                conn.commit()
                _flg = True
        except (sqlite3.Error, Exception) as e:
            print(f"{e}: sqlite3エラー、その他例外発生")
            return False

        return _flg


    def fetch_sql_sqlite3(self, sqlText: str) -> Optional[list]:
        """指定してたSQLを実行し行レコード単位にlistに格納する

        Args:
            sqlText (str): 実行するSQL

        Returns:
            list: SQL実行結果を格納したlist
        """
        if not isinstance(sqlText ,str):
            return False

        if not sqlText:
            return False

        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute(sqlText)
                rows = cur.fetchall()
                _flg = True
        except (sqlite3.Error, Exception) as e:
            print(f"{e}: sqlite3エラー、その他例外発生")
            return False

        return rows