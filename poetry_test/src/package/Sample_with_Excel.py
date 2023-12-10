import pandas as pd

# pattern.1
try:
    with open('example.xlsx', 'rb') as f:
        df = pd.read_excel(f)
except FileNotFoundError as e:
    print(f"ファイルが見つかりませんでした: {e}")
except Exception as e:
    print("ファイルを読み込む際にエラーが発生しました:", e)
else:
    print(df)

# pattern.2
try:
    with pd.ExcelFile('example.xlsx') as xls:
        df = pd.read_excel(xls, sheet_name='Sheet1')
except FileNotFoundError as e:
    print(f"ファイルが見つかりませんでした: {e}")
except Exception as e:
    print(f"ファイルを読み込む際にエラーが発生しました: {e}")
else:
    print(df)


# pattern.3
def read_data(self) -> pd.DataFrame:

    """
    Excelファイルからデータを読み込む。
    :return: Excelファイルから読み込んだデータ
    """
    try:
        with open(self.file_path, 'rb') as file:
            target_excel = pd.ExcelFile(file)
            if self.sheet_name not in target_excel.sheet_names:
                return pd.DataFrame()
            df = target_excel.parse(
                sheet_name=self.sheet_name,
                index_col=False,
                na_values='',
                header=0,
                skiprows=self.skip_rows,
                usecols=self.use_cols,
            )
    except Exception as e:
        raise ValueError(f"Excelファイルの読み込みに失敗しました: {str(e)}")
    return df
