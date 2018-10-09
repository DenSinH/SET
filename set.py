import pygame
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

(width, height) = (1280, 720)
screen = pygame.display.set_mode((width, height))

game_x_lim = 960

shapes = ["square", "circle", "poly"]
amounts = [1, 2, 3]
fills = [85, 170, 255]
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]


class Card(object):

    def __init__(self, shape, amount, fill, color):
        self.shape = shape
        self.amount = amount
        self.fill = fill
        self.color = color

    def __repr__(self):
        return str(shapes[self.shape]) + str(colors[self.color])

    def visual(self, (card_width, card_height)):
        tex = pygame.Surface((card_width, card_height))
        tex.fill((255, 255, 255))

        row_height = card_height // (2*self.amount + 3)
        row_ys = [(2*row + 1)*row_height for row in range(self.amount + 1)]

        (x_min, x_max) = (card_width // 5, card_width - card_width // 5)

        shape_thickness = 0 if self.fill > 0 else 5

        if self.shape == 0:
            for row_y in row_ys:
                pygame.draw.rect(tex, colors[self.color],
                                 [x_min, row_y, (x_max - x_min), card_height // 7], shape_thickness)

        elif self.shape == 1:
            for row_y in row_ys:
                pygame.draw.ellipse(tex, colors[self.color],
                                    [x_min, row_y, (x_max - x_min), card_height // 7], shape_thickness)

        elif self.shape == 2:
            for row_y in row_ys:
                pygame.draw.polygon(tex, colors[self.color], [
                    (x_min, row_y + card_height // 14),
                    (card_width // 2, row_y + card_height // 7),
                    (x_max, row_y + card_height // 14),
                    (card_width // 2, row_y)
                ],
                                    shape_thickness)

        tex.set_alpha(128 if self.fill == 1 else 255)

        return tex




class Game(object):

    def __init__(self):
        self.deck = []
        self.table = []
        self.chosen = []

        for shape in range(3):
            for amount in range(3):
                for fill in range(3):
                    for color in range(3):
                        self.deck.append(Card(shape, amount, fill, color))

        random.shuffle(self.deck)

    def fill(self, extra=0):
        while len(self.table) < 12 + extra:
            self.table.append(self.deck[-1])
            self.deck.pop(-1)

    def check(self):
        Set = False
        for stat in ["shape", "amount", "fill", "color"]:
            stat_set = set([getattr(self.chosen[i], stat) for i in range(3)])
            print stat_set
            if len(stat_set) == 2:
                break
        else:
            print "Correct"
            for card in self.chosen:
                self.table.remove(card)

    def choose(self, index):
        if self.table[index] not in self.chosen:
            self.chosen.append(self.table[index])
            print self.chosen
            print self.table[index]

        if len(self.chosen) == 3:
            self.check()
            self.chosen = []
            self.fill()

    def update(self):
        screen.fill((255, 255, 255))

        card_width = game_x_lim / (len(self.table) / 3)
        card_height = height / 3

        for i in range(len(self.table)):
            x = (i // 3) * card_width
            y = (i % 3) * card_height
            screen.blit(self.table[i].visual((card_width, card_height)), (x, y))
            pygame.draw.rect(screen, (0, 0, 0), (x, y, card_width, card_height), 2)

        for i in range(len(self.chosen)):
            y = i * card_height
            screen.blit(self.chosen[i].visual((card_width, card_height)), (width - card_width, y))
            pygame.draw.rect(screen, (0, 0, 0), (width - card_width, y, card_width, card_height), 2)

        pygame.display.update()



game = Game()
game.fill()

Loop = True
while Loop:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Loop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.fill(3)
            elif event.key == pygame.K_t:
                for i in range(len(game.table)):
                    print game.table[i]

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()

                x_cards = (len(game.table)) // 3
                y_cards = 3
                j = pos[0] // (game_x_lim / x_cards)
                i = pos[1] // (height / y_cards)

                if i <= y_cards and j <= x_cards:
                    print (3*j + i)

                    game.choose((3*j + i))
            else:
                game.chosen = []


    game.update()

    clock.tick(fps)
