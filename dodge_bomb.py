import time
import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = { #移動量辞書
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (5,0),
    }


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect、または爆弾Rect
    戻り値：x方向、y方向の画面内判定結果
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True #初期値：画面内
    if rct.left < 0 or WIDTH < rct.right: #x方向の画面外判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  #y方向の画面外判定
        tate = False
    return yoko, tate #x方向、y方向の画面内判定結果を返す


def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー時に，半透明の黒い画面上に「Game Over」と表示し，泣いているこうかとん画像を貼り付ける関数
    """
    print("ゲームオーバー")
    go_img = pg.Surface((WIDTH, HEIGHT))  #空のSurface
    pg.draw.rect(go_img, (0, 0, 0), (0, 0, 20, 20)) #黒い四角を描画

    go_img.set_alpha(100) #半透明に設定
    screen.blit(go_img, (0, 0))
    cry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9) #泣いているこうかとん画像
    cry_rct = cry_img.get_rect()
    screen.blit(cry_img, [350, 300]) #泣いているこうかとん画像を貼り付ける
    screen.blit(cry_img, [710, 300]) #半透明の黒い画面を貼り付ける
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255)) #ゲームオーバーの文字
    txt_rct = txt.get_rect()
    txt_rct.center = [550, 330]
    screen.blit(txt, txt_rct)
    pg.display.update() #画面更新


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) #空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) #赤い円を描画
    bb_img.set_colorkey((0, 0, 0)) #黒色を透明色に設定
    bb_rct = bb_img.get_rect() #爆弾Rectを取得
    bb_rct.centerx = random.randint(0, WIDTH) #爆弾のx座標を設定
    bb_rct.centery = random.randint(0, HEIGHT) #爆弾のy座標を設定
    vx, vy = +5, +5 #爆弾の移動速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct): #こうかとんRectと爆弾Rectの衝突判定
            gameover(screen)
            time.sleep(5)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) #移動を打ち消す
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy) #爆弾の移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
