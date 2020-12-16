import pygame as pg
from settings import *
import random
import os

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.sjump = False
        self.doublej = False
        self.image = pg.image.load(os.path.join('img_folder', 'santa.png')).convert()
        self.image.set_colorkey(BLACK)
        self.image = pg.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()

        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)  # Geschwindigkeit
        self.acc = vec(0, 0)  # Beschleunigung

    def update(self):
        self.acc = vec(0, 0.8)  # x-Achse Beschleunigung 0, y-Achse beschleunigung 0.8
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:  # nach links
            self.acc.x = -PLAYER_ACC
            self.image = pg.image.load(os.path.join('img_folder', 'santa.png')).convert()
            self.image.set_colorkey(BLACK)
            self.image = pg.transform.scale(self.image, (70, 70))
        if keys[pg.K_RIGHT]:  # nach rechts
            self.acc.x = PLAYER_ACC
            self.image = pg.image.load(os.path.join('img_folder', 'santa2.png')).convert()
            self.image.set_colorkey(BLACK)
            self.image = pg.transform.scale(self.image, (70, 70))
        # x Koordinate ausrechnen
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        self.rect.midbottom = self.pos

    def jump(self):
        self.sjump = False
        # stellt fest, ob Player auf der Plattform steht
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, g.platforms, False)
        self.rect.x -= 1
        if hits:
            self.game.jump_sound.play()
            self.vel.y = -20  # jump
            self.doublej = True
        elif self.doublej:
            self.vel.y = -15
            self.doublej = False

    def jump_short(self):
        if self.vel.y < -3 and self.sjump == False:
            self.vel.y = -3

    def superjump(self):
        self.sjump = True
        self.game.jump_sound.play()
        self.vel.y = -50

    # def doublejump(self):
    #     if self.doublej:
    #         self.vel.y = -15
    #         self.doublej = False


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)

        self.game = game
        # Bilder der Plattform
        images = [pg.image.load(os.path.join('img_folder', 'ice1.png')).convert(),
                  pg.image.load(os.path.join('img_folder', 'ice2.png')).convert(),
                  pg.image.load(os.path.join('img_folder', 'ice3.png')).convert()]

        self.image = random.choice(images)
        self.image.set_colorkey(BLACK)
        self.image = pg.transform.scale(self.image, (random.randint(70, 150), random.randint(30, 50)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Gift(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load(os.path.join('img_folder', 'gift.png'))
        self.image.set_colorkey(BLACK)
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y


class Gold_Apple(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load(os.path.join('img_folder', 'goldapple.png'))
        self.image.set_colorkey(BLACK)
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y


class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        if direction == 1:
            self.image = pg.image.load(os.path.join('img_folder', 'enemy_left.png'))
            x -= 10
        else:
            self.image = pg.image.load(os.path.join('img_folder', 'enemy.png'))
        self.image.set_colorkey(BLACK)
        self.image = pg.transform.scale(self.image, (80, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hoehe = y
        self.speed = direction * random.randint(1, 3)

    def update(self):
        self.rect.x += self.speed
        if self.rect.y >= self.hoehe:
            self.rect.y -= 11
        self.rect.y += 10.6

    def change_pos(self, n):
        self.rect.y += n
        self.hoehe += n


class Bomb(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load(os.path.join('img_folder', 'bomb1.png'))
        self.image.set_colorkey(BLACK)
        self.image = pg.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.hit = False
        self.exploding = False
        self.countdown = 60
        self.explodcountdown = 60
        self.up = True
        self.slowdown = 0

    def update(self):
        if self.hit:
            if self.countdown == 0:
                if self.exploding == False:
                    self.image = pg.image.load(os.path.join('img_folder', 'explosion.png'))
                    self.image.set_colorkey(BLACK)
                    self.image = pg.transform.scale(self.image, (100, 100))
                    self.exploding = True
                if self.explodcountdown != 0:
                    self.explodcountdown -= 1
                else:
                    self.kill()
            else:

                self.countdown -= 1
                self.slowdown += 1
                if self.slowdown % 5 == 0:
                    if self.up:
                        self.rect.y += 11
                        self.up = False
                    else:
                        self.rect.y -= 11
                        self.up = True


class Game:
    # Fenster und Clock werden initialisiert
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('JUMP!')
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)

        self.load_data()

    def load_data(self):
        self.dir = os.path.dirname(__file__)

        filepath = os.path.join(self.dir, HS_FILE)
        with open(filepath, 'r')as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        self.snd_dir = os.path.join(self.dir, 'snd')
        self.jump_sound = pg.mixer.Sound(os.path.join(self.snd_dir, 'Jump33.wav'))  # Jump Musik
        self.background = pg.transform.scale(
            pg.image.load(os.path.join(self.dir, 'img_folder', 'background.jpg')).convert(), (WIDTH, HEIGHT))

    # eine neue Runde starten
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.enemy = pg.sprite.Group()
        self.player = Player(g)
        self.all_sprites.add(self.player)
        # Plattform wird erzeugt
        for plat in PLATFORM_LIST:
            p = Platform(self, *plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.score = 0
        self.run()

    # game loop
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)  # FPS
            self.events()  # reagirt auf input
            self.update()  # aktualisieren
            self.draw()  # anzeigen

    # aktualiseren
    def update(self):
        self.all_sprites.update()
        # Kollisionserkennung, solang Player im Fenster ist(y >0)
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit  # kleinster Wert

                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top + 1
                        self.player.vel.y = 0
        for each in self.enemy:
            if each.rect.top >= HEIGHT or each.rect.right <= 0 or each.rect.left >= WIDTH or each.rect.bottom <= 0:
                each.kill()
        # item Kollision
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        if hits:

            if hits[0].__class__.__name__ == "Gift":
                self.score += 50
                hits[0].kill()
            elif hits[0].__class__.__name__ == "Gold_Apple":
                self.player.superjump()
                hits[0].kill()
            elif hits[0].__class__.__name__ == "Bomb":
                if hits[0].exploding == False:
                    hits[0].hit = True
                else:
                    self.playing = False
        # enemy Kolission
        hits = pg.sprite.spritecollide(self.player, self.enemy, False)
        if hits:
            self.playing = False

        # Player im oberen Teil des Fensters
        if self.player.rect.top <= HEIGHT / 4:
            # player.y
            self.player.pos.y += abs(self.player.vel.y)  # abs = Betrag
            # Plattform ausserhalb des Fensters werden geloescht
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10
            for i in self.items:
                i.rect.y += abs(self.player.vel.y)
                if i.rect.top >= HEIGHT:
                    i.kill()

            for each in self.enemy:
                each.change_pos(abs(self.player.vel.y))

        # Tod - Player.bottem > Hoehe des Fensters
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)  # Plattform nach oben
                if sprite.rect.bottom < 0:
                    sprite.kill()  # Plattform ausserhalb des Fensters werden geloescht
        if len(self.platforms) == 0:  # keine Plattform = Tod
            self.playing = False

        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            # Plattform werden im bestimmten Bereich erzeugt
            p = Platform(self, random.randrange(0, WIDTH - width),
                         random.randrange(-100, -30))

            hits = pg.sprite.spritecollide(p, self.platforms, False)
            if hits:
                p.kill()
            else:
                self.platforms.add(p)
                self.all_sprites.add(p)
                chance = random.randint(0, 20)
                if chance > 19:
                    choice = random.choice(['gift', 'apple'])
                    x = p.rect.centerx + random.randint(-5, 5)
                    y = p.rect.top
                    if choice == 'gift':
                        gift = Gift(g, x, y)
                    else:
                        gift = Gold_Apple(g, x, y)
                    self.all_sprites.add(gift)
                    self.items.add(gift)
                if chance == 10:
                    x = p.rect.centerx - 30
                    y = p.rect.top
                    bomb = Bomb(g, x, y)
                    self.all_sprites.add(bomb)
                    self.items.add(bomb)
        chance = random.randint(0, 200)
        if chance == 1 and not self.player.sjump:
            side = random.choice([0, WIDTH])
            if side == 0:
                enemy = Enemy(g, side, random.randint(0, HEIGHT), 1)
            else:
                enemy = Enemy(g, side, random.randint(0, HEIGHT), -1)
            self.enemy.add(enemy)
            self.all_sprites.add(enemy)

    def events(self):
        for event in pg.event.get():
            # Exit
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            # Jump
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    # if self.player.doublej:
                    #     self.player.doublejump()
                    # else:
                    #     self.player.jump()
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_short()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)
        # self.items.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)  # Punktzahl
        pg.display.flip()

    def show_start_screen(self):
        pg.mixer.music.load(os.path.join(self.snd_dir, 'purple_people_eater.mp3'))
        # wiederholen
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Left and right button move, space bar jump ", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press space bar to jump higher ", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 30)
        self.draw_text("Press any key to start the game", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BGCOLOR)

        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)

        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)

            with open(os.path.join(self.dir, HS_FILE), 'w')as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)

        pg.display.flip()

        self.wait_for_key()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def wait_for_key(self):
        waiting = True

        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()
pg.quit()
