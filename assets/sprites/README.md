# Sprite Assets

This directory contains the sprite sheet images for Troup'O Invaders.

## Required Sprite Sheets

### Individual Ruminant Spritesheets
Each ruminant has its own spritesheet for easier independent updates:

#### cow.png
- **Size**: 384x128 pixels (6 columns × 2 rows of 64x64 frames)
- **Contents**:
  - Row 0: Cow idle animation (4 frames)
  - Row 1: Cow walk animation (6 frames)

#### sheep.png
- **Size**: 384x128 pixels (6 columns × 2 rows of 64x64 frames)
- **Contents**:
  - Row 0: Sheep idle animation (4 frames)
  - Row 1: Sheep walk animation (6 frames)

#### goat.png
- **Size**: 384x128 pixels (6 columns × 2 rows of 64x64 frames)
- **Contents**:
  - Row 0: Goat idle animation (4 frames)
  - Row 1: Goat walk animation (6 frames)

#### alpaca.png
- **Size**: 384x128 pixels (6 columns × 2 rows of 64x64 frames)
- **Contents**:
  - Row 0: Alpaca idle animation (4 frames)
  - Row 1: Alpaca walk animation (6 frames)

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
# Create placeholder ruminant spritesheets (colored rectangles)
convert -size 384x128 xc:red assets/sprites/cow.png
convert -size 384x128 xc:white assets/sprites/sheep.png
convert -size 384x128 xc:tan assets/sprites/goat.png
convert -size 384x128 xc:wheat assets/sprites/alpaca.png

# Create placeholder player spritesheet (blue rectangles)
convert -size 288x96 xc:blue assets/sprites/player.png

# Create placeholder projectiles spritesheet (yellow rectangles)
convert -size 32x32 xc:yellow assets/sprites/projectiles.png
```

Or use any graphics tool to create solid color images with the dimensions above.

## Current Status

✅ **Placeholder images created!** The sprite system is fully implemented and working with colored placeholder sprites. Each ruminant has its own spritesheet for easy independent updates:
- cow.png (brown)
- sheep.png (white/gray)
- goat.png (tan/beige)
- alpaca.png (cream/brown)

Test the system at: http://localhost:8080/sprite-example.html
