import yaml
from pathlib import Path
from typing import Optional

######################################################
# 同一階層ライブラリ
######################################################
from UtilsDataHelper import check_file_read_permission

######################################################
# 関数定義
######################################################

class YamlParser:
    """Class for parsing YAML files into objects."""

    @staticmethod
    def parse_yaml_file(yaml_path: Path) -> Optional[dict]:
        """Parse the YAML file and return an object of the corresponding type.

        Arges:
            yaml_path: Path to YAML file

        Returns:
            dict: loaded yaml strcture to dict

        Raises:
            exception: yaml file処理のException

        Examples:
            @staticmethodにしているのでインスタンス生成せず直接利用する
            >>> _dict = YamlParser.parse_yaml_file('xxxxx/yyyyy.yaml')

        Note:
            sys.path.append()を使ってlibへのパスを通してから使用する。

        """
        if not isinstance(yaml_path, Path):
            print(f"Pathオブジェクトではありません {yaml_path}")
            return None

        if not yaml_path.exists():
            print(f"存在しないファイルです {yaml_path}")
            return None

        if not check_file_read_permission(yaml_path):
            print(f"{yaml_path}に読み取り権限がありません")
            return None

        try:
            with open(yaml_path) as f:
                yaml_obj = yaml.safe_load(f)
        except Exception as e:
            print(f"{e}: Error/yamlfile: {yaml_path}")
            return None

        return yaml_obj
