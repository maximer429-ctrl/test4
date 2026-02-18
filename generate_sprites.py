#!/usr/bin/env python3
"""
Generate placeholder sprite sheets for Troup'O Invaders
Creates simple colored rectangles as sprite placeholders
"""

import struct
import zlib

def create_png(width, height, color_rgb):
    """
    Create a simple PNG image with a solid color
    color_rgb: tuple of (r, g, b) values (0-255)
    """
    # PNG signature
    png_signature = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk (image header)
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr_chunk = create_chunk(b'IHDR', ihdr_data)
    
    # IDAT chunk (image data)
    raw_data = b''
    r, g, b = color_rgb
    for y in range(height):
        raw_data += b'\x00'  # Filter type
        raw_data += bytes([r, g, b] * width)
    
    compressed_data = zlib.compress(raw_data, 9)
    idat_chunk = create_chunk(b'IDAT', compressed_data)
    
    # IEND chunk (end of file)
    iend_chunk = create_chunk(b'IEND', b'')
    
    return png_signature + ihdr_chunk + idat_chunk + iend_chunk

def create_chunk(chunk_type, data):
    """Create a PNG chunk with type and data"""
    length = struct.pack('>I', len(data))
    crc = struct.pack('>I', zlib.crc32(chunk_type + data) & 0xffffffff)
    return length + chunk_type + data + crc

def create_grid_sprite(width, height, cell_width, cell_height, colors):
    """
    Create a sprite sheet with a grid of colored rectangles
    colors: list of (r, g, b) tuples for each cell
    """
    png_signature = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr_chunk = create_chunk(b'IHDR', ihdr_data)
    
    # Create image data
    raw_data = b''
    cols = width // cell_width
    
    for y in range(height):
        raw_data += b'\x00'  # Filter type
        row_idx = y // cell_height
        for x in range(width):
            col_idx = x // cell_width
            color_idx = row_idx * cols + col_idx
            if color_idx < len(colors):
                r, g, b = colors[color_idx]
            else:
                r, g, b = (0, 0, 0)  # Black for empty cells
            raw_data += bytes([r, g, b])
    
    compressed_data = zlib.compress(raw_data, 9)
    idat_chunk = create_chunk(b'IDAT', compressed_data)
    iend_chunk = create_chunk(b'IEND', b'')
    
    return png_signature + ihdr_chunk + idat_chunk + iend_chunk

# Generate individual ruminant spritesheets (6x2 grid of 64x64 each)
ruminants = {
    'cow': {
        'colors': [
            # Row 0: Cow idle - brown shades
            (139, 90, 43), (160, 110, 63), (139, 90, 43), (120, 80, 40), (0, 0, 0), (0, 0, 0),
            # Row 1: Cow walk - brown shades
            (139, 90, 43), (160, 110, 63), (139, 90, 43), (120, 80, 40), (160, 110, 63), (139, 90, 43),
        ]
    },
    'sheep': {
        'colors': [
            # Row 0: Sheep idle - white/gray
            (240, 240, 240), (220, 220, 220), (240, 240, 240), (200, 200, 200), (0, 0, 0), (0, 0, 0),
            # Row 1: Sheep walk - white/gray
            (240, 240, 240), (220, 220, 220), (240, 240, 240), (200, 200, 200), (220, 220, 220), (240, 240, 240),
        ]
    },
    'goat': {
        'colors': [
            # Row 0: Goat idle - tan/beige
            (210, 180, 140), (190, 160, 120), (210, 180, 140), (180, 150, 110), (0, 0, 0), (0, 0, 0),
            # Row 1: Goat walk - tan/beige
            (210, 180, 140), (190, 160, 120), (210, 180, 140), (180, 150, 110), (190, 160, 120), (210, 180, 140),
        ]
    },
    'alpaca': {
        'colors': [
            # Row 0: Alpaca idle - cream/brown
            (245, 222, 179), (238, 203, 173), (245, 222, 179), (222, 184, 135), (0, 0, 0), (0, 0, 0),
            # Row 1: Alpaca walk - cream/brown
            (245, 222, 179), (238, 203, 173), (245, 222, 179), (222, 184, 135), (238, 203, 173), (245, 222, 179),
        ]
    }
}

for animal_name, data in ruminants.items():
    print(f"Generating {animal_name}.png...")
    animal_png = create_grid_sprite(384, 128, 64, 64, data['colors'])
    with open(f'assets/sprites/{animal_name}.png', 'wb') as f:
        f.write(animal_png)
    print(f"✓ Created assets/sprites/{animal_name}.png (384x128)")


# Generate player.png (288x96, 6x2 grid of 48x48)
print("Generating player.png...")
player_colors = [
    # Row 0: Ship idle - cyan/blue
    (0, 255, 255), (0, 200, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
    # Row 1: Ship thrust - cyan with orange
    (0, 255, 255), (255, 165, 0), (255, 140, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
]
player_png = create_grid_sprite(288, 96, 48, 48, player_colors)
with open('assets/sprites/player.png', 'wb') as f:
    f.write(player_png)
print("✓ Created assets/sprites/player.png (288x96)")

# Generate projectiles.png (32x32, 2x2 grid of 16x16)
print("Generating projectiles.png...")
projectile_colors = [
    # Row 0: Player bullet - yellow/white
    (255, 255, 0), (255, 255, 255),
    # Row 1: Enemy bullet - red/orange
    (255, 0, 0), (255, 100, 0),
]
projectiles_png = create_grid_sprite(32, 32, 16, 16, projectile_colors)
with open('assets/sprites/projectiles.png', 'wb') as f:
    f.write(projectiles_png)
print("✓ Created assets/sprites/projectiles.png (32x32)")

print("\n✓ All placeholder sprite sheets generated successfully!")
print("\nSprite sheets created:")
print("  - assets/sprites/cow.png (cow animations)")
print("  - assets/sprites/sheep.png (sheep animations)")
print("  - assets/sprites/goat.png (goat animations)")
print("  - assets/sprites/alpaca.png (alpaca animations)")
print("  - assets/sprites/player.png (player ship animations)")
print("  - assets/sprites/projectiles.png (bullet animations)")
print("\nYou can now test the sprite system at http://localhost:8080/sprite-example.html")
