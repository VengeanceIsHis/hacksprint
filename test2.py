import pygame as pg
import random
import time
import os

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 64
        self.height = 64
        self.x = 100
        self.y = 100
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

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
                    frame = pg.image.load(frame_path)
                    frame = pg.transform.scale(frame, (self.width, self.height))
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
        self.last_update = pg.time.get_ticks()
        self.flipped = flipped

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = now

    def get_current_frame(self):
        frame = self.frames[self.current_frame]
        if self.flipped:
            return pg.transform.flip(frame, True, False)
        return frame
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