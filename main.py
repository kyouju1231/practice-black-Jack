### ブラックジャック
""" バージョンアップ履歴
ver1.0 : 点数のみで計算
ver1.1 : Cardクラスを実装
ver1.2 : Aを1点と11点どちらでも計算できるように点数計算を変更
ver1.3 : メインプログラムをdef main():へ格納
         Chipクラスを実装しPL,DE間でチップのやり取りを可能に
ver2.0 : クラス、関数を整理
         Player,Dealerクラスを作成し、手札・チップ・ベットを管理
ver2.1 : result関数を作成
         ダブルダウン、サレンダーを実装
ver2.2 : Npcクラスを作成
ver3.0 : クラス・関数をlibraryファイルへ分割
 """

### ----------------------- library --------------------------------

from library import Card, Player, Dealer, Npc
from library import judge_natural_21, result, continue_game, show_all_hands, hide_all_hands
from library import WIN, LOSE, PUSH

import time, sys

### ----------------------- main -----------------------------------

def main():

    user   = Player( "You" )
    npc1   = Npc   ( "NPC1" )
    dealer = Dealer( "Dealer" )
    user.chip   = 10
    npc1.chip   = 10
    dealer.chip = 100

    deck = []
    players_list:list = [ user, npc1 ]      #そのうちNPCの人数も可変にしたい
    members_list:list = players_list + [dealer]
    #ディーラー以外のplayers_listとディーラー含めたmembers_list
    #ディーラー以外にまとめて処理をするために分けておく
    #また、リストの最後にディーラーを配置してNPCが増えた時もlist[-1]でアクセスしやすくしておく


    while True:

        if len( deck ) < 17:                #山札の枚数が減ったら山札を作り直す
            deck = [ Card(i,j) for i in range(4)  for j in range(13) ]

        member:Player|Npc|Dealer

        for member in members_list:
            if member.no_chips() == True:       # チップが無いメンバーは
                players_list.remove( member )   # ゲームに参加不可、リストから削除する
                members_list.remove( member )

        if len( players_list ) == 0:
            print( "All Players Lose" )
            print( "quit the game..." )
            sys.exit

        continue_game( user, players_list)
        #ユーザーがリストから削除された場合にゲームを止めるか聞く


        for member in members_list:         #ベットと2枚ドロー
            member.bet()
            member.add_draw_card( deck )
            member.add_draw_card( deck )

        hide_all_hands( members_list )      #一部伏せて手札を表示


        judge_natural_21( members_list )    #ナチュラル21判定
        #ここで21点ならば match_result に数字が入る


        for member in members_list:         #ヒット・スタンド
            if member.match_result == None: #勝敗が未決ならヒット・スタンドを実行
                member.hit_or_stand( members_list, deck )


        player:Player|Npc

        for player in players_list:         #点数を比較して勝敗を決定する
            if player.match_result == None: #まだ勝敗が決定してない場合
                if player.sum_points() > dealer.sum_points():
                    player.match_result = WIN
                elif player.sum_points() < dealer.sum_points():
                    player.match_result = LOSE
                else:
                    player.match_result = PUSH


        print("Open hands...")
        time.sleep(1.5)
        show_all_hands( members_list )      #全員の手札の開示

        for player in players_list:
            result( player, dealer )        #チップの移動と勝敗結果の表示

        for member in members_list:
            member.match_result = None      #勝敗結果をリセット
            member.hand = []                #手札を初期化


if __name__ == "__main__":
    main()