import pygame as pg
import random
import time

def main():
    pg.init()
    WIDTH, HEIGHT = 800, 600
    WIN = pg.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pg.time.Clock()
    player = Player()
    player.set_animation('idle')

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    run = True
    while run:
        dt = CLOCK.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        keys = pg.key.get_pressed()
        dx, dy = 0, 0

        if keys[pg.K_LEFT]:
            dx = -5
            player.set_animation('run_left')
        elif keys[pg.K_RIGHT]:
            dx = 5
            player.set_animation('run_right')
        else:
            player.set_animation('idle')

        player.move(dx, dy)

        for star in stars[:]:
            star.y += 5  # Example velocity
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.colliderect(player.rect):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = pg.font.SysFont(None, 55).render("You Lost!", True, "white")
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
            pg.display.update()
            pg.time.delay(4000)
            break

        player.update()
        WIN.fill((0, 0, 0))  # Clear screen
        player.draw(WIN)
        pg.display.flip()

    pg.quit()