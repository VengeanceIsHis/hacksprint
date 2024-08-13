import pygame as pg
import os

class Player: 
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.health = 3
        self.path = "assets/animations/Knight/idle"

    def player(self):
        frames = []
        for filename in sorted(os.listdir(self.path)):
            if filename.endswith('.png'):
                frame_path = os.path.join(self.path, filename)
                frame = pg.image.load(frame_path)
                frame = pg.transform.scale(frame, self.width, self.height)
                frames.append(frame)
        frame_rate = 300
        knight_animation = Animation(frames, frame_rate)
        

class Animation:
    def __init__(self, frames, frame_rate):
        self.frames = frames
        self.frame_rate = frame_rate
        self.current_frame = 0
        self.last_update = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = now

    def get_current_frame(self):
        return self.frames[self.current_frame]

def draw_with_outline(screen, image, position, outline_color, outline_width):

    outline_rect = pg.Rect(position[0] - outline_width, position[1] - outline_width, image.get_width() + 2 * outline_width, image.get_height() + 2 * outline_width)
    pg.draw.rect(screen, outline_color, outline_rect, outline_width)

    screen.blit(image, position)

def main():
    pg.init()
    screen_width, screen_height = 1080, 1080
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption("Smoky Lava")

    image_path = os.path.join('assets', 'images', 'Castle_4.png')
    print("Image Path:", image_path)
    image = pg.image.load(image_path)
    image = pg.transform.scale(image, (1080, 1080))
    player = Player(40, 40)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        knight_animation.update()

        screen.fill((255, 255, 255))
        screen.blit(image, (0, 0))

        screen.blit(knight_animation.get_current_frame(), (7.5, 7.5))

        pg.display.flip()

        pg.time.Clock().tick(60)

    pg.quit()

if __name__ == "__main__":
    main()