### ----------------------- library --------------------------------
import time
import random
import sys
import math

### ----------------------- class ----------------------------------

class Card :
    SUITS   = ("Spd-","Hrt-","Dmd-","Clb-")
    NUMBERS = ("A","2","3","4","5","6","7","8","9","10","J","Q","K")
    POINTS  = (1,2,3,4,5,6,7,8,9,10,10,10,10)

    def __init__(self,sui,num) -> None: # Card( i, j )がCardクラスの構造
        self.sui = sui                  # iがスート、jが数字を特定する
        self.num = num
        self.poi = num

    def __str__(self) -> str:   #スート+数字を返す
        return self.SUITS[self.sui] + self.NUMBERS[self.num]

    def point(self) -> int:     #点数のみを返す
        return self.POINTS[self.poi]

    def number(self) -> str:    #数字のみを返す(Aがあるかの判定を行う時に使う)
        return self.NUMBERS[self.num]



class Player :
    def __init__(self,name:str) -> None:
        self.name = name                #プレーヤの名前
        self.hand :list = []            #手札リスト Cardクラスのみが入る
        self.chip :int = 0              #現在のチップの総額
        self.betted_chip :int = 0       #ベットしたチップの額
        self.match_result :float = None #勝敗の結果 そのまま掛け金に対するレートになる
        #                                正なら勝ち、負なら負け、0なら引き分け


    ## 手札に関するメソッド--------------------------------------------
    def add_draw_card(self, dck:list) -> None: #山札からカードを1枚引いて手札に加える
        card = random.choice(dck)
        self.hand.append(card)
        dck.remove(card)


    def sum_points(self) -> int:    #手札の点数の合計を返す
        poi_list = [ p.point() for p in self.hand ] #手札の点数だけを抽出したリスト
        total = sum( poi_list )

        if total <= 11  and  1 in poi_list:
            return total+10             #Aは1点として計算し、合計11点以下ならば10点を加算する
        else:
            return total


    def show_hand(self) -> None:    #手札を表示する 伏せ札なし
        hand_list = [ c.__str__() for c in self.hand ]

        print( f"{self.name :>6s} : {hand_list}",   #手札
               f" total: {self.sum_points()}",      #点数
               f" chip: {self.chip}$" )             #チップ


    def hide_hand(self) -> None:    #手札を表示する 伏せ札あり
        return self.show_hand()     #プレーヤーなので全て表


    ## チップに関するメソッド--------------------------------------------
    def bet(self) -> None:      #ベットする額を入力させる
        print( f"\n{self.name}: How much to bet  1~{self.chip}" )

        bt = input()
        try:
            bt = int(bt)
        except:         #整数以外が入力された時の処理
            print( "\n!!!---Please enter integer---!!!" )
            return self.bet()

        if ( bt < 0 ) or ( self.chip < bt ):    #所持チップの範囲外の額が入力された時の処理
            print( f"\n!!!---Please enter 1~{self.chip}---!!!" )
            return self.bet()
        else:
            self.betted_chip = bt
            print( f"{self.name} bet {self.betted_chip}$" )


    def chip_move(self, rate:float) -> int:         #勝敗決定後のチップの移動
        self.chip += int( self.betted_chip *rate )  #rateは配当倍率 負の値なら敗け 端数は0へ丸める
        return int( self.betted_chip *rate ) *-1    #ディーラーのチップ増減量を返す


    def no_chips(self) -> bool: #チップが無くなったかの判定
        if self.chip < 1:
            print( f"{self.name} have no chips " )
            return True
        else:
            return False


    ## ヒット・スタンド--------------------------------------------
    def hit_or_stand(self, mems_li, dck) -> None:
        while True:
            print( "\nHit, Stand, DoubleDown or Surrender?" )
            select = input ( "h / s / d / rr\n" )

            if select == "s":           #standするとループ終了
                break

            elif select == "h":         #hitで1枚ドロー
                self.add_draw_card( dck )

            elif select == "d":         #double downで1枚ドローしてループ終了
                self.add_draw_card( dck )
                if self.betted_chip *2 <= self.chip:
                    self.betted_chip *= 2           #掛け金を2倍
                else:                               #掛け金を2倍にして総チップ額を超えるなら
                    self.betted_chip = self.chip    #チップを全てベット
                hide_all_hands( mems_li )
                return

            elif select == "rr":        #surrender ベットの半額を支払って負け
                self.match_result = LOSE*0.5
                break

            else:
                print( "!!!----Invalid input----!!!" )    #入力値が不正

            hide_all_hands( mems_li )

            if self.sum_points() > 21:          #プレーヤーのバストは負け確定
                time.sleep(0.5)
                print( f"{self.name} : Bust" )
                self.match_result = LOSE
                return
            elif self.sum_points() == 21:       #ディーラーと同じ21点ならプレーヤーの勝利なので
                self.match_result = WIN         #ここで勝ちを確定する
                return



