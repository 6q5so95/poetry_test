"""_summary_

Raises
------
    RuntimeError: _description_
    RuntimeError: _description_

Returns
-------
    _type_: _description_

"""
from pathlib import Path

import toml


class TomlParser:
    """TOMLファイルを解析するクラス

    Raises
    ------
        RuntimeError: TOMLファイルの解析中にエラーが発生した場合
        RuntimeError: TOMLファイルの処理中に予期しないエラーが発生した場合

    Returns
    -------
        dict|None: TOMLファイルから読み込んだデータを辞書形式で返す。エラーが発生した場合はNoneを返す。
    """

    @staticmethod
    def parse_toml_file(toml_path: Path) -> dict|None:
        """Tomlファイルを解析する

        Args:
        ----
            toml_path (Path): 解析するTOMLファイルのパス

        Raises:
        ------
            RuntimeError: TOMLファイルの解析中にエラーが発生した場合
            RuntimeError: TOMLファイルの処理中に予期しないエラーが発生した場合

        Returns:
        -------
            dict|None: TOMLファイルから読み込んだデータを辞書形式で返す。エラーが発生した場合はNoneを返す。
        """
        try:
            with toml_path.open() as f:
                return toml.load(f)
        except toml.TomlDecodeError as e:
            raise RuntimeError(f"TOMLファイル {toml_path} を解析する際にエラーが発生しました: {e}") from e
        except Exception as e: # noqa: BLE001 Exceptionを指定する状況を認識済
            raise RuntimeError(f"TOMLファイル {toml_path} を処理する際にエラーが発生しました: {e}")
