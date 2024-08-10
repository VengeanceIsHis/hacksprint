import pygame as pg
import sys
import os

def main():
    pg.init()
    screen = pg.display.set_mode((640, 480))  # Create a display surface
    pg.display.set_caption("White Screen")
    image_path = os.path.join(os.path.expanduser('~'), 'Documents', 'gamephotos', 'forest')
    print("Image Path:", image_path)

    image = pg.image.load(image_path)
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill((255, 255, 255))  # Fill the screen with white
        screen.blit(image, (0, 0))
        pg.display.flip()  # Update the display

    pg.quit()

if __name__ == "__main__":
    main()