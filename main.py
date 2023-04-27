import pygame as pygame
import random

pygame.init()
pygame.font.init()

PLAYER_SPRITE = pygame.image.load('data/vfx/player.png')
MOB_SPRITES = [pygame.image.load(
    'data/vfx/mob.png'), pygame.image.load('data/vfx/mob_2.png'), pygame.image.load('data/vfx/mob_3.png')]
COIN_SPRITE = pygame.image.load('data/vfx/coin.png')
BUTTON_IMAGE = pygame.image.load('data/vfx/button.png')
START_IMAGE = pygame.image.load('data/vfx/start_button.png')
NULL_INDICATOR_IMAGE = pygame.image.load('data/vfx/null_indicator.png')
SPEED_INDICATOR_IMAGE = pygame.image.load(
    'data/vfx/shooting_speed_indicator.png')
VELOCITY_INDICATOR_IMAGE = pygame.image.load('data/vfx/velocity_indicator.png')

FONT = pygame.font.SysFont(pygame.font.get_default_font(), 40)

COIN_SOUND = pygame.mixer.Sound('data/sfx/coin.wav')
LASER_SOUND = pygame.mixer.Sound('data/sfx/laser.wav')
HIT_SOUND = pygame.mixer.Sound('data/sfx/hit.wav')
LEVELUP_SOUND = pygame.mixer.Sound('data/sfx/levelup.wav')
NO_SOUND = pygame.mixer.Sound('data/sfx/no.wav')

WIDTH, HEIGHT = 1240, 660
WHITE = (255, 255, 255)
YELLOW = (230, 210, 0)
SHOP_BG_COLOR = (105, 105, 85)

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(PLAYER_SPRITE)
pygame.display.set_caption('StarBlower')

clock = pygame.time.Clock()
running = True


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_SPRITE
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2, HEIGHT-50)
        self.vel = 2
        self.shot_vel = 5
        self.rect = window.blit(self.image, self.rect)

    def draw(self, win):
        self.rect = win.blit(self.image, self.rect)


class Shot(pygame.sprite.Sprite):
    def __init__(self, xy, vel):
        super().__init__()
        self.position = pygame.Vector2()
        self.position.xy = xy
        self.vel = vel
        self.color = (233, 101, 3)  # (233, 60, 3)
        self.radius = 4
        self.rect = pygame.draw.circle(
            window, self.color, self.position, self.radius)

    def draw(self, win):
        self.rect = pygame.draw.circle(
            win, self.color, self.position, self.radius)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(MOB_SPRITES)
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        # self.position.xy = WIDTH//2, 50
        self.vel = 3

    def draw(self, win):
        self.rect = win.blit(self.image, self.rect)


class Coin(pygame.sprite.Sprite):
    def __init__(self, xy, value):
        super().__init__()
        self.image = COIN_SPRITE
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.vel = 3
        self.value = value

    def draw(self, win):
        self.rect = win.blit(self.image, self.rect)


class Button:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.price = 1
        self.level = 1
        self.typeIndicatorSprite = NULL_INDICATOR_IMAGE


def draw_money_count():
    money_text = FONT.render(f"{money}", 1, YELLOW)
    window.blit(money_text, (WIDTH - money_text.get_width() -
                10, HEIGHT - money_text.get_height() - 10))
    window.blit(COIN_SPRITE, (WIDTH - money_text.get_width() -
                10 - COIN_SPRITE.get_width()-3, HEIGHT - money_text.get_height() - 10))


def draw_game():
    draw_money_count()

    # moving stuff
    player.draw(window)

    for shot in shots:
        shot.draw(window)

    for mob in mobs:
        mob.draw(window)

    for coin in coins:
        coin.draw(window)

    pygame.display.update()


def spawn_mob():
    mob = Mob()
    mob.rect.x, mob.rect.y = random.randrange(
        0, WIDTH - mob.size[0], mob.size[0]), -mob.size[1]
    mobs.append(mob)


money = 0
SHOT_INTERVAL = 70
player = Player()
shots = []
had_shot = 70
mobs = []
coins = []
spawn_mob()
spawned = 0
spawn_wait = 80
dead = False

start_button = Button(START_IMAGE)
start_button.rect.center = WIDTH//2, HEIGHT*2//3
START_TEXT = FONT.render("START", 1, WHITE)

