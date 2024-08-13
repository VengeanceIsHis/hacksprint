import pygame as pg
import os

def load_animation_frames(folder_path):
    frames = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith('.png'):
            frame_path = os.path.join(folder_path, filename)
            frame = pg.image.load(frame_path)
            frames.append(frame)
    return frames

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

def main():
    pg.init()
    screen = pg.display.set_mode((1080, 1080))
    pg.display.set_caption("Smoky Lava")

    image_path = os.path.join('assets', 'images', 'Castle_4.png')
    print("Image Path:", image_path)
    image = pg.image.load(image_path)
    image = pg.transform.scale(image, (1080, 1080))

    knight_folder_path = os.path.join('assets', 'animations', 'Knight', 'idle')
    knight_frames = load_animation_frames(knight_folder_path)
    frame_rate = 200
    knight_animation = Animation(knight_frames, frame_rate)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        knight_animation.update()

        screen.fill((255, 255, 255))
        screen.blit(image, (0, 0))

        screen.blit(knight_animation.get_current_frame(), (100, 100))

        pg.display.flip()

        pg.time.Clock().tick(60)

    pg.quit()

if __name__ == "__main__":
    main()