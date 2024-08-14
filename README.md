david.portillo@atlasschool.com
|Casey Paul| (Casey.Paul@atlasschool.com)
# Smoky Lava - Pygame Animation

This Pygame project showcases a simple animation of a knight character over a background image. The knight's animation is looped, and an optional outline can be drawn around the character.

## Features

- **Animated Knight**: The knight character is displayed with a smooth frame-by-frame animation.
- **Customizable Frame Rate**: The animation speed can be adjusted by changing the frame rate in the code.
- **Outlined Drawing**: The knight can be drawn with an outline to make it stand out more against the background.

## Requirements

- Python 3.x
- Pygame (`pip install pygame`)

## Project Structure

```
project-root/
│
├── assets/
│   ├── images/
│   │   └── Castle_4.png
│   └── animations/
│       └── Knight/
│           └── idle/
│               ├── frame_001.png
│               ├── frame_002.png
│               ├── ...
│               └── frame_n.png
├── main.py
└── README.md
```

- **assets/images/**: Contains the background image (`Castle_4.png`).
- **assets/animations/Knight/idle/**: Contains the knight's animation frames.

## Setup and Usage

1. **Install Pygame**:
   ```bash
   pip install pygame
   ```

2. **Run the Program**:
   ```bash
   python main.py or python3 main.py
   ```

   This will launch a window showing the animated knight over the background image.
