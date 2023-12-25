from pytest_mock import mocker
import pytest
import main


def test_func_main(mocker):
    
    mocker.patch('main.func_hoge', return_value=[1, 2])
    print(main.func_main())
    print(main.func_hoge())


##################################################
# 名前空間での違い
# import と from xxx import でmoker.patchでの指定は異なる
##################################################
def test_func_main1(mocker):
    mocker.patch('os.getcwd', return_value='/var/app')
    print(main.func_main1())
    
def test_func_main2(mocker):
    mocker.patch('main.getcwd', return_value='/var/app')
    print(main.func_main2())

##################################################
# 関数/各種メソッド/プロパティの置き換え
# @propertyは留意必要 -> , new_callable=mocker.PropertyMock
##################################################
def test_func_main3(mocker):
    m1 = mocker.patch('os.getcwd', return_value='/var/app')
    m2 = mocker.patch('main.func_sample', return_value =1)
    m3 = mocker.patch('main.Sample.half_value', return_value=11)
    m4 = mocker.patch('main.Sample.get_cvalue', return_value=31)
    m5 = mocker.patch('main.Sample.get_svalue', return_value=41)

    # 差し替えを確認 mocker.patch効果
    # Sampleでの設定との違いを確認!
    main.func_main3()


##################################################
# ダミークラスへ差し替え
# ,new = で指定する
##################################################
class DummyClass:
    ...

def test_func_main4(mocker):
    m6 = mocker.patch('main.Sample', new=DummyClass)
    print(main.Sample)


##################################################
# 戻り値を設定する
##################################################
# 常に同じ値
def test_func_main5(mocker):
    m5 = mocker.patch("main.func_sample", return_value=1)
    print(main.func_sample())

# 実行回数により返る
def test_func_main6(mocker):
    m6 = mocker.patch("main.func_sample", side_effect=[10, 20, 30])
    print(main.func_sample())

# 引数の値によって変える
def test_func_main7(mocker):
    m7 = mocker.patch('main.func_sample', side_effect=lambda x: False if x %2 else True)
    print(main.func_sample(1))


##################################################
# 例外を発生させる 
##################################################
def test_func_main8(mocker):
    m8 = mocker.patch('main.func_sample', side_effect=Exception('new exception'))
    
    # Exceptionを検知
    # matchに期待する文字列を指定できる
    # assertで詳細確認もできる

    # 検証目的により使い分ける
    # 1行で済ますならmatchを使用する
    # いろいろチェックするならassertで柔軟に対応する


    # 通常、特定の例外の発生を確認する場合は pytest.raises を使用し
    # テストが期待されたように失敗することを確認する場合は @pytest.mark.xfail を使用します。

    with pytest.raises(Exception, match='new exception') as e:
        main.func_sample()
    

    with pytest.raises(Exception) as e:
        main.func_sample()
    
    assert 'new exception' in str(e.value)



