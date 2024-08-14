import pygame
import time
import random
import os
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

BG = pygame.transform.scale(pygame.image.load("bg.png"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

PLAYER_VEL = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3

FONT = pygame.font.SysFont("comicsans", 30)


def display(elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))


    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()

class Idle(pygame.sprite.Sprite):
    def __init__(self,x , y):
        super().__init__()
        self.x = x
        self.y = y
        self.sprites = []
        new_size = (50, 50)
        img1 = pygame.image.load('assets/animations/Knight/idle/i1.png')
        img2 = pygame.image.load('assets/animations/Knight/idle/i2.png')
        img1_resized = pygame.transform.scale(img1, new_size)
        img2_resized = pygame.transform.scale(img2, new_size)
        self.sprites.append(img1_resized)
        self.sprites.append(img2_resized)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

    def update(self):
            self.current_sprite += 1
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[self.current_sprite]

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)

def main():
    pygame.init()
    run = True

    player = Idle(10, 10)
    moving_sprites = pygame.sprite.Group()
    moving_sprites.add(player)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_LEFT]:
            dx = -PLAYER_VEL
           
        elif keys[pygame.K_RIGHT]:
            dx = PLAYER_VEL
           
            

        # Ensure the player position is updated
        player.move(dx, dy)

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.colliderect(player.rect):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        # Update the player's animation and draw the updated player
        
        WIN.blit(BG, (0, 0))  # Clear screen with background image
        moving_sprites.draw(BG)
        moving_sprites.update()
        display(elapsed_time, stars)  # Draw other game elements
        pygame.display.flip()  # Update the display

    pygame.quit()


if __name__ == "__main__":
    main()
