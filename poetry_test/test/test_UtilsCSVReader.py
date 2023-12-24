# library
import csv
import inspect

# logger
import logging
import logging.config
import re
import sys
from pathlib import Path
from typing import Any, Optional

import pandas as pd
import pytest
from tabulate import tabulate as tb

#######################################################
# テスト対象ライブラリパス追加/ロード
#######################################################
TARGET_PREFIX = Path(__file__).parent.parent.parent / 'src'
TARGET_PREFIX_LIB = TARGET_PREFIX / 'lib'
sys.path.append(str(TARGET_PREFIX_LIB))
from UtilsCSVReader import import_csv_to_dataframe, import_csv_to_row

############################################
# 実行環境PREFIX 生成
############################################
PREFIX = Path(__file__).parent.parent
PREFIX_DEF = PREFIX / 'def'
PREFIX_LOG = PREFIX / 'log'
PREFIX_TMP = PREFIX / 'tmp'
LOGGINIG_INI = PREFIX_DEF / 'logging.ini'
LOGGINIG_LOG = PREFIX_LOG / 'app.log'

############################################
# logger 定義
############################################
logging.config.fileConfig(LOGGINIG_INI)
logger = logging.getLogger(__name__)

############################################
# Helper 関数
############################################
def create_csv_file(
    file_path: Path,
    data: list[list[Any]],
    delimiter=",",
    quoting=csv.QUOTE_NONE,
    )-> bool:
    """指定した出力先にlist定義したデータを出力する

    Args:
    ----
        file_path (Path): 出力先ファイルフルパス
        data (list):  出力データ、list定義
        delimiter (str, optional): データ区切り文字指定, デフォルトはカンマ区切り
        quoting (_type_, optional): 出力データQuote定義、デフォルトはcsv.QUOTE_NONE

    Returns:
    -------
        True: ファイル作成成功
        False: ファイル作成失敗
    """
    try:
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=delimiter, quoting=quoting)
            writer.writerows(data)
            return True
    except Exception as e:
        logger(f"{e}: csvファイル作成に失敗しました")
        logger(f"{f}")
        logger(f"{delimiter}")
        logger(f"{quoting}")
        return False

############################################
# fixture
############################################
## result
@pytest.fixture(scope='session')
def csv_data_001():
    return [
        ["title1", "title2", "title3"],
        ["aaaaaa", 10, 11],
        ["bbbbbb", 20, 21],
        ["cccccc", 30, 31],
    ]

@pytest.fixture(scope='session')
def csv_data_002():
    return [
        ["title1", "title2", "title3"],
    ]

@pytest.fixture(scope='session')
def csv_data_003():
    return [
        ["aaaaaa", 10, 11],
    ]

@pytest.fixture(scope='session')
def csv_data_004():
    return [
        ["aaaaaa", 10, 11],
        ["bbbbbb", 20, 21],
        ["cccccc", 30, 31],
    ]

## 実行fixture setup/yield/tear down
@pytest.fixture(scope='function')
def csv_resource_001(csv_data_001: list)-> Optional[Path]:
    # テストデータ出力先定義
    outfile = PREFIX_TMP / 'test_UtilsCSVReader_temp_N001.csv'
    if create_csv_file(outfile, csv_data_001):
        # setup
        logger.info("setup")

        # Exectute Test
        yield outfile

        # tear_down
        logger.info("tear down")
        if outfile.exists():
            outfile.parent.chmod(0o755)
            outfile.chmod(0o755)
            logger.info(f"shutil.rmtree: {outfile.parent}")
            #shutil.rmtree(f"{outfile.parent}")
    else:
        print("テスト実行に失敗しています")
        print(f"Test Datapath: {outfile}")
        return None


@pytest.fixture(scope='function')
def csv_resource_002()-> Optional[Path]:
    # テストデータ出力先定義
    outfile = PREFIX_TMP / 'test_UtilsCSVReader_temp_N002.csv'
    with open(outfile, 'w') as f:
        f.write('title1|title2|title3\n')
        f.write('aaaaaa|10|11\n')
        f.write('bbbbbb|20|21\n')
        f.write('cccccc|30|31\n')
    # setup
    logger.info("setup")

    # Exectute Test
    yield outfile

    # tear_down
    logger.info("tear down")
    if outfile.exists():
        outfile.parent.chmod(0o755)
        outfile.chmod(0o755)
        logger.info(f"shutil.rmtree: {outfile.parent}")
        #shutil.rmtree(f"{outfile.parent}")


@pytest.fixture(scope='function')
def csv_resource_003()-> Optional[Path]:
    # テストデータ出力先定義
    outfile = PREFIX_TMP / 'test_UtilsCSVReader_temp_N003.csv'
    with open(outfile, 'w') as f:
        f.write('')
    # setup
    logger.info("setup")

    # Exectute Test
    yield outfile

    # tear_down
    logger.info("tear down")
    if outfile.exists():
        outfile.parent.chmod(0o755)
        outfile.chmod(0o755)
        logger.info(f"shutil.rmtree: {outfile.parent}")
        #shutil.rmtree(f"{outfile.parent}")


@pytest.fixture(scope='function')
def csv_resource_004(csv_data_002: list)-> Optional[Path]:
    # テストデータ出力先定義
    outfile = PREFIX_TMP / 'test_UtilsCSVReader_temp_N004.csv'
    if create_csv_file(outfile, csv_data_002):
        # setup
        logger.info("setup")

        # Exectute Test
        yield outfile

        # tear_down
        logger.info("tear down")
        if outfile.exists():
            outfile.parent.chmod(0o755)
            outfile.chmod(0o755)
            logger.info(f"shutil.rmtree: {outfile.parent}")
            #shutil.rmtree(f"{outfile.parent}")
    else:
        print("テスト実行に失敗しています")
        print(f"Test Datapath: {outfile}")
        return None


@pytest.fixture(scope='function')
def csv_resource_005(csv_data_003: list)-> Optional[Path]:
    # テストデータ出力先定義
    outfile = PREFIX_TMP / 'test_UtilsCSVReader_temp_N005.csv'
    if create_csv_file(outfile, csv_data_003):
        # setup
        logger.info("setup")

        # Exectute Test
        yield outfile

        # tear_down
        logger.info("tear down")
        if outfile.exists():
            outfile.parent.chmod(0o755)
            outfile.chmod(0o755)
            logger.info(f"shutil.rmtree: {outfile.parent}")
            #shutil.rmtree(f"{outfile.parent}")
    else:
        print("テスト実行に失敗しています")
        print(f"Test Datapath: {outfile}")
        return None


@pytest.fixture(scope='function')
def csv_resource_006()-> Optional[Path]:
    # テストデータ出力先定義
    outfile = PREFIX_TMP / 'test_UtilsCSVReader_temp_N006.csv'
    with open(outfile, 'w') as f:
        f.write('title1,title2,title3\n')
        f.write('aaaaaa,10,11\n')
        f.write('bbbbbb,20,21\n')
        f.write('cccccc,30,31\n')
    # setup
    logger.info("setup")

    # Exectute Test
    yield outfile

    # tear_down
    logger.info("tear down")
    if outfile.exists():
        outfile.parent.chmod(0o755)
        outfile.chmod(0o755)
        logger.info(f"shutil.rmtree: {outfile.parent}")
        #shutil.rmtree(f"{outfile.parent}")


@pytest.fixture(scope='function')
def csv_resource_007()-> Optional[Path]:
    # テストデータ出力先定義
    outfile = PREFIX_TMP / 'test_UtilsCSVReader_temp_N007.csv'
    with open(outfile, 'w') as f:
        f.write('title1\ttitle2\ttitle3\n')
        f.write('aaaaaa\t10\t11\n')
        f.write('bbbbbb\t20\t21\n')
        f.write('cccccc\t30\t31\n')
    # setup
    logger.info("setup")

    # Exectute Test
    yield outfile

    # tear_down
    logger.info("tear down")
    if outfile.exists():
        outfile.parent.chmod(0o755)
        outfile.chmod(0o755)
        logger.info(f"shutil.rmtree: {outfile.parent}")
        #shutil.rmtree(f"{outfile.parent}")


