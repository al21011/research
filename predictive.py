'''
緊張感・集中力の予測機能実装部分です。
とりあえず長谷川さんが開発に進めるようにコードを書いておきます。
---注意事項---
・pythonの特性上、0の場合でも0.00として下さい。
    例えば緊張感が適切な場合、tension = (1.75-2.25)などです。
・このコードはcontrol + Cで実行を止めることができます。
'''

# estimation.pyでの関数が呼び出せるようになります
import estimation
import time

def main():
    # この変数をカスタマイズして欲しい値にして下さい
    tension_area = (0.00, 3.00)
    concentration_area = (0.00, 3.00)
    
    ### 擬似的に緊張感と集中力を算出します
    while True:
        # これらの値を使って開発を進めて下さい
        tension = round(estimation.random_value(*tension_area), 2)
        concentration = round(estimation.random_value(*concentration_area), 2)
        # 一応出力しておきます
        print('緊張感：' + str(tension))
        print('集中力；' + str(concentration))
        
        '''
        ここ、もしくは冒頭にmain関数以外に関数を定義して予測処理を書きます。
        '''
        
        # 1秒動作を止めます(開発が進み、不要になったタイミングで消して下さい)
        time.sleep(1)

# スクリプトが直接実行された時のみ動作することを保証する書き方です 
if __name__ == '__main__':
    main()