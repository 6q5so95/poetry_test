# library
import csv
import pandas as pd

from pathlib import Path
from typing import Optional
from typing import Sequence
from typing import Union

######################################################
# 同一階層ライブラリ
######################################################
from UtilsDataHelper import check_file_read_permission

######################################################
# 関数定義
######################################################
def import_excel_onesheet_to_dataframe(
    file_path: Union[str, Path],
    target_sheet_name: str,
    skiprows: int,
    usecols: Optional[Sequence[int]] = None
) -> Optional[pd.DataFrame]:
    """
    指定したExcelファイルから、指定したシートを読み込んで、pandas DataFrameとして返す。
    Args:
        file_path: strまたはPathオブジェクト。Excelファイルのパス。
        target_sheet_name: str。読み込むシート名。
        skiprows: int。読み込み開始行。
        use_cols: オプション。listまたはtuple。読み込む列名のリスト。
    Returns:
        pd.DataFrameまたはNone。読み込みが成功した場合は、pandas DataFrameを返す。それ以外の場合は、Noneを返す。
    """
    if not isinstance(file_path, Path):
        print(f"Pathオブジェクトを指定してください {file_path}")
        return None

    if not file_path.is_file():
        print(f"ファイルが存在しないか、ファイルへのアクセス権がありません。{file_path}")
        return None

    if usecols is None:
        print(f"use_colsパラメータがNoneに設定されています: {usecols}")
        return None

    if not isinstance(usecols, list) or not all(isinstance(x, int) for x in usecols):
        print("usecolsはint型のリストで指定してください。")
        return None

    # Excelインスタンス生成
    try:
        target_excel = pd.ExcelFile(file_path)
    except Exception as e:
        print(f"{e}:")
        return None

    if not target_sheet_name in target_excel.sheet_names:
        print(f"シートが存在しません: {target_sheet_name}")
        return None

    try:
        parse_args = dict(
            target_sheet_name=target_sheet_name,
            index_col=False,
            na_values='',
            header=0,
            skiprows=skiprows,
            usecols = usecols
        )
        df = target_excel.parse(**parse_args)
    except Exception as e:
        print(f"{e}: parse処理で例外が発生しました")
        return None

    return df


def import_excel_sheets_to_dataframe(
    file_path: Path,
    skiprows: int,
    exclusion_sheet_names=None,
    na_values=['-','NaN', 'null'],
    usecols=None,
    ) -> Optional[pd.DataFrame]:
    """指定したExcelBookの複数シートに対してページごとにデータを積み上げて１つのDataFrameを生成する

    Args:
        file_path (Path): ExcelBook Path
        skiprows (int): データスキップ行 
        exclusion_sheet_names (str_, optional): 取り込まないSheet名 Defaults to None.
        na_values (list, optional): NAとして扱うExcel上のデータ Defaults to ['-','NaN', 'null'].
        usecols (int, optional): 取り込む絡む列番号 Defaults to None. Noneのままだとデータ取り込みしない

    Returns:
        Optional[pd.DataFrame]: パラメータ、データエラーによりNoneが返るケースあり

    """
    if not isinstance(file_path, Path):
        print(f"Pathオブジェクトを指定してください {file_path}")
        return None

    if not file_path.is_file():
        print(f"ファイルが存在しないか、ファイルへのアクセス権がありません。{file_path}")
        return None

    if usecols is None:
        print(f"use_colsパラメータがNoneに設定されています: {usecols}")
        return None

    if not isinstance(usecols, list) or not all(isinstance(x, int) for x in usecols):
        print("use_colsはint型のリストで指定してください。")
        return None


    # excelインスタンス生成
    target_excel = pd.ExcelFile(file_path)

    # 器を初期化
    df_cum_excel = pd.DataFrame()

    # 除外なし
    if exclusion_sheet_names is None:
        exclusion_sheet_names = []

    # Book内のSheetを積み上げ
    try:
        for worksheet in target_excel.sheet_names:
            # 取り込み除外シートはバイパス
            if worksheet not in exclusion_sheet_names:
                df_work_excel = target_excel.parse(
                    worksheet,
                    index_col=False,
                    exclusion_sheet_names=exclusion_sheet_names,
                    na_values=na_values,
                    skiprows=skiprows,
                    usecols=usecols,
                )
                # 積み上げ
                df_cum_excel = pd.concat([df_cum_excel, df_work_excel])

    except Exception as e:
        print(f"{e}: parse処理で例外が発生しました")
        return None

    # EDA
    df_cum_excel.reset_index(inplace=True, drop=True)

    return df_cum_excel