import yaml

from logging import config
from logging import Logger
from json import load
from pathlib import Path

####################################
# カスタムライブラリ導入
####################################

####################################
# Helper関数
####################################
    def config_Logger(logger: Logger, LIBPATH: str):
        """logger定義を取得する

        Args:
            logger (Logger): 
            LIBPATH (str): _description_

        Raises:
            TypeError: _description_
            FileNotFoundError: _description_

        Returns:
            _type_: _description_
        """
        if not isinstance(logger, Logger):
            raise TypeError

        if not isinstance(LIBPATH, str):
            raise TypeError

        filepath = Path(f"LIBPATH")
        if not filepath.exists():
            raise FileNotFoundError

        # logger定義ロード
        try:
            with open (filepath, 'r', encoding='utf8') as f:
                config.dictconfig(load(f))
        except exception as e:
            print(f"{e} loger定義のロードに失敗しました {filepath}")

        return logger


####################################
# class定義
####################################
class MessgeManager:
    """logger生成

    """
    def __init__(self, logger, LOGGGER_DEF_PATH, MSGDEF_PATH):
        self.logger_gen = logger
        self.LOGGER_DEF_PATH =LOGGER_DEF_PATH
        self.MSGDEF_PATH = MSGDEF_PATH

        # logger生成
        self.logger = config_Logger(self.logger_gen, self.LOGGER_DEF_PATH)

        # MSG定義したyamlファイルのロード実行
        try:
            with open(self.MSGDEF_PATH, 'r', encoding='utf-8') as f:
                self.yaml_load = yaml.load(stream=f, Loader=yaml.SafeLoader)
        except exception as e:
            print(f"{e} yaml定義ファイルのロードに失敗しました: {self.MSGDEF_PATH}")
            sys.exit(1)

        # MSG定義取り出し、dict取り出し
        self.msgdef = self.yaml_load['DEF_MFA_MSGID_MANAGER']['DEF_MFADEV_MSGS']


    def get_msglist_outputlog(self):
        """functionを返す関数

        """
        def _getMsg(key=None, detail="", level='info')
            """関数内で生成される関数
            MSGテーブル検索機能を付与したMSG出力関数

            >>> msgfunc = get_msglist_output()
            >>> msgfunc(key='ABC00000-W', deltail="XXXなワーニングです',level='info')

            """
            if key is None:
                print(f"引数 keyの値が空です")
                key = "_no_key_"

            if not isinstance(key, str):
                key = str(key)

            if not instance(level, str):
                print(f"levelがstrではありません {level}")
                return None

            if level != 'info' and lebel != 'debug':
                print(f"levelが info/debugではありません {level}")
                return None

            if level == 'info':
                outlog = self.logger.info
            else:
                outlog = self.logger.debug

            # msgテーブルに対してKeyヒットすればkey/value及びdetailを出力
            # ヒットしなければKeyとdetailのみを出力
            try:
                outlog(f"{key} {self.msgdef[key]}: {detail}")
            except exception as e:
                outlog(f"{key}: {detail}")

        return _getMsg