class Dealer (Player):
    ## ディーラー専用の動作
    def hide_hand(self) -> None:
        print( f"{self.name :>6s} : ['{self.hand[0]}', '???-?']",
                " total: ??",
               f" chip: {self.chip}$" )
        #手札の1枚目だけ表示して点数も伏せる


    def bet(self) -> None:
        pass


    def chip_move(self, amount:int) -> None:    #amountにPlayer.chip_move(rate)を入れて使う
        self.chip += amount             #Player.cip_move()の返り値だけ増額(負の数なら減額)


    def no_chips(self) -> bool:
        if self.chip < 1:
            print( f"{self.name} has no chips " ) # haveをhasに変更
            print( "quit the game..." )
            sys.exit
        else:
            return False


    def hit_or_stand(self, mems_li, dck) -> None:
        while self.sum_points() <= 17:      #ディーラーは17点以上になるまで強制ヒット
            #                                かつ17点以上になれば強制スタンド
            print( f"{self.name} hit..." )
            self.add_draw_card(dck)
            time.sleep(1)

            if self.sum_points() > 21:
                print( f"{self.name} : Bust" )

                mem:Player|Npc
                for mem in mems_li:      #ディーラーがバストしたのでバストしてないプレーヤー全員勝利
                    if mem.match_result == None:    # この時点で勝敗が決定していないプレーヤーを
                        mem.match_result = WIN      # 勝利とする
                        #ディーラーがバストした時点で勝敗が決しているプレイヤーはバストかナチュラル21
                        #ディーラーのmatch_resultにWIN(1.0)が入るが使わないので無視する



class Npc (Player):
    ## NPC専用の動作
    def hide_hand(self) -> None:
        print( f"{self.name :>6s} : ['???-?', '???-?']",
                " total: ??"
               f" chip: {self.chip}$" )


    def no_chips(self) -> bool:
        if self.chip < 1:
            print( f"{self.name} has no chips " ) # haveをhasに変更
            return True
        else:
            return False


    def bet(self) -> None:
        self.betted_chip = math.ceil( self.chip *0.5 )
        print( f"{self.name} bet {self.betted_chip}$" )


    def hit_or_stand( self, mems_li, dck ) -> None:
        dlr:Dealer = mems_li[-1]
        up_card = dlr.hand[0]               #アップカード:ディーラーの表向きのカードの事

        while self.sum_points() <= 21:      #このループの中身がNPCのヒット・スタンドの基準
            time.sleep(1)                   #アップカードによって基準を変えるのもあり
            if self.sum_points() <= 17:
                print( f"{self.name} hit..." )
                self.add_draw_card( dck )

            elif ( self.sum_points() > 17 ):
                print( f"{self.name} stand" )
                time.sleep(1)
                break

        if self.sum_points() > 21:
            print( f"{self.name} : Bust" )
            self.match_result = LOSE
        elif self.sum_points() == 21:
            self.match_result = WIN
            return


### ----------------------- function -------------------------------

WIN :float = 1.0
LOSE:float = -1.0
PUSH:int   = 0

def judge_natural_21( plr_li:list ) -> None:
    time.sleep(1)
    dlr:Dealer = plr_li[-1]
    plr:Player

    if dlr.sum_points() == 21:
        print( f"\n{dlr.name} : Natural BlackJack" )

    for plr in plr_li:
        if dlr.sum_points() == 21:

            if plr.sum_points() == 21:
                print( f"\n{plr.name} : Natural BlackJack" )
                plr.match_result = PUSH
            else:
                plr.match_result = LOSE*2.5

        else:

            if plr.sum_points() == 21:
                print( f"\n{plr.name} : Natural BlackJack" )
                plr.match_result = WIN*2.5
            else:
                pass


def result( plr:Player|Npc, dlr:Dealer ):   #勝敗処理
    time.sleep(1)

    if plr.match_result > 0:
        print( f"{plr.name} Win  +{plr.betted_chip}$" )     #勝敗表示
    elif plr.match_result < 0:
        print( f"{plr.name} Lose  -{plr.betted_chip}$" )
    else:
        print( f"{plr.name} Push  ±0$" )

    dlr.chip_move( plr.chip_move( plr.match_result ) )      #チップの移動
    plr.betted_chip  = 0                                    #ベット額をリセット


def continue_game( usr, plys_li ) -> bool:
        if not( usr in plys_li ):       #プレーヤーがリストから削除された場合
            print( "quit the game?   y/n" )
            ans = input()
            if ans == "y":
                sys.exit
            elif ans == "n":
                pass
            else:
                return continue_game( usr,plys_li )


def show_all_hands( mems_li:list ) -> None:
    member:Player
    print()
    for member in mems_li:
        member.show_hand()

def hide_all_hands( mems_li:list ) -> None:
    member:Player
    print()
    for member in mems_li:
        member.hide_hand()


### ----------------------------------------------------------------




""" def test(): #テスト用プログラム
    deck = [Card(i,j) for i in range(4)  for j in range(13)]
    player = Player("You")
    player.chip = 10
    dealer = Dealer("Dlr")
    dealer.chip = 30

    for i in range(2):
        player.add_draw_card(deck)
        dealer.add_draw_card(deck)

    player.show_hand()
    player.add_draw_card(deck)
    player.show_hand()
    # player.bet()
    # dealer.chip_move(player.chip_move(True))
    # print(player.chip)
    # print(dealer.chip)

test() """