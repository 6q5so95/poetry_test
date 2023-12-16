
import pandas as pd


class ExcelDataLoader:
    """Excelファイルからデータを読み込むためのクラス

    :param file_path: ファイルのパス
    :param sheet_name: 対象のシート名
    :param skip_rows: ヘッダ行を除外する場合の行数
    :param use_cols: 使用する列のインデックスのリスト。指定されない場合はすべての列を使用する。
    """

    def __init__(                  # noqa: ANN204,PLR0913
        self,                      # noqa: ANN101
        file_path: str,
        sheet_name: str,
        skip_rows: int = 0,
        use_cols: list[int]|None=None,
        exclusion_sheets: list[int]|None = None,
    ):
        """ExcelDataLoaderオブジェクトを初期化する"""
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.skip_rows = skip_rows
        self.use_cols = use_cols
        self.exclusionSheets = exclusion_sheets

    def read_excel_one_sheet(self) -> pd.DataFrame|None:  # noqa: ANN101
        """対象のExcelBookに対し指定した1シートをDataFrameに取り込む

        各種パラメターによりチューニングしたDataFrameの状態にある。
        ヘダースキップして最初の行をcolumnsとして取り込む。

        Raises
        ------
            ValueError: 全包囲で例外を拾った結果、ValueErrorを返す

        Returns
        -------
            pd.DataFrame|None: Excelシートを取り込んだDataFrame

        """
        try:
            with pd.ExcelFile(self.file_path) as target_excel:
                # 指定PathでExcelBookがない場合は空のDataFrameを返す
                if self.sheet_name not in target_excel.sheet_names:
                    return pd.DataFrame()

                return target_excel.parse(
                    sheet_name=self.sheet_name,
                    index_col=False,
                    na_values="",
                    header=0,
                    skiprows=self.skip_rows,
                    usecols=self.use_cols,
                )
        except FileNotFoundError:
            raise ValueError(f"指定されたファイルが見つかりませんでした: {self.file_path}")
        except ValueError as e:
            raise ValueError(f"Excelファイルの読み込みに失敗しました: {e}") from e
        except Exception as e:  # noqa: BLE001を許容(pd.read_excel()は様々な例外が発生するため)
            raise RuntimeError(f"予期しないエラーが発生しました: {e}") from e
        finally:
            target_excel.close()


    def read_excel_all_sheets(self) -> pd.DataFrame|None:    # noqa: ANN101
        """対象のExcelBookに対し取り込まないと指定したシート以外を全てDataFrameに取り込む

        シートは全て同一フォーマットである必要がある。
        各種パラメターによりチューニングしたDataFrameの状態にある。
        ヘダースキップして最初の行をcolumnsとして取り込む。

        Raises
        ------
            ValueError: 指定したExcelBookが見つからない
            ValueError: DataFrame取り込み時に起きたエラー全て

        Returns
        -------
            pd.DataFrame|None: 条件を満たす全てのExcelSheetを取り込んだDataFrame
        """
        try:
            with pd.ExcelFile(self.file_path) as target_excel:
                # 処理対象シートのみDataFrame生成
                all_sheets = {sheet: target_excel.parse(sheet) for sheet in target_excel.sheet_names if sheet not in self.exclusionSheets}
        except FileNotFoundError as e:
            raise ValueError(f"can not get target files {e}") from e
        except Exception as e:  # noqa: BLE001を許容(pd.read_excel()は様々な例外が発生するため)
            raise RuntimeError(f"予期しないエラーが発生しました: {e}") from e
        finally:
            target_excel.close()

        try:
            df_cum_excel = pd.concat(
                [
                    all_sheets[worksheet]
                    for worksheet in all_sheets
                ],
            )
        except Exception as e:  # noqa: BLE001を許容(pd.read_excel()は様々な例外が発生するため)
            raise RuntimeError(f"ExcelSheet読み込み処理に失敗しました: {e}") from e
        finally:
            pass

        return df_cum_excel.reset_index(drop=True)
