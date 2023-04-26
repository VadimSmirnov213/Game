import pygame, sys, time, random, colorsys, math


class Background:
    def __init__(self):
        self.sprite = pygame.image.load('data/gfx/background.png')
        self.sprite_nocolor = pygame.image.load('data/gfx/background.png')
        self.position = 0

    def give_sprite(self, tint):
        copy = self.sprite_nocolor.copy()
        color = colorsys.hsv_to_rgb(tint, 1, 1)
        k = (color[0] * 255, color[1] * 255, color[2] * 255)
        copy.fill(k, special_flags=pygame.BLEND_ADD)
        self.sprite = copy


class Player:
    pos = pygame.Vector2()
    pos.xy = 295, 100
    veloc = pygame.Vector2()
    veloc.xy = 3, 0
    accelerat = 0.1
    rightsprite = pygame.image.load('data/gfx/player.png')
    leftsprite = pygame.transform.flip(rightsprite, True, False)
    currentsprite = rightsprite


class Carrot:
    def __init__(self):
        self.sprite = pygame.image.load('data/gfx/carrot.png')
        self.position = pygame.Vector2()


class Button:
    def __init__(self):
        self.price = 3
        self.level = 1

    sprite = pygame.image.load('data/gfx/button.png')
    typeIndicatorSprite = pygame.image.load('data/gfx/null_indicator.png')


def check_value(value, min, max):
    if value < min:
        return min
    if value > max:
        return max
    return value


def check_overlay(x1, y1, width1, height1, x2, y2, width2, height2):
    return (x1 + width1 > x2) and (x1 < x2 + width2) and (y1 + height1 > y2) and (y1 < y2 + height2)


def main():
    # Инициализация
    pygame.init()
    screen = pygame.display.set_mode((640, 480), 0, 32)
    pygame.display.set_caption('Feed The Bunny')
    pygame.display.set_icon(Carrot().sprite)

    WHITE = (255, 255, 255)
    rotoffs = -5

    # Звуки
    jump_sound = pygame.mixer.Sound("data/sfx/flap.wav")
    upgrade_sound = pygame.mixer.Sound("data/sfx/upgrade.wav")
    getbean_sound = pygame.mixer.Sound("data/sfx/bean.wav")
    dead_sound = pygame.mixer.Sound("data/sfx/dead.wav")
    opengame_sound = pygame.mixer.Sound("data/sfx/enter_ingame.wav")

    # Пнгшки для игры
    shop = pygame.image.load('data/gfx/shop.png')
    shop_back = pygame.image.load('data/gfx/shop_bg.png')
    retry_button = pygame.image.load('data/gfx/retry_button.png')
    start_button = pygame.image.load('data/gfx/retry_button.png')
    logo = pygame.image.load('data/gfx/logo.png')
    title_back = pygame.image.load('data/gfx/background.png')
    title_back.fill((210, 40, 0), special_flags=pygame.BLEND_ADD)

    # Шрифты
    font = pygame.font.Font('data/fonts/meri.ttf', 100)
    font_small = pygame.font.Font('data/fonts/meri.ttf', 32)
    font_20 = pygame.font.Font('data/fonts/meri.ttf', 20)

    # создание персонажа кнопочек и морковок
    player = Player()
    carrots = []
    buttons = []

    # константы начала игры
    beans_kolvo = 30
    bean_multiply = 2
    HEIGHT_1 = player.pos.y
    height = 0
    health = 100
    jump_sila = 3
    dead = False
    maxi = 0

    # кнопки для апгрейда перса
    for i in range(3):
        buttons.append(Button())

    # создание еды
    for i in range(5):
        carrots.append(Carrot())

    for carrot in carrots:
        carrot.position.xy = random.randrange(0, screen.get_width() - carrot.sprite.get_width()), carrots.index(
            carrot) * -200 - player.pos.y

    # фотки для этих апгрейдов
    buttons[0].typeIndicatorSprite = pygame.image.load('data/gfx/flap_indicator.png')
    buttons[0].price = 5
    buttons[1].typeIndicatorSprite = pygame.image.load('data/gfx/speed_indicator.png')
    buttons[1].price = 5
    buttons[2].typeIndicatorSprite = pygame.image.load('data/gfx/carrot_upgrade.png')
    buttons[2].price = 30

    # бэкграунды
    bg = [Background(), Background(), Background()]



    # таймер для интро и фпс
    last_time = time.time()
    screentime = 0

    # музыка
    pygame.mixer.Sound.play(opengame_sound)
    while screentime < 60:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        a = time.time() - last_time
        a *= 60
        last_time = time.time()
        screentime += a
        screen.fill((250, 190, 125))

        # СОЗДАТЕЛИ ПРОЕКТА
        imena = font_small.render("Kostya and Vadim", True, (100, 100, 100))
        screen.blit(imena, (screen.get_width() / 2 - imena.get_width() / 2,
                            screen.get_height() / 2 - imena.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(10)

    # Название игры
    game_name = True
    pygame.mixer.Sound.play(opengame_sound)
    while game_name:
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        a = time.time() - last_time
        a *= 60
        last_time = time.time()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        startMessage = font_small.render("START", True, (0, 0, 0))
        screen.fill(WHITE)
        screen.blit(title_back, (0, 0))
        screen.blit(logo, (screen.get_width() / 2 - logo.get_width() / 2,
                           screen.get_height() / 2 - logo.get_height() / 2 + math.sin(time.time() * 5) * 5 - 25))
        screen.blit(start_button, (screen.get_width() / 2 - start_button.get_width() / 2, 288))
        screen.blit(startMessage, (screen.get_width() / 2 - startMessage.get_width() / 2, 300))

        pygame.display.update()
        pygame.time.delay(10)

        # если нажал старт, то открывается игра

        if (clicked and check_overlay(mouse_x, mouse_y, 3, 3,
                                      screen.get_width() / 2 - start_button.get_width() / 2,
                                      288, start_button.get_width(), start_button.get_height())):
            pygame.mixer.Sound.play(upgrade_sound)
            game_name = False

    # ВСЯ ИГРА
    while True:
        a = time.time() - last_time
        a *= 60
        last_time = time.time()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        jump = False
        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                jump = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
            if clicked and mouse_y < screen.get_height() - 90:
                jump = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        offset = screen.get_height() / 2 - player.pos.y - player.currentsprite.get_size()[1] / 2
        screen.fill(WHITE)

        # Создание красивого бэкграунда
        for i in bg:
            i.give_sprite(((player.pos.y / 50) % 100) / 100)
            screen.blit(i.sprite, (0, i.position))

        # Номер этажа
        color = colorsys.hsv_to_rgb(((player.pos.y / 50) % 100) / 100, 0.5, 0.5)
        height_mark = font.render(str(round(height)), True, (color[0] * 255, color[1] * 255, color[2] * 255, 50))

        screen.blit(height_mark, (screen.get_width() / 2 - height_mark.get_width() / 2,
                                  offset + round((player.pos.y - HEIGHT_1) / screen.get_height())
                                  * screen.get_height() + player.currentsprite.get_height() - 40))

        # Появление морковок
        for carrot in carrots:
            screen.blit(carrot.sprite, (carrot.position.x, carrot.position.y + offset))

        # Появление перса и разных кнопок
        screen.blit(pygame.transform.rotate(player.currentsprite, check_value(player.veloc.y, -10, 5) * rotoffs),
                    (player.pos.x, player.pos.y + offset))
        screen.blit(shop_back, (0, 0))
        pygame.draw.rect(screen, (240, 100, 30), (20, 435, 150 * (health / 100), 25))
        screen.blit(shop, (0, 0))

        # Числа на кнопках
        for button in buttons:
            screen.blit(button.sprite, (220 + (buttons.index(button) * 125), 393))
            priceDisplay = font_small.render(str(button.price), True, (0, 0, 0))
            screen.blit(priceDisplay, (260 + (buttons.index(button) * 125), 410))
            levelDisplay = font_20.render('Lvl. ' + str(button.level), True, (100, 100, 100))
            screen.blit(levelDisplay, (235 + (buttons.index(button) * 125), 440))

        # фотки на кнопках
        beanCountDisplay = font_small.render(str(beans_kolvo).zfill(7), True, (0, 0, 0))
        screen.blit(buttons[0].typeIndicatorSprite, (197, 390))
        screen.blit(buttons[1].typeIndicatorSprite, (320, 388))
        screen.blit(buttons[2].typeIndicatorSprite, (434, 380))

        screen.blit(beanCountDisplay, (70, 400))
        # значение высоты
        height = -(player.pos.y - HEIGHT_1) / screen.get_height()

        if height > maxi:
            maxi = height
        # Если умер
        if dead:
            screen.fill(WHITE)
            screen.blit(title_back, (0, 0))
            screen.blit(logo, (screen.get_width() / 2 - logo.get_width() / 2,
                               screen.get_height() / 2 - logo.get_height() / 2 + math.sin(time.time() * 5) * 5 - 25))
            pygame.display.update()

            # показ рекорда
            with open("best.txt", "r") as j:
                b = round(float(j.readlines()[-1]))
            screen.blit(retry_button, (250, 340))
            deathMessage = font_small.render("RETRY", True, (0, 0, 0))
            screen.blit(deathMessage, (270, 350))
            if maxi >= b:
                screen.blit(font_small.render(f"New record:{b}", True, (0, 0, 0)), (200, 300))
                with open("best.txt", "w") as j:
                    j.write(str(maxi))
            else:
                now_result = font_small.render(f"Result:{str(round(maxi))}", True, (0, 0, 0))
                screen.blit(now_result, (260, 270))
                screen.blit(font_small.render(f"Your best result:{b}", True, (0, 0, 0)), (200, 300))

        # Движение и прыжки
        player.pos.x += player.veloc.x * a

        # Реализация столкновений об стены
        if player.pos.x + player.currentsprite.get_size()[0] > 640:
            player.veloc.x = -abs(player.veloc.x)
            player.currentsprite = player.rightsprite
            rotoffs = 5
        if player.pos.x < 0:
            player.veloc.x = abs(player.veloc.x)
            player.currentsprite = player.leftsprite
            rotoffs = -5

        # реализация прыжка
        if jump and not dead:
            player.veloc.y = -jump_sila
            pygame.mixer.Sound.play(jump_sound)
        player.pos.y += player.veloc.y * a
        player.veloc.y = check_value(player.veloc.y + player.accelerat * a, -99999999999, 50)

        # Здоровье
        health -= 0.2 * a
        if health <= 0 and not dead:
            dead = True
            pygame.mixer.Sound.play(dead_sound)

        # кушание морковок
        for carrot in carrots:
            if carrot.position.y + offset + 90 > screen.get_height():
                carrot.position.y -= screen.get_height() * 2
                carrot.position.x = random.randrange(0, screen.get_width() - carrot.sprite.get_width())

            if (check_overlay(player.pos.x, player.pos.y, player.currentsprite.get_width(),
                              player.currentsprite.get_height(), carrot.position.x, carrot.position.y,
                              carrot.sprite.get_width(), carrot.sprite.get_height())):

                dead = False
                pygame.mixer.Sound.play(getbean_sound)
                beans_kolvo += 1
                health = 100
                carrot.position.y -= screen.get_height() - random.randrange(0, 200)
                carrot.position.x = random.randrange(0, screen.get_width() - carrot.sprite.get_width())

        # Прожимание кнопок
        for button in buttons:
            buttonX, buttonY = 220 + (buttons.index(button) * 125), 393
            if clicked and not dead and check_overlay(mouse_x, mouse_y, 3, 3, buttonX, buttonY,
                                                      button.sprite.get_width(), button.sprite.get_height()):
                if beans_kolvo >= button.price:
                    pygame.mixer.Sound.play(upgrade_sound)
                    button.level += 1
                    beans_kolvo -= button.price
                    button.price = round(button.price * 2.5)

                    if buttons.index(button) == 0:
                        jump_sila *= 1.5
                    if buttons.index(button) == 1:
                        player.veloc.x *= 1.5
                    if buttons.index(button) == 2:
                        bean_multiply += 10
                        for i in range(bean_multiply):
                            carrots.append(Carrot())
                            carrots[-1].position.xy = random.randrange(0,
                                                                       screen.get_width() - carrot.sprite.get_width()), \
                                                      player.pos.y - screen.get_height() - random.randrange(0, 200)

        # Обновление значений после смерти
        if dead and clicked and check_overlay(mouse_x, mouse_y, 3, 3, 4, 4, retry_button.get_width() + 250,
                                              retry_button.get_height() + 340):
            health = 100
            player.veloc.xy = 3, 0
            player.pos.xy = 295, 100
            player.currentsprite = player.rightsprite
            beans_kolvo = 0
            height = 0
            maxi = 0
            jump_sila = 3
            bean_multiply = 2
            buttons = []

            for i in range(3):
                buttons.append(Button())
            buttons[0].typeIndicatorSprite = pygame.image.load('data/gfx/flap_indicator.png')
            buttons[0].price = 5
            buttons[1].typeIndicatorSprite = pygame.image.load('data/gfx/speed_indicator.png')
            buttons[1].price = 5
            buttons[2].typeIndicatorSprite = pygame.image.load('data/gfx/carrot_upgrade.png')
            buttons[2].price = 30
            carrots = []

            for i in range(5):
                carrots.append(Carrot())
            # спавн еще раз морковок
            for carrot in carrots:
                carrot.position.xy = random.randrange(0, screen.get_width() - carrot.sprite.get_width()), carrots.index(
                    carrot) * -200 - player.pos.y
            pygame.mixer.Sound.play(upgrade_sound)
            dead = False

        bg[0].position = offset + round(player.pos.y / screen.get_height()) * screen.get_height()
        bg[1].position = bg[0].position + screen.get_height()
        bg[2].position = bg[0].position - screen.get_height()

        pygame.display.update()
        pygame.time.delay(10)


if __name__ == "__main__":
    main()
