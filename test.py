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

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 64
        self.height = 64
        self.x = 100
        self.y = 100
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Load frames for the animation
        self.animations = {
            'idle': [],
            'run_left': [],
            'run_right': []
        }
        self.load_frames()
        self.current_animation = None

    def set_animation(self, animation_type):
        if animation_type in self.animations and self.animations[animation_type]:
            self.current_animation = Animation(self.animations[animation_type], frame_rate=300)
    
    def load_frames(self):
        for animation_type in self.animations:
            animation = animation_type
            if animation == 'run_left' or animation == 'run_right':
                animation = 'run'
            frames = []
            folder_path = os.path.join('assets', 'animations', 'Knight', animation)
            for filename in sorted(os.listdir(folder_path)):
                if filename.endswith('.png'):
                    frame_path = os.path.join(folder_path, filename)
                    frame = pygame.image.load(frame_path)
                    frame = pygame.transform.scale(frame, (self.width, self.height))
                    frames.append(frame)
            self.animations[animation_type] = frames

    def update(self):
        if self.current_animation:
            self.current_animation.update()

    def get_current_frame(self):
        # Return the current frame from the animation
        if self.current_animation:
            return self.current_animation.get_current_frame()
        return None

    def draw(self, screen):
        frame = self.get_current_frame()
        if frame:
            screen.blit(frame, (self.x, self.y))
            print("HIIII")

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)

class Animation:
    def __init__(self, frames, frame_rate, flipped=False):
        self.frames = frames
        self.frame_rate = frame_rate
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.flipped = flipped

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = now

    def get_current_frame(self):
        frame = self.frames[self.current_frame]
        if self.flipped:
            return pygame.transform.flip(frame, True, False)
        return frame

def main():
    run = True

    player = Player()
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
