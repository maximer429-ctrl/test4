# Generic Sprite Handling System

A unified sprite management system for Troup'O Invaders that works seamlessly with both Canvas 2D (test page) and WebGL (game).

## Features

- **Single Source of Truth**: All sprite definitions in one JSON config file
- **Spritesheet Support**: Efficiently loads and manages sprite sheets
- **Animation System**: Frame-based animations with customizable FPS
- **Dual Rendering**: Works with Canvas 2D and WebGL contexts
- **Metadata Support**: Store game-specific data (point values, speed, etc.)
- **Hot Updates**: Change config or sprites, refresh to see updates everywhere

## Quick Start

### 1. Load the Sprite Manager

```javascript
import { spriteManager } from './js/sprites/SpriteManager.js';

// Load all sprites
await spriteManager.load('assets/sprites/config.json');
```

### 2. Draw a Static Sprite (Canvas 2D)

```javascript
const ctx = canvas.getContext('2d');

// Draw first frame of cow_idle animation
spriteManager.draw(ctx, 'cow_idle', 0, x, y);
```

### 3. Use Animations

```javascript
// Create animation instance
const animation = spriteManager.createAnimation('cow_walk');
animation.play();

// In game loop
function update(deltaTime) {
    animation.update(deltaTime);
}

function render() {
    spriteManager.drawAnimation(ctx, animation, x, y);
}
```

## File Structure

```
src/js/sprites/
├── Animation.js        # Animation frame sequencing
├── Spritesheet.js      # Spritesheet loading & frame extraction
└── SpriteManager.js    # Main API (singleton)

assets/sprites/
├── config.json         # Sprite definitions
├── ruminants.png       # Enemy sprites
├── player.png          # Player ship sprites
└── projectiles.png     # Bullet sprites
```

## Configuration Format

### Sprite Config (`assets/sprites/config.json`)

```json
{
  "spritesheets": {
    "sheetName": {
      "path": "assets/sprites/sheet.png",
      "frameWidth": 64,
      "frameHeight": 64,
      "sprites": {
        "sprite_name": {
          "frames": [0, 1, 2, 3],
          "row": 0,
          "fps": 8,
          "loop": true
        }
      }
    }
  },
  "metadata": {
    "category": {
      "item": {
        "customData": "values"
      }
    }
  }
}
```

### Spritesheet Layout

Sprites are organized in a grid:
- **Columns**: Frame sequence (left to right)
- **Rows**: Different sprites (top to bottom)
- All frames must be the same size per spritesheet

```
[Frame 0][Frame 1][Frame 2][Frame 3]  <- Row 0: cow_idle
[Frame 0][Frame 1][Frame 2][Frame 3]  <- Row 1: cow_walk
[Frame 0][Frame 1][Frame 2][Frame 3]  <- Row 2: sheep_idle
```

## API Reference

### SpriteManager

#### Loading

```javascript
await spriteManager.load(configPath)
```

#### Query

```javascript
spriteManager.getAllSpriteNames()           // Get all sprite names
spriteManager.getSpritesByCategory()        // Get sprites grouped
spriteManager.getSpriteInfo(name)           // Get sprite metadata
spriteManager.isLoaded()                    // Check load status
```

#### Canvas 2D Rendering

```javascript
// Draw static frame
spriteManager.draw(ctx, spriteName, frameIndex, x, y, width?, height?)

// Draw animation
const anim = spriteManager.createAnimation(name)
anim.play()
spriteManager.drawAnimation(ctx, anim, x, y, width?, height?)
```

#### Game-Specific

```javascript
spriteManager.getRuminantMetadata(type)     // Get enemy data
spriteManager.getAllRuminantTypes()         // Get all enemy types
```

### Animation

```javascript
const anim = spriteManager.createAnimation('sprite_name')

anim.play()                    // Start playing
anim.pause()                   // Pause
anim.stop()                    // Stop and reset
anim.reset()                   // Reset to first frame
anim.update(deltaTime)         // Update (call each frame)
anim.getCurrentFrame()         // Get current frame data
```

### Spritesheet

```javascript
const sheet = spriteManager.getSpritesheet('sheetName')

sheet.getFrame(index, row)           // Get single frame
sheet.getFrames(indices, row)        // Get multiple frames
sheet.drawFrame(ctx, index, row, x, y, w?, h?)  // Draw directly
sheet.getFrameUVs(index, row)        // Get UV coords for WebGL
sheet.getInfo()                      // Get metadata
```

## Usage Examples

### Test Page (Canvas 2D)

```javascript
import { spriteManager } from './js/sprites/SpriteManager.js';

async function init() {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    
    // Load sprites
    await spriteManager.load();
    
    // Get all sprites for menu
    const sprites = spriteManager.getAllSpriteNames();
    sprites.forEach(name => {
        addToMenu(name);
    });
    
    // Draw selected sprite
    function drawSprite(spriteName) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        spriteManager.draw(ctx, spriteName, 0, 100, 100);
        
        // Show info
        const info = spriteManager.getSpriteInfo(spriteName);
        console.log(info);
    }
}
```

### Game (WebGL)

```javascript
import { spriteManager } from './js/sprites/SpriteManager.js';

class Enemy {
    constructor(type) {
        this.animation = spriteManager.createAnimation(`${type}_walk`);
        this.animation.play();
        this.metadata = spriteManager.getRuminantMetadata(type);
    }
    
    update(deltaTime) {
        this.animation.update(deltaTime);
        // Use this.metadata.speed for movement
    }
    
    render(ctx) {
        spriteManager.drawAnimation(ctx, this.animation, this.x, this.y);
    }
}

// Create enemy
const cow = new Enemy('cow');
```

### Animation with Custom Frame Rate

```javascript
// Slow idle animation
const idle = spriteManager.createAnimation('cow_idle');
idle.fps = 4;  // Slow down
idle.play();

// Fast walk animation
const walk = spriteManager.createAnimation('cow_walk');
walk.fps = 20;  // Speed up
walk.play();
```

## Updating Sprites

To update sprites without changing code:

1. **Edit sprite images**: Update PNG files in `assets/sprites/`
2. **Edit config**: Modify `assets/sprites/config.json` if needed
3. **Refresh**: Reload page/game to see changes

No code changes required!

## WebGL Integration

For WebGL rendering, use the UV coordinates:

```javascript
const sheet = spriteManager.getSpritesheet('ruminants');
const uvs = sheet.getFrameUVs(frameIndex, row);

// Use uvs.u, uvs.v, uvs.uWidth, uvs.vHeight in shaders
```

## Performance Tips

- **Reuse animations**: Call `createAnimation()` once per entity
- **Batch rendering**: Group sprites from same spritesheet
- **Preload**: Load all sprites at game start
- **Cache frames**: Animation frames are cached in memory

## Troubleshooting

### Sprites not showing
- Check console for loading errors
- Verify image paths in config.json
- Ensure spritesheet grid matches config

### Animations jerky
- Adjust fps value in config
- Ensure deltaTime is in milliseconds
- Check frame count matches spritesheet

### Wrong frames displayed
- Verify row/column indices in config
- Check frameWidth/frameHeight match actual sprites
- Confirm sprite sheet grid layout

## Future Enhancements

- [ ] Support for sprite atlases (non-grid layouts)
- [ ] Rotation and flipping
- [ ] Tint/color modifications
- [ ] Sprite effects (glow, shadow)
- [ ] Animation callbacks (onComplete, onLoop)
- [ ] Sprite preloading with progress
