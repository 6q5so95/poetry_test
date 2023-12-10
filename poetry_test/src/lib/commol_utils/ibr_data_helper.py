"""_summary_

Returns
-------
    _type_: _description_

"""
import os
import re
from pathlib import Path


def is_file_read_permission(file_path: Path) -> bool:
    """読み取り権限有無チェック

    Args:
    ----
        file_path (Path): チェック対象ファイルのPathオブジェクト

    Raises:
    ------
        なし

    Returns:
    -------
        bool: 読み取り権限がある場合はTrue
    """
    if not file_path.exists():
        return False

    if not file_path.is_file():
        return False

    if not os.access(file_path, os.R_OK):
        return False

    return True


def check_file_read_permission(file_path: Path) -> bool:
    """読み取り権限有無チェック

    Args:
    ----
        file_path (Path): チェック対象ファイルのPathオブジェクト

    Raises:
    ------
        FileNotFoundError: ファイルが存在しない場合
        IsADirectoryError: ファイルではなくディレクトリの場合
        PermissionError: 読み取り権限がない場合

    Returns:
    -------
        bool: 読み取り権限がある場合はTrue
    """
    if not file_path.exists():
        raise FileNotFoundError(f"ファイル {file_path} が存在しません")

    if not file_path.is_file():
        raise IsADirectoryError(f"{file_path} はディレクトリです")

    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"ファイル {file_path} に読み取り権限がありません")

    return True

def is_file_write_permission(file_path: Path) -> bool:
    """書き込み権限有無チェック

    Args:
    ----
        file_path (Path): チェック対象ファイルのPathオブジェクト

    Returns:
    -------
        bool: 読み取り権限がある場合はTrue
    """
    # １つ上階層の親ディレクトリが存在するか
    parent_dir = file_path.parent
    if not parent_dir.exists():
        return False

    # １つ上階層の親ディレクトリでの書き込み権限チェックを行う
    if not os.access(parent_dir, os.W_OK):
        return False

    # 親ディレクトリにW権限があった上ですでに対象ファイルが存在しW権限がない
    # ファイルが存在しない場合は親ディレクトリ書き込み権限確認済のため通過
    if file_path.exists() and not os.access(str(file_path), os.W_OK):
        return False

    return True

def check_file_write_permission(file_path: Path) -> bool:
    """書き込み権限有無チェック

    Args:
    ----
        file_path (Path): チェック対象ファイルのPathオブジェクト

    Raises:
    ------
        NotADirectoryError: １つ上階層の親ディレクトリが存在しない場合
        PermissionError: １つ上階層の親ディレクトリに書き込み権限がない場合
        PermissionError: 対象ファイルが存在し、書き込み権限がない場合

    Returns:
    -------
        bool: 書き込み権限がある場合はTrue
    """
    parent_dir = file_path.parent
    if not parent_dir.exists():
        raise NotADirectoryError(f"１つ上階層の親ディレクトリが存在しません {file_path}")

    if not os.access(parent_dir, os.W_OK):
        raise PermissionError(f"１つ上階層の親ディレクトリに書き込み権限がありません {file_path}")

    if file_path.exists() and not os.access(str(file_path), os.W_OK):
        raise PermissionError(f"対象ファイル {file_path} が存在し、書き込み権限がありません")

    return True


def delete_file(file_path: Path) -> bool:
    """ファイル削除可否をチェックし、ファイルを消す

    Args:
    ----
        file_path (Path): チェック対象ファイルのPathオブジェクト

    Returns:
    -------
        bool: 成功／失敗
    """
    # Pathオブジェクトであるか
    if not isinstance(file_path, Path):
        return False

    # １つ上階層の親ディレクトリでの書き込み権限チェックを行う
    # ファイルの削除可否は親ディレクトリの権限設定に依存
    parent_dir = file_path.parent
    if not os.access(parent_dir, os.W_OK):
        return False

    # 指定ファイルが存在しない
    if not file_path.exists():
        #raise NotADirectoryError(file_path)
        print(f"file not found: {file_path}")
        return False

    # 指定対象がファイルでない
    if not file_path.is_file():
        #raise FileNotFoundError(file_path)
        print(f"file has is not file: {file_path}")
        return False

    try:
        file_path.unlink()
    except Exception as e:
        print(f"{e}: ファイル削除失敗 {file_path}")
        return False

    return True


def get_file_record_count(file_path: Path) -> int|None:
    """ファイルのレコード件数をカウントする

    Args:
    ----
        file_path (Path): カウント対象ファイルのPathオブジェクト

    Returns:
    -------
        Optional[int]: レコード件数/None

    See:
        check_file_read_permission

    """
    # ファイル読み取り権限があるか
    if not check_file_read_permission(file_path):
        return None

    return sum(1 for line in file_path.open(mode='rb'))


def change_upn_to_id(col: str) -> str|None:
    """UPNからID部分を抽出する

    @ドメイン以降を削除しID部分を抽出する。

    Args:
    ----
        col (str): 処理対象文字列

    Returns:
    -------
        str: ID部分

    Notes:
    -----
        df['id'] = df['UPN'].map(change_UPN_to_ID)

    """
    if not isinstance(col, str):
        print(f"colがstrではありません {col}")
        return None

    return re.sub(r"(^.*)@(.*)", r"\1", col)