upgrade_buttons = []
for i in range(3):
    button = Button(BUTTON_IMAGE)
    offset = 0
    if i == 0:
        offset = - (button.rect.width+10)
    elif i == 2:
        offset = (button.rect.width+10)
    button.rect.center = WIDTH//2 + offset, HEIGHT//3
    upgrade_buttons.append(button)
upgrade_buttons[0].typeIndicatorSprite = VELOCITY_INDICATOR_IMAGE
upgrade_buttons[1].typeIndicatorSprite = SPEED_INDICATOR_IMAGE


while running:
    clock.tick(60)

    if not dead:
        # clock.tick(60)
        window.fill((19, 10, 31))

        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                # if (btn.collidepoint((mouseX, mouseY))):
                #     pass
            elif e.type == pygame.QUIT:
                running = False

        # end event handling

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.rect.x > 0:
            player.rect.x -= player.vel
        if keys[pygame.K_RIGHT] and player.rect.right < WIDTH:
            player.rect.x += player.vel
        if keys[pygame.K_UP] and player.rect.y > 0:
            player.rect.y -= player.vel
        if keys[pygame.K_DOWN] and player.rect.bottom < HEIGHT:
            player.rect.y += player.vel
        if keys[pygame.K_SPACE]:
            if had_shot > SHOT_INTERVAL:
                LASER_SOUND.play()
                shots.append(Shot(
                    (player.rect.x + player.size[0]//2, player.rect.y), player.shot_vel))
                had_shot = 0
        had_shot += 1
        
        shot_rects = pygame.sprite.Group(*shots)
        for mob in mobs:
            mob.rect.y += mob.vel
            if shot := pygame.sprite.spritecollideany(mob, shot_rects):
                coins.append(Coin(mob.rect.center, 1))
                HIT_SOUND.play()
                mobs.remove(mob)
                try:
                    shots.remove(shot)
                except ValueError as err:
                    print(err)
                    
        
        for shot in shots:
            if shot.position.y > 0:
                shot.position.y -= shot.vel
            else:
                shots.pop(shots.index(shot))


        for coin in coins:
            coin.rect.y += coin.vel
            if pygame.sprite.collide_rect(player, coin):
                COIN_SOUND.play()
                money += coin.value
                coins.remove(coin)

        mob_rects = pygame.sprite.Group(*mobs)

        if s := pygame.sprite.spritecollideany(player, mob_rects):
            print(s)
            dead = True

        spawned += 1
        if spawned > spawn_wait:
            spawn_mob()
            spawned = 0
            spawn_wait = spawn_wait * 0.96

        draw_game()
        
    else:
        window.fill(SHOP_BG_COLOR)

        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                if (start_button.rect.collidepoint((mouseX, mouseY))):
                    player.rect.center = (WIDTH//2, HEIGHT-50)
                    shots = []
                    had_shot = 31
                    mobs = []
                    coins = []
                    spawn_mob()
                    spawned = 0
                    spawn_wait = 80
                    dead = False
                else:
                    for button in upgrade_buttons:
                        if button.rect.collidepoint((mouseX, mouseY)):
                            if button.price <= money:
                                LEVELUP_SOUND.play()
                                money -= button.price
                                button.price = round(button.price * 1.8)
                                button.level += 1
                                if upgrade_buttons.index(button) == 0:
                                    player.vel = round(player.vel * 1.3)
                                elif upgrade_buttons.index(button) == 1:
                                    SHOT_INTERVAL = round(SHOT_INTERVAL * 0.8)
                                elif upgrade_buttons.index(button) == 2:
                                    player.shot_vel = round(
                                        player.shot_vel * 1.3)
                            else:
                                NO_SOUND.play()

            elif e.type == pygame.QUIT:
                running = False

        window.blit(start_button.image, start_button.rect)
        window.blit(START_TEXT, (start_button.rect.centerx - START_TEXT.get_width() //
                    2, start_button.rect.centery - START_TEXT.get_height()//2))

        for button in upgrade_buttons:
            window.blit(button.image, button.rect)
            # DISPLAY.blit(button.sprite, (220 + (buttons.index(button)*125), 393))
            priceText = FONT.render(str(button.price), True, YELLOW)
            window.blit(priceText, (42 + button.rect.x, button.rect.y + 20))
            levelText = FONT.render(
                'Lvl. ' + str(button.level), True, (100, 100, 100))
            window.blit(levelText, (14 + button.rect.x, button.rect.y + 48))
            window.blit(button.typeIndicatorSprite,
                        (-18 + button.rect.x, button.rect.y))

        pygame.display.update()


# end main loop
pygame.quit()
