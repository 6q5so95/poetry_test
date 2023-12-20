from pathlib import Path
import shutil
import os

def move_file(source_path, destination_directory):
    source_path = Path(source_path)
    destination_directory = Path(destination_directory)

    # 移動元の存在チェックと読み取り権限チェック
    if not source_path.exists():
        raise FileNotFoundError(f"エラー: ファイルが存在しません - {source_path}")
    if not source_path.is_file() or not os.access(source_path, os.R_OK):
        raise PermissionError(f"エラー: ファイルに読み取り権限がありません - {source_path}")

    # 移動先のディレクトリ存在チェックと書き込み権限チェック
    if not destination_directory.exists() or not destination_directory.is_dir() or not os.access(destination_directory, os.W_OK):
        raise PermissionError(f"エラー: 移動先のディレクトリに書き込み権限がありません - {destination_directory}")

    # 移動先のファイルパスを構築
    destination_path = destination_directory / source_path.name

    # 移動先に同名ファイルが存在するか確認
    if destination_path.exists():
        raise FileExistsError(f"エラー: 移動先に同名のファイルが既に存在します - {destination_path}")

    # ファイルを移動
    try:
        source_path.replace(destination_path)
        print(f"ファイルを {destination_path} に移動しました。")
    except Exception as e:
        raise Exception(f"エラー: ファイルの移動中にエラーが発生しました - {str(e)}")

# 例として使い方
source_file = "/path/to/source/file.txt"
destination_directory = "/path/to/destination/"

try:
    move_file(source_file, destination_directory)
except Exception as e:
    print(str(e))
