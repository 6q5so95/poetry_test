"""_summary_

Returns
-------
    _type_: _description_

"""
# library
import csv
from pathlib import Path
from typing import Optional

import pandas as pd

######################################################
# 同一階層ライブラリ
######################################################
from UtilsDataHelper import check_file_read_permission


######################################################
# 関数定義
######################################################
def import_csv_to_row( file_path: Path, delimiter: str=",") -> [list[list]]|None:
    """CSVファイルをlistに取り込む

    デリミターで許容範囲であればlistにとり込みを行う

    Args:
    ----
        file_path (Path): csvファイルのパス指定
        delimiter (str, optional): ファイルのデリミター、Defaults to ",".

    Returns:
    -------
        Optional[list]: 取り込み後のデータ 2次元List構造

    """
    if not isinstance(file_path, Path):
        print(f"{file_path}はPathオブジェクトではありません")
        return None

    if not file_path.exists():
        print(f"{file_path}指定したファイルが存在しません")
        return None

    if not check_file_read_permission(file_path):
        print(f"{file_path}に読み取り権限がありません")
        return None

    try:
        with open(str(file_path), encoding='utf8', newline='') as f:
            rows = list(csv.reader(f, delimiter=delimiter))
    except Exception as e:
        print("例外発生 Exception")
        print(f"{e}: {file_path}")
        return None
    return rows


def import_csv_to_dataframe(
    file_path: Path,
    header=0,
    skiprows=0,
    na_values=['-','NaN', 'null'],
    encoding='utf-8',
    dtype=object,
    engine='python',
    usecols=None,
    ) -> Optional[pd.DataFrame]:
    """CSVをPandasDataFrameへ格納する

    Args:
    ----
        file_path (Path): CSVへのパス
        header (int, optional): データにへダーを含むか Defaults to 0.
        skiprows (int, optional): スキップするデータ件数. Defaults to 0.
        na_values (list, optional): naとして扱うデータ形式 Defaults to ['-','NaN', 'null'].
        encoding (str, optional): 文字コード Defaults to 'utf-8'.
        dtype (_type_, optional): 取り込んだ際の型定義 Defaults to object.
        engine (str, optional): データ評価エンジン指定 Defaults to 'python'.
        usecols (_type_, optional): 取り込む列番号定義 Defaults to None.

    Returns:
    -------
        Optional[pd.DataFrame]: CSVデータから取得したデータを格納したDataFrame 2次元Matrix

    Note:
    ----
        CSVファイルは全カラム取り込みをデフォルトとしています。
        usecols=Noneをデフォルトとし、None（全取り込み）を初期パメータ設定している。
        必要に応じてusecolsを設定して利用します。
    """
    if not isinstance(file_path, Path):
        print(f"{file_path}はPathオブジェクトではありません")
        return None

    if not file_path.exists():
        print(f"{file_path}指定したファイルが存在しません")
        return None

    if not check_file_read_permission(file_path):
        print(f"{file_path}に読み取り権限がありません")
        return None

    try:
        df = pd.read_csv(
            file_path,
            header=header,
            skiprows=skiprows,
            na_values=na_values,
            encoding=encoding,
            dtype=dtype,
            engine=engine,
            usecols=usecols,
        )
    except Exception as e:
        print("例外発生 Exception")
        print(f"{e}: {file_path!s}")
        return None

    return df