@pytest.fixture(scope='function')
def csv_resource_008()-> Optional[Path]:
    # テストデータ出力先定義
    outfile = PREFIX_TMP / 'test_UtilsCSVReader_temp_N008.csv'
    with open(outfile, 'w') as f:
        f.write('title1 title2 title3\n')
        f.write('aaaaaa 10 11\n')
        f.write('bbbbbb 20 21\n')
        f.write('cccccc 30 31\n')
    # setup
    logger.info("setup")

    # Exectute Test
    yield outfile

    # tear_down
    logger.info("tear down")
    if outfile.exists():
        outfile.parent.chmod(0o755)
        outfile.chmod(0o755)
        logger.info(f"shutil.rmtree: {outfile.parent}")
        #shutil.rmtree(f"{outfile.parent}")


@pytest.fixture(scope='function')
def csv_resource_009(csv_data_004: list)-> Optional[Path]:
    # テストデータ出力先定義
    outfile = PREFIX_TMP / 'test_UtilsCSVReader_temp_N009.csv'
    if create_csv_file(outfile, csv_data_004):
        # setup
        logger.info("setup")

        # Exectute Test
        yield outfile

        # tear_down
        logger.info("tear down")
        if outfile.exists():
            outfile.parent.chmod(0o755)
            outfile.chmod(0o755)
            logger.info(f"shutil.rmtree: {outfile.parent}")
            #shutil.rmtree(f"{outfile.parent}")
    else:
        print("テスト実行に失敗しています")
        print(f"Test Datapath: {outfile}")
        return None



###########################################
# テスト実施
############################################
# Important! C0, C1, C2観点でテスト範囲をカバーすること
# pytest -lsv xxxxxx

