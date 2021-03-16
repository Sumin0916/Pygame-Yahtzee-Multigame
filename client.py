import pygame as pg
import random
import os
import time
import copy

pg.init()

HOLD = 0
WAIT = 1
WIDTH = 500
HEIGHT = 700
DICE_NUM = 5
DICE_LEN = 50
SCORE_BOARD = [-1] * 13
CATEGORIES = [
    "aces", "twos", "threes", "fours", "fives", "sixs", "bonus",
    "four_of_a_kind", "full_house", "small_straight", "large_straight",
    "chance", "yahtzee"
]

white = (255, 255, 255)
black = (0, 0, 0)
client_number = 0

base_path = os.path.join(os.path.dirname(__file__))
img_base_path = os.path.join(base_path, "source/img/")
sound_base_path = os.path.join(base_path, "source/sounds/")

dice_img = [
    pg.image.load(os.path.join(img_base_path, "diceOne.png")),
    pg.image.load(os.path.join(img_base_path, "diceTwo.png")),
    pg.image.load(os.path.join(img_base_path, "diceThree.png")),
    pg.image.load(os.path.join(img_base_path, "diceFour.png")),
    pg.image.load(os.path.join(img_base_path, "diceFive.png")),
    pg.image.load(os.path.join(img_base_path, "diceSix.png"))
]

rolling_dice_sound = pg.mixer.Sound(os.path.join(sound_base_path, "rolling_dice.ogg"))

win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Yahtzee~!")
clock = pg.time.Clock()


class Player(object):
    def __init__(self, name):
        self.name = name
        self.dices = [Dice(n) for n in range(1, 6)]
        self.storage = [0, 0, 0, 0, 0]

    def roll_remain_dices(self):
        for i, dice in enumerate(self.dices):
            dice.roll()
            self.storage[i] = dice.num

    def draw_all_dices(self):
        for d in self.dices:
            d.draw()


class Dice(object):
    def __init__(self, order):
        self.num = random.randint(1, 6)
        self.stat = WAIT
        self.order = order
        self.img_adjustment()

    def roll(self):
        if self.stat == WAIT:
            self.num = random.randint(1, 6)
            self.img_adjustment()

    def turn_stat(self):
        if self.stat:
            self.stat = HOLD

        else:
            self.stat = WAIT

    def img_adjustment(self):
        self.img = dice_img[self.num-1]
        self.img = pg.transform.scale(self.img, (DICE_LEN, DICE_LEN))
        self.img_rect = self.img.get_rect()
        self.img_rect.centerx = (WIDTH / DICE_NUM) * self.order - DICE_LEN
        self.img_rect.centery = HEIGHT / 2

    def draw(self):
        win.blit(self.img, self.img_rect)
        pg.display.update()


class ScoreBoard(object):
    def __init__(self, name, num_list):
        self.name = name
        self.visible_board = SCORE_BOARD
        self.score_board = SCORE_BOARD
        self.num_list = num_list

    def record_score(self, categories, score):
        self.score_board[categories] += score
        self.visible_board = copy.deepcopy(self.score_board)

    def cal_categories(self):
        # modifiable_score_list = list(filter(lambda x: x[1] == -1, self.score_board))
        print(self.visible_board)


def draw_window(win):
    win.fill(black)
    pg.display.update()


def main():
    running = True
    draw_window(win)
    p1 = Player("Sumin")
    t = ScoreBoard("Sumin", [1, 2, 3, 4, 5])
    t.cal_categories()
    t1 = ScoreBoard("Sumin", [1, 1, 2, 2, 3])
    t1.cal_categories()
    while running:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()

        p1.draw_all_dices()
        p1.roll_remain_dices()
        time.sleep(2)
        p1.draw_all_dices()


main()
