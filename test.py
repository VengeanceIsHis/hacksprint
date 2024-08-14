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

class Animation:
    def __init__(self, frames=None, frame_rate=300, flipped=False):
        if frames is None:
            frames = []
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
        if not self.frames:
            return None
        frame = self.frames[self.current_frame]
        if self.flipped:
            print("HIII")
            return pygame.transform.flip(frame, True, False)
        return frame

class Player(Animation):
    def __init__(self):
        super().__init__()
        self.width = 64
        self.height = 64
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.current_animation = None

        # Load frames for the animation
        self.animations = {
            'idle': self.load_frames('idle'),
            'run': self.load_frames('run'),
        }

        # Set the initial animation
        self.current_animation = self.animations['idle']

    def load_frames(self, animation_type):
        frames = []
        folder_path = os.path.join('assets', 'animations', 'Knight', animation_type)
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith('.png'):
                frame_path = os.path.join(folder_path, filename)
                frame = pygame.image.load(frame_path)
                frame = pygame.transform.scale(frame, (self.width, self.height))
                frames.append(frame)
        print("HIII")
        return frames

    def set_animation(self, animation_type):
        if animation_type in self.animations and self.animations[animation_type]:
            self.current_animation = Animation(self.animations[animation_type], frame_rate=100)  # Adjust frame rate as needed

    def update(self):
        if self.current_animation:
            self.current_animation.update()

    def draw(self, screen):
        if self.current_animation:
            screen.blit(self.current_animation.get_current_frame(), (self.x, self.y))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)

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
            player.set_animation('run')
        elif keys[pygame.K_RIGHT]:
            dx = PLAYER_VEL
            player.set_animation('run')
        else:
            player.set_animation('idle')

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
        player.update()
        WIN.blit(BG, (0, 0))  # Clear screen with background image
        player.draw(BG)      # Draw the player on the screen
        draw(elapsed_time, stars)  # Draw other game elements
        pygame.display.flip()  # Update the display

    pygame.quit()


if __name__ == "__main__":
    main()