class Test_import_csv_to_row:
    """import_csv_to_rowのテスト全体をまとめたClass
    C0: 命令カバレッジ
        ファイルアクセスカバレッジ
            - ファイルパスが存在する/読み取り権限がある/数件のデータがある場合
            - ファイルパスがPathオブジェクトでない場合
            - ファイルパスが存在しない場合
            - 読み取り権限のないファイルを指定した場合
            - ファイルOPEN処理で例外が発生する場合

    C1: 分岐カバレッジ
        引数カバレッジ
            - file_pathがNoneの場合
            - delimiterがNoneの場合
            - delimiterを変更して読み取った場合

    C2: 条件カバレッジ
        CSVファイル内容カバレッジ
            - CSVファイルの中身が空の場合
            - csvファイルにヘッダーだけがある場合
            - CSVファイルの中身がへダーがなく1行だけの場合
            - csvファイルの区切り文字がカンマの場合
            - csvファイルの区切り文字がタブの場合
            - csvファイルの区切り文字がスペースの場合
            #- CSVファイルの中身が複数行ある場合 -> C0で検証済
            #- csvファイルの区切り文字がパイプの場合 -> C1で検証済
    """

    def test_C0_Normal_UT_import_csv_to_row_Normal_data_include_header(self, csv_resource_001):
        """テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: へダーありデータの取り込み
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_row(csv_resource_001)
        logger.info(f"result: \n{result}")

        # assert
        assert type(result) == list
        assert result[0] == ['title1', 'title2', 'title3']
        assert result[1] == ['aaaaaa', '10', '11']
        assert result[2] == ['bbbbbb', '20', '21']
        assert result[3] == ['cccccc', '30', '31']


    def test_C0_Error_UT_path_is_not_Path_instance(self, csv_resource_001):
        """テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: Pathインスタンス以外を渡す,None戻り確認
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_row("AAAAAAAAAAAAA")
        logger.info(f"result: \n{result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == None


    def test_C0_Error_UT_path_is_not_exists(self, csv_resource_001):
        """テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: 存在しない適当なPathObject指定,None戻り確認
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_row(Path("AAAAAAAAAAAAA"))
        logger.info(f"result: \n{result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == None


    def test_C0_Error_UT_path_is_not_have_read_permission(self, csv_resource_001):
        """テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: 読み取り権限のないパス指定,None戻り確認 Path('/home/nxautomation')
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        csv_resource_001.chmod(0o111)
        result = import_csv_to_row(csv_resource_001)
        logger.info(f"result: \n{result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == None


    def test_C0_Error_UT_open_error_by_mock(self, mocker, csv_resource_001):
        """テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: データ操作処理のtry-catchでのexceptionをmockでシミュレート
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # openコマンド実行時にExceptionが発生するようMocker定義を行う
        ## buildin.open→Exception
        mocker.patch("builtins.open", side_effect=Exception)

        result = import_csv_to_dataframe(csv_resource_001)
        logger.info(f"result: \n{tb(result, headers='keys')}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == None


    def test_C1_Error_UT_set_path_None(self, csv_resource_001):
        """テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: pathにNoneを指定する, Noneが返る
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_row(None)
        logger.info(f"result: \n{result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == None


    def test_C1_Error_UT_set_delimiter_None(self, csv_resource_001):
        """テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: delimiterにNoneを指定する, delimiter must be string, Noneが返る
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_row(csv_resource_001, delimiter=None)
        logger.info(f"result: \n{result}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == None


    def test_C1_Normal_UT_set_delimiter_to_pipe(self, csv_resource_002):
        """テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 正常系/UT
        - テストシナリオ: delimiterに|を指定する
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_row(csv_resource_002, delimiter="|")
        logger.info(f"result: \n{result}")

        # assert
        assert type(result) == list
        assert result[0] == ['title1', 'title2', 'title3']
        assert result[1] == ['aaaaaa', '10', '11']
        assert result[2] == ['bbbbbb', '20', '21']
        assert result[3] == ['cccccc', '30', '31']


    def test_C2_Normal_UT_set_data_empty(self, csv_resource_003):
        """テスト定義：
        - テストカテゴリ: C2
        - テスト区分: 正常系/UT
        - テストシナリオ: 取り込みデータをゼロ件
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_row(csv_resource_003)
        logger.info(f"result: \n{result}")

        # assert
        assert type(result) == list
        assert result == []


    def test_C2_Normal_UT_set_data_only_header(self, csv_resource_004):
        """テスト定義：
        - テストカテゴリ: C2
        - テスト区分: 正常系/UT
        - テストシナリオ: 取り込みデータへダーのみ
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_row(csv_resource_004)
        logger.info(f"result: \n{result}")

        # assert
        assert type(result) == list
        assert result[0] == ['title1', 'title2', 'title3']


    def test_C2_Normal_UT_set_data_only_detail(self, csv_resource_005):
        """テスト定義：
        - テストカテゴリ: C2
        - テスト区分: 正常系/UT
        - テストシナリオ: 取り込みデータ明細のみ
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_row(csv_resource_005)
        logger.info(f"result: \n{result}")

        # assert
        assert type(result) == list
        assert result[0] == ['aaaaaa', '10', '11']


    def test_C2_Normal_UT_set_data_delimiter_to_commma(self, csv_resource_006):
        """テスト定義：
        - テストカテゴリ: C2
        - テスト区分: 正常系/UT
        - テストシナリオ: 取り込みデータカンマ区切り、delimiter指定
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_row(csv_resource_006, delimiter=',')
        logger.info(f"result: \n{result}")

        # assert
        assert type(result) == list
        assert result[0] == ['title1', 'title2', 'title3']
        assert result[1] == ['aaaaaa', '10', '11']
        assert result[2] == ['bbbbbb', '20', '21']
        assert result[3] == ['cccccc', '30', '31']


    def test_C2_Normal_UT_set_data_delimiter_to_tab(self, csv_resource_007):
        """テスト定義：
        - テストカテゴリ: C2
        - テスト区分: 正常系/UT
        - テストシナリオ: 取り込みデータTab区切り、delimiter指定
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_row(csv_resource_007, delimiter='\t')
        logger.info(f"result: \n{result}")

        # assert
        assert type(result) == list
        assert result[0] == ['title1', 'title2', 'title3']
        assert result[1] == ['aaaaaa', '10', '11']
        assert result[2] == ['bbbbbb', '20', '21']
        assert result[3] == ['cccccc', '30', '31']


    def test_C2_Normal_UT_set_data_delimiter_to_space(self, csv_resource_008):
        """テスト定義：
        - テストカテゴリ: C2
        - テスト区分: 正常系/UT
        - テストシナリオ: 取り込みデータSpace区切り、delimiter指定
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_row(csv_resource_008, delimiter=' ')
        logger.info(f"result: \n{result}")

        # assert
        assert type(result) == list
        assert result[0] == ['title1', 'title2', 'title3']
        assert result[1] == ['aaaaaa', '10', '11']
        assert result[2] == ['bbbbbb', '20', '21']
        assert result[3] == ['cccccc', '30', '31']


###########################################
# テスト実施
############################################
# Important! C0, C1, C2観点でテスト範囲をカバーすること
# pytest -lsv xxxxxx

class Test_import_csv_to_dataframe:
    """import_csv_to_rowのテスト全体をまとめたClass
    C0: 命令カバレッジ
        ファイルアクセスカバレッジ
            - ファイルパスが存在する/読み取り権限がある/数件のデータがある場合
            - ファイルパスがPathオブジェクトでない場合
            - ファイルパスが存在しない場合
            - 読み取り権限のないファイルを指定した場合
            - ファイルOPEN処理で例外が発生する場合

    C1: 分岐カバレッジ
        引数カバレッジ
            - file_pathがNoneの場合
            - skiprowsがNoneの場合
            - headerがNoneの場合
            - usercolsがNoneの場合

    C2: 条件カバレッジ
        CSVファイル内容カバレッジ
            - CSVファイルの中身が空の場合
            - csvファイルにヘッダーだけがある場合
            - CSVファイルの中身がへダーがなく1行だけの場合
            - CSVファイルの中身がへダーがなく複数行ある場合
            - CSVファイルの中身がへダーがなく複数行ある場合, skiprowを指定 読み飛ばし行チェック
            - CSVファイルの中身がへダーがなく複数行ある場合, usecolsを指定 取得列チェック
            - CSVファイルの中身がへダーがなく複数行ある場合, usecolsを存在範囲上で指定 空Frame戻り
            #- CSVファイルの中身がへダーがありデータが複数行ある場合 -> C0で検証済
    """

    def test_C0_Normal_UT_import_csv_to_row_Normal_data_include_header(self, csv_resource_001: Path):
        """テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 正常系/UT
        - テストシナリオ: へダーありデータの取り込み
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_dataframe(csv_resource_001)
        logger.info(f"result: \n{tb(result, headers='keys')}")

        # assert
        assert type(result) == pd.DataFrame
        x, y = result.shape
        assert x == 3
        assert y == 3
        assert list(result.columns) == ['title1', 'title2', 'title3']
        assert list(result.iloc[0, :]) == ['aaaaaa', '10', '11']
        assert list(result.iloc[1, :]) == ['bbbbbb', '20', '21']
        assert list(result.iloc[2, :]) == ['cccccc', '30', '31']


    def test_C0_Error_UT_path_is_not_Path_instance(self, csv_resource_001):
        """テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: Pathインスタンス以外を渡す,None戻り確認
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_dataframe("AAAAAAAAAAAAA")
        logger.info(f"result: \n{tb(result, headers='keys')}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == None


    def test_C0_Error_UT_path_is_not_exists(self, csv_resource_001):
        """テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: 存在しない適当なPathObjectを指定,None戻り確認
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_dataframe(Path('AAAAAAAAAAAAAAAAAA'))
        logger.info(f"result: \n{tb(result, headers='keys')}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == None


    def test_C0_Error_UT_path_is_not_have_read_permission(self, csv_resource_001):
        """テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: 読み取り権限のないパス指定,None戻り確認
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        csv_resource_001.chmod(0o111)
        result = import_csv_to_dataframe(csv_resource_001)
        logger.info(f"result: \n{tb(result, headers='keys')}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == None


    def test_C0_Error_UT_open_error_by_mock(self, mocker, csv_resource_001):
        """テスト定義：
        - テストカテゴリ: C0
        - テスト区分: 異常系/UT
        - テストシナリオ: データ操作処理のtry-catchでのexceptionをmockでシミュレート
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # openコマンド実行時にExceptionが発生するようMocker定義を行う
        mocker.patch("builtins.open", side_effect=Exception)

        result = import_csv_to_dataframe(csv_resource_001)
        logger.info(f"result: \n{tb(result, headers='keys')}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == None


    def test_C1_Error_UT_set_path_None(self, csv_resource_001):
        """テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 異常系/UT
        - テストシナリオ: pathにNoneを指定する, Noneが返る
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_dataframe(None)
        logger.info(f"result: \n{tb(result, headers='keys')}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == None


    def test_C1_Normal_UT_set_skiprows_None(self, csv_resource_001):
        """テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 正常系/UT
        - テストシナリオ: skiprowsにNoneを指定する, データ取り込み正常
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_dataframe(csv_resource_001, skiprows=None)
        logger.info(f"result: \n{tb(result, headers='keys')}")

        # assert
        assert type(result) == pd.DataFrame
        x, y = result.shape
        assert x == 3
        assert y == 3
        assert list(result.columns) == ['title1', 'title2', 'title3']
        assert list(result.iloc[0, :]) == ['aaaaaa', '10', '11']
        assert list(result.iloc[1, :]) == ['bbbbbb', '20', '21']
        assert list(result.iloc[2, :]) == ['cccccc', '30', '31']


    def test_C1_Normal_UT_set_header_None(self, csv_resource_001):
        """テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 正常系/UT
        - テストシナリオ: headerにNoneを指定する, データ取り込み正常
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_dataframe(csv_resource_001, header=None)
        logger.info(f"result: \n{tb(result, headers='keys')}")

        # assert
        assert type(result) == pd.DataFrame
        x, y = result.shape
        assert x == 4
        assert y == 3
        assert list(result.iloc[0, :]) == ['title1', 'title2', 'title3']
        assert list(result.iloc[1, :]) == ['aaaaaa', '10', '11']
        assert list(result.iloc[2, :]) == ['bbbbbb', '20', '21']
        assert list(result.iloc[3, :]) == ['cccccc', '30', '31']


    def test_C1_Normal_UT_set_usecols_None(self, csv_resource_001):
        """テスト定義：
        - テストカテゴリ: C1
        - テスト区分: 正常系/UT
        - テストシナリオ: usecolsにNoneを指定する, データ取り込み正常
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_dataframe(csv_resource_001, usecols=None)
        logger.info(f"result: \n{tb(result, headers='keys')}")

        # assert
        assert type(result) == pd.DataFrame
        x, y = result.shape
        assert x == 3
        assert y == 3
        assert list(result.columns) == ['title1', 'title2', 'title3']
        assert list(result.iloc[0, :]) == ['aaaaaa', '10', '11']
        assert list(result.iloc[1, :]) == ['bbbbbb', '20', '21']
        assert list(result.iloc[2, :]) == ['cccccc', '30', '31']


    def test_C2_Normal_UT_set_data_empty(self, csv_resource_003):
        """テスト定義：
        - テストカテゴリ: C2
        - テスト区分: 正常系/UT
        - テストシナリオ: 取り込みデータをゼロ件
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_dataframe(csv_resource_003)
        logger.info(f"result: \n{tb(result, headers='keys')}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"


    def test_C2_Normal_UT_set_data_only_header(self, csv_resource_004):
        """テスト定義：
        - テストカテゴリ: C2
        - テスト区分: 正常系/UT
        - テストシナリオ: 取り込みデータへダーのみ
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_dataframe(csv_resource_004)
        logger.info(f"result: \n{tb(result, headers='keys')}")

        # assert
        assert type(result) == pd.DataFrame
        x, y = result.shape
        assert x == 0
        assert y == 3
        assert list(result.columns) == ['title1', 'title2', 'title3']


    def test_C2_Normal_UT_set_data_only_detail(self, csv_resource_005):
        """テスト定義：
        - テストカテゴリ: C2
        - テスト区分: 正常系/UT
        - テストシナリオ: 取り込みデータ明細のみ １件
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_dataframe(csv_resource_005, header=None)
        logger.info(f"result: \n{tb(result, headers='keys')}")

        # assert
        assert type(result) == pd.DataFrame
        x, y = result.shape
        assert x == 1
        assert y == 3
        assert list(result.columns) == [0, 1, 2]


    def test_C2_Normal_UT_set_data_some_detail(self, csv_resource_009):
        """テスト定義：
        - テストカテゴリ: C2
        - テスト区分: 正常系/UT
        - テストシナリオ: 取り込みデータ明細のみ １件
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_dataframe(csv_resource_009, header=None)
        logger.info(f"result: \n{tb(result, headers='keys')}")

        # assert
        assert type(result) == pd.DataFrame
        x, y = result.shape
        assert x == 3
        assert y == 3
        assert list(result.columns) == [0, 1, 2]


    def test_C0_Normal_UT_import_csv_to_row_Normal_data_include_header_with_skiprows(self, csv_resource_001: Path):
        """テスト定義：
        - テストカテゴリ: C2
        - テスト区分: 正常系/UT
        - テストシナリオ: へダーありデータの取り込み, skiprows指定 skiprow=1のため結果Header行を飛ばす状況になる
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_dataframe(csv_resource_001,skiprows=1)
        logger.info(f"result: \n{tb(result, headers='keys')}")

        # assert
        assert type(result) == pd.DataFrame
        x, y = result.shape
        assert x == 2
        assert y == 3
        #assert list(result.columns) == ['title1', 'title2', 'title3']
        assert list(result.columns) == ['aaaaaa', '10', '11']
        assert list(result.iloc[0, :]) == ['bbbbbb', '20', '21']
        assert list(result.iloc[1, :]) == ['cccccc', '30', '31']


    def test_C0_Error_UT_import_csv_to_row_Normal_data_include_header_with_skiprows_overvalue(self, csv_resource_001: Path):
        """テスト定義：
        - テストカテゴリ: C2
        - テスト区分: 正常系/UT
        - テストシナリオ: へダーありデータの取り込み, skiprows指定 skiprow=100のため結果はNone
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_dataframe(csv_resource_001,skiprows=100)
        logger.info(f"result: \n{tb(result, headers='keys')}")

        # assert
        assert str(type(result)) == "<class 'NoneType'>"
        assert result == None


    def test_C0_Normal_UT_import_csv_to_row_Normal_data_include_header_with_usecols(self, csv_resource_001: Path):
        """テスト定義：
        - テストカテゴリ: C2
        - テスト区分: 正常系/UT
        - テストシナリオ: へダーありデータの取り込み, usecols指定 0列と2列を指定
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_dataframe(csv_resource_001,usecols=[0, 2])
        logger.info(f"result: \n{tb(result, headers='keys')}")

        # assert
        assert type(result) == pd.DataFrame
        x, y = result.shape
        assert x == 3
        assert y == 2
        assert list(result.columns) == ['title1', 'title3']
        assert list(result.iloc[0, :]) == ['aaaaaa', '11']
        assert list(result.iloc[1, :]) == ['bbbbbb', '21']
        assert list(result.iloc[2, :]) == ['cccccc', '31']


    def test_C0_Error_UT_import_csv_to_row_Normal_data_include_header_with_usecols_overvalue(self, csv_resource_001: Path):
        """テスト定義：
        - テストカテゴリ: C2
        - テスト区分: 異常系/UT
        - テストシナリオ: へダーありデータの取り込み, usecols指定,存在しない列番号指定, 空のDataFrameが返る

        Note:
        ----
            test_UtilsCSVReader.py::Test_import_csv_to_dataframe::test_C0_Normal_UT_import_csv_to_row_Normal_data_include_header_with_usecols_overvalue
            /home/satoshi/git_area/pytest_first_kaggle/src/lib/UtilsCSVReader.py:94: FutureWarning: Defining usecols with out of bounds indices is deprecated and will raise a ParserError in a future version.
        """
        # test info（変更不要）
        logger.info(re.sub(r' {2}', '', f"\n{'='*10} {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {'='*10}"))
        logger.info(re.sub(r' {2}', '', eval(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}.__doc__"))[:-1])

        # Execute test
        result = import_csv_to_dataframe(csv_resource_001,usecols=[3, 100])
        logger.info(f"result: \n{tb(result, headers='keys')}")

        # assert
        assert type(result) == pd.DataFrame
        x, y = result.shape
        assert x == 0
        assert y == 0
