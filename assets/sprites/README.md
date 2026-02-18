# Sprite Assets

This directory contains the sprite sheet images for Troup'O Invaders.

## Required Sprite Sheets

### ruminants.png
- **Size**: 384x512 pixels (6 columns × 8 rows of 64x64 frames)
- **Contents**:
  - Row 0: Cow idle animation (4 frames)
  - Row 1: Cow walk animation (6 frames)
  - Row 2: Sheep idle animation (4 frames)
  - Row 3: Sheep walk animation (6 frames)
  - Row 4: Goat idle animation (4 frames)
  - Row 5: Goat walk animation (6 frames)
  - Row 6: Alpaca idle animation (4 frames)
  - Row 7: Alpaca walk animation (6 frames)

### player.png
- **Size**: 288x96 pixels (6 columns × 2 rows of 48x48 frames)
- **Contents**:
  - Row 0: Ship idle (1 frame)
  - Row 1: Ship thrust animation (3 frames)

### projectiles.png
- **Size**: 32x32 pixels (2 columns × 2 rows of 16x16 frames)
- **Contents**:
  - Row 0: Player bullet animation (2 frames)
  - Row 1: Enemy bullet animation (2 frames)

## Creating Sprites

For now, you can use placeholder colored rectangles or simple pixel art.

Recommended tools:
- **Aseprite** - Best for pixel art and sprite sheets
- **Piskel** - Free online pixel art tool
- **GIMP** - Free image editor
- **Photoshop** - Commercial option

## Temporary Placeholders

Until actual sprites are created, the sprite manager will attempt to load these files.
You can create simple colored rectangles as placeholders for testing.

Example using ImageMagick:
```bash
# Create placeholder ruminants spritesheet (red rectangles)
convert -size 384x512 xc:red assets/sprites/ruminants.png

# Create placeholder player spritesheet (blue rectangles)
convert -size 288x96 xc:blue assets/sprites/player.png

# Create placeholder projectiles spritesheet (yellow rectangles)
convert -size 32x32 xc:yellow assets/sprites/projectiles.png
```

Or use any graphics tool to create solid color images with the dimensions above.

## Current Status

⚠️ **Placeholder images not yet created.** The sprite system is fully implemented and ready to use, but actual sprite image files need to be created and placed in this directory. Until then, the example page will show loading errors for missing images.

To test the system immediately, create simple placeholder PNGs with the dimensions specified above using any graphics tool.
