import pygame as pg
import os

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
    pg.init()
    screen_width, screen_height = 1080, 1080
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption("Smoky Lava")

    image_path = os.path.join('assets', 'images', 'Castle_4.png')
    image = pg.image.load(image_path)
    image = pg.transform.scale(image, (1080, 1080))
    player = Player()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # Handle player movement
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            player.move(-5, 0)
        if key[pg.K_d]:
            player.move(5, 0)
        if key[pg.K_w]:
            player.move(0, -5)
        if key[pg.K_s]:
            player.move(0, 5)

        # Update player animation
        player.update()

        # Draw everything
        screen.blit(image, (0, 0))  # Draw background
        player.draw(screen)         # Draw player

        pg.display.flip()

        pg.time.Clock().tick(60)

    pg.quit()

if __name__ == "__main__":
    main()
