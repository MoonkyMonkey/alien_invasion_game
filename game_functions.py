import sys
from time import sleep
import pygame

from bullet import Bullet
from alien import Alien

# evens functions
def check_keydown_events(event, ai_settings, screen, stats, scoreboard, ship, aliens, bullets):
    """react to keydown"""
    # print(event.key)
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:
        if not stats.game_active:
            start_game(ai_settings, screen, stats, scoreboard, ship, aliens, bullets)
    # elif event.key == pygame.K_UP:
    #     ship.moving_up = True
    # elif event.key == pygame.K_DOWN:
    #     ship.moving_down = True

def check_keyup_events(event, ship):
    """react to keyup"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    # elif event.key == pygame.K_UP:
    #     ship.moving_up = False
    # elif event.key == pygame.K_DOWN:
    #     ship.moving_down = False

def start_game(ai_settings, screen, stats, scoreboard, ship, aliens, bullets):
    # reset game speed
    ai_settings.initialize_dynamic_settings()

    # set cursor invisible
    pygame.mouse.set_visible(False)

    stats.reset_stats()
    stats.game_active = True

    # reset score 
    scoreboard.prep_score()
    scoreboard.prep_high_score()
    scoreboard.prep_level()
    scoreboard.prep_ships()

    aliens.empty()
    bullets.empty()

    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

def check_play_buttom(ai_settings, screen, stats, scoreboard, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    buttom_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if buttom_clicked and not stats.game_active:
        start_game(ai_settings, screen, stats, scoreboard, ship, aliens, bullets)
        

def check_events(ai_settings, screen, stats, scoreboard, play_button, ship, aliens, bullets):
    """react to mouse keybroad events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, scoreboard, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_buttom(ai_settings, screen, stats, scoreboard, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        
# screen functions
def update_screen(ai_settings, stats, screen, ship, aliens, bullets, play_button, scoreboard):
    """update srceen images"""
    # use background color 
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    scoreboard.show_score()
    if not stats.game_active:
        play_button.draw_button()

    # make screen availble
    # 每次执行 while 都会绘制一个空屏幕，并擦去旧屏幕
    pygame.display.flip()

# bullet function
def check_bullet_alien_collisions(ai_settings, screen, stats, scoreboard, ship, aliens, bullets):
    # 检查子弹击中外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            scoreboard.prep_score()
        check_high_score(stats, scoreboard)
        

    # 外星人全没了重新生成
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        
        # level up
        stats.level += 1
        scoreboard.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)

def update_bullets(ai_settings, screen, stats, scoreboard, ship, aliens, bullets):
    # 更新子弹位置
    bullets.update()

    check_bullet_alien_collisions(ai_settings, screen, stats, scoreboard, ship, aliens, bullets)
    # 释放消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))

def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

# aliens functions
def get_number_aliens_x(ai_settings, alien_width):
    """compute alien number of each line"""
    availble_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(availble_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # 创建一个外星人并加入当前行
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def get_number_rows(ai_settings, ship_height, alien_height):
    """compute alien lines"""
    availble_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(availble_space_y / (2 * alien_height))
    return number_rows

def create_fleet(ai_settings, screen, ship, aliens):
    """create alien fleet"""
    # 创建一个外星人并计算一行容纳外星人的个数
    # 外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def ship_hit(ai_settings, screen, stats, scoreboard,  ship, aliens, bullets):
    """when alien hit the ship"""
    if stats.ships_left > 0:
        stats.ships_left -= 1
        scoreboard.prep_ships()

        # reset aliens and bullets
        aliens.empty()
        bullets.empty()

        # create new alien and reset ship position
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def update_aliens(ai_settings, screen, stats, scoreboard, ship, aliens, bullets):
    """update aliens positions"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 飞船和外星人碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, scoreboard, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, screen, stats, scoreboard, ship, aliens, bullets)

def check_fleet_edges(ai_settings, aliens):
    """if alien hit the edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """move down aliens and change dirctions"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_aliens_bottom(ai_settings, screen, stats, scoreboard, ship, aliens, bullets):
    """check alien hit the bottom"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings,  screen, stats, scoreboard, ship, aliens, bullets)


def check_high_score(stats, scoreboard):
    """check if it the highest score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()