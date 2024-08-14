
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


def draw(elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))


    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()

class Player:
    def __init__(self):
        # Define width and height for scaling frames
        self.width = 64  # Example width, adjust as needed
        self.height = 64  # Example height, adjust as needed

        # Load frames for the animation
        self.frames = self.load_frames()
        self.animations = {
            'run_left': self.load_frames()
        }

        # Create an Animation object
        self.animation = Animation(self.frames, frame_rate=300)  # Adjust frame_rate as needed

        # Player position
        self.x = 100
        self.y = 100

    def load_frames(self):
        frames = []
        folder_path = os.path.join('assets', 'animations', 'Knight', 'idle')
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith('.png'):
                frame_path = os.path.join(folder_path, filename)
                frame = pg.image.load(frame_path)
                # Scale frame using defined width and height
                frame = pg.transform.scale(frame, (self.width, self.height))
                frames.append(frame)
        return frames

    def update(self):
        # Update the animation
        self.animation.update()

    def get_current_frame(self):
        # Return the current frame from the animation
        return self.animation.get_current_frame()

    def draw(self, screen):
        screen.blit(self.get_current_frame(), (self.x, self.y))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

class Animation:
    def __init__(self, frames, frame_rate, flipped=False):
        self.frames = frames
        self.frame_rate = frame_rate
        self.current_frame = 0
        self.last_update = pg.time.get_ticks()
        self.flipped = flipped

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = now

    def get_current_frame(self):
        return self.frames[self.current_frame]

def main():
    run = True

    player = Player(width=40, height=40)
    player.load_frames('idle')
    player.load_frames
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
            player.set_animation('run_left')
        elif keys[pygame.K_RIGHT]:
            dx = PLAYER_VEL
            player.set_animation('run_right')
        else:
            player.set_animation('idle')

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

        player.update()
        WIN.blit(BG, (0, 0))  # Clear screen with background color
        player.draw(WIN)
        draw(elapsed_time, stars)
        pygame.display.flip()  # Update the display

    pygame.quit()


if __name__ == "__main__":
    main()
