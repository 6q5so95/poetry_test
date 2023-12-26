def func_main():
    return func_hoge()

def func_hoge():
    return [x for x in range(10)]

##################################################
# 名前空間での違い
# import と from xxx import でmoker.patchでの指定は異なる
##################################################
import os
def func_main1():
    return os.getcwd()

from os import getcwd
def func_main2():
    return getcwd()

##################################################
# 関数/各種メソッド/プロパティの置き換え
# @propertyは留意必要 -> , new_callable=mocker.PropertyMock
##################################################
def func_main3():
    s = Sample()
    print("")
    print("ライブラリ呼び出し:" + os.getcwd())
    print("関数呼び出し:" + str(func_sample()))
    print("インスタンスメソッド呼び出し:" + str(s.half_value()))
    print("プロパティ呼び出し:" + str(s.value))
    print("クラスメソッド呼び出し:" + str(Sample.get_cvalue()))
    print("スタティックメソッド呼び出し:" + str(Sample.get_svalue()))
    print("")

def func_sample():
    return 0

class Sample:
    __cvalue = 30
    
    def __init__(self):
        self.__value = 20

    def half_value(self):
        return int(self.__value / 2)
    
    @property
    def value(self):
        return self.__value
    
    @classmethod
    def get_cvalue(cls):
        return cls.__cvalue
    
    @staticmethod
    def get_svalue(self):
        return 40

