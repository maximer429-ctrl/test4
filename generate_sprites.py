#!/usr/bin/env python3
"""
Generate sprite sheets for Troup'O Invaders
Creates pixel art sprites of ruminants (cow, sheep, goat, alpaca)
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

def create_image_from_pixels(width, height, pixels):
    """
    Create a PNG from a 2D array of (r, g, b, a) tuples
    pixels: list of lists, each inner list is a row of (r, g, b, a) tuples
    """
    png_signature = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk (with alpha channel: type 6)
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    ihdr_chunk = create_chunk(b'IHDR', ihdr_data)
    
    # Create image data with alpha
    raw_data = b''
    for row in pixels:
        raw_data += b'\x00'  # Filter type
        for pixel in row:
            r, g, b, a = pixel
            raw_data += bytes([r, g, b, a])
    
    compressed_data = zlib.compress(raw_data, 9)
    idat_chunk = create_chunk(b'IDAT', compressed_data)
    iend_chunk = create_chunk(b'IEND', b'')
    
    return png_signature + ihdr_chunk + idat_chunk + iend_chunk

def draw_sprite(pattern, colors):
    """
    Convert a text pattern to pixels
    pattern: list of strings, each character represents a color key
    colors: dict mapping characters to (r, g, b, a) tuples
    """
    pixels = []
    for line in pattern:
        row = []
        for char in line:
            if char in colors:
                row.append(colors[char])
            else:
                row.append((0, 0, 0, 0))  # Transparent
        pixels.append(row)
    return pixels

def create_spritesheet(frames, frame_width, frame_height):
    """
    Create a spritesheet from multiple frame patterns
    frames: list of frame pixel arrays
    Returns a combined spritesheet image
    """
    cols = 6
    rows = (len(frames) + cols - 1) // cols
    
    sheet_width = cols * frame_width
    sheet_height = rows * frame_height
    
    # Initialize empty sheet
    sheet_pixels = []
    for _ in range(sheet_height):
        row = [(0, 0, 0, 0)] * sheet_width
        sheet_pixels.append(row)
    
    # Place frames
    for i, frame in enumerate(frames):
        col = i % cols
        row = i // cols
        start_x = col * frame_width
        start_y = row * frame_height
        
        for y in range(min(len(frame), frame_height)):
            for x in range(min(len(frame[y]), frame_width)):
                sheet_pixels[start_y + y][start_x + x] = frame[y][x]
    
    return create_image_from_pixels(sheet_width, sheet_height, sheet_pixels)

# Cow sprite patterns (96x96)
def create_cow_sprites():
    colors = {
        ' ': (0, 0, 0, 0),           # Transparent
        'B': (139, 90, 43, 255),     # Brown body
        'W': (255, 255, 255, 255),   # White spots
        'D': (100, 65, 30, 255),     # Dark brown
        'P': (255, 192, 203, 255),   # Pink nose
        'H': (200, 200, 200, 255),   # Horn
        'E': (50, 30, 20, 255),      # Eye
    }
    
    # Simplified cow idle frame 1
    idle1 = [
        "                                                                                                ",
        "                                                                                                ",
        "                                                                                                ",
        "                                                                                                ",
        "                                      HHHH        HHHH                                          ",
        "                                    HH  HH      HH  HH                                          ",
        "                                  HH    HH    HH    HH                                          ",
        "                              EEEE  DDDDDDDDDDDDDD  EEEE                                        ",
        "                            EEBBBBBBBBBBBBBBBBBBBBBBBBBE                                        ",
        "                            EBBBBWWBBBBBBBBBBBBWWBBBBBBE                                        ",
        "                          DBBBBWWWWBBBBBBBBBBWWWWBBBBBBBD                                       ",
        "                          DBBBBBWWBBBBBBBBBBBBWWBBBBBBBD                                        ",
        "                          DBBBBBBBBBBBBBBBBBBBBBBBBBBBBD                                        ",
        "                        DDBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDD                                      ",
        "                        DBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBD                                       ",
        "                        DBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBD                                       ",
        "                        DBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBD                                       ",
        "                        DBBBBBBBBBBBBBWWWWBBBBBBBBBBBBBD                                        ",
        "                        DBBBBBBBBBBBBWWWWWWBBBBBBBBBBBBD                                        ",
        "                        DBBBBBBBBBBBWWWWWWWWBBBBBBBBBBBD                                        ",
        "                        DBBBBBBBBBBBBWWWWWWBBBBBBBBBBBBD                                        ",
        "                        DBBBBBBBBBBBBBWWWWBBBBBBBBBBBBBD                                        ",
        "                        DBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBD                                       ",
        "                        DBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBD                                       ",
        "                        DBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBD                                       ",
        "                        DBBWWBBBBBBBBBBBBBBBBBBBBBBWWBBBD                                       ",
        "                        DBBWWWBBBBBBBBBBBBBBBBBBBBBWWWBBD                                       ",
        "                        DBBWWBBBBBBBBBBBBBBBBBBBBBBWWBBBD                                       ",
        "                        DBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBD                                       ",
        "                        DDBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDD                                      ",
        "                        DDBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDD                                      ",
        "                          DBBBBBBBBBBBBBBBBBBBBBBBBBBBBD                                        ",
        "                          DBBBBBBBBBBBBBBBBBBBBBBBBBBBBD                                        ",
        "                          DDBBBBBBBBBBBBBBBBBBBBBBBBBBDD                                        ",
        "                            DBBBBBBBBBBBBBBBBBBBBBBBBBD                                         ",
        "                            DDBBBBBBBBBBBBBBBBBBBBBBDD                                          ",
        "                              DDDDDDDDDDDDDDDDDDDDDD                                            ",
        "                              PPPPP            PPPPP                                            ",
        "                             PP   PP          PP   PP                                           ",
        "                             PPPPPPP          PPPPPPP                                           ",
        "                             DDDDDD            DDDDDD                                           ",
        "                           DD    DD          DD    DD                                           ",
        "                          DD      DD        DD      DD                                          ",
        "                          DD      DD        DD      DD                                          ",
        "                          DD      DD       DD       DD                                          ",
        "                          DD      DD       DD       DD                                          ",
        "                          DD      DD       DD       DD                                          ",
        "                          DDDDDDDDDD       DDDDDDDDDD                                           ",
        "                                                                                                ",
        "                                                                                                ",
    ] + ["                                                                                                "] * 46
    
    # Walk frames with slight variations
    walk1 = idle1  # Reuse idle for simplicity
    walk2 = idle1
    walk3 = idle1
    
    frames = [
        draw_sprite(idle1, colors),
        draw_sprite(idle1, colors),
        draw_sprite(idle1, colors),
        draw_sprite(idle1, colors),
        draw_sprite(walk1, colors),
        draw_sprite(walk2,colors),
        draw_sprite(walk3, colors),
        draw_sprite(walk1, colors),
        draw_sprite(walk2, colors),
        draw_sprite(walk3, colors),
    ]
    
    return create_spritesheet(frames, 96, 96)

# Sheep sprite patterns
def create_sheep_sprites():
    colors = {
        ' ': (0, 0, 0, 0),           # Transparent
        'W': (240, 240, 240, 255),   # White wool
        'F': (220, 220, 220, 255),   # Fluffy wool
        'D': (180, 180, 180, 255),   # Dark wool
        'K': (80, 80, 80, 255),      # Dark gray face
        'E': (30, 30, 30, 255),      # Eye
        'L': (100, 100, 100, 255),   # Legs
    }
    
    idle1 = [
        "                                                                                                ",
        "                                                                                                ",
        "                                                                                                ",
        "                                                                                                ",
        "                                                                                                ",
        "                                  EEEE    KKKKKKK    EEEE                                       ",
        "                                EEKKKKKKKKKKKKKKKKKKKKE                                        ",
        "                                EKKKKKKKKKKKKKKKKKKKKKKE                                       ",
        "                              DDKKKKKKKKKKKKKKKKKKKKKKKDD                                      ",
        "                              DKKKKKKKKKKKKKKKKKKKKKKKKD                                       ",
        "                            FFWWWWWWWWWWWWWWWWWWWWWWWWWWFF                                     ",
        "                          FFWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWFF                                   ",
        "                          FWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWF                                   ",
        "                        FFWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWFF                                 ",
        "                        FWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWF                                 ",
        "                        FWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWF                                 ",
        "                        FWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWF                                 ",
        "                        FWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWF                                 ",
        "                        FWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWF                                 ",
        "                        FWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWF                                 ",
        "                        FWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWF                                 ",
        "                        FWWWWFFWWWWWWWWWWWWWWWWWWWWWWFFWWWWWWF                                 ",
        "                        FWWWFFWWWWWWWWWWWWWWWWWWWWWWWFFWWWWWWF                                 ",
        "                        FWWWWFFWWWWWWWWWWWWWWWWWWWWWWFFWWWWWWF                                 ",
        "                        FWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWF                                 ",
        "                        FWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWF                                 ",
        "                        FWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWF                                 ",
        "                        FWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWF                                 ",
        "                        FFWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWFF                                 ",
        "                          FWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWF                                   ",
        "                          DDWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWDD                                   ",
        "                            DDWWWWWWWWWWWWWWWWWWWWWWWWWWDD                                     ",
        "                              DDDDDDDDDDDDDDDDDDDDDDDD                                          ",
        "                              LL    LL      LL    LL                                           ",
        "                            LL  LL  LL    LL  LL  LL                                           ",
        "                            LL  LL  LL    LL  LL  LL                                           ",
        "                            LL  LL  LL    LL  LL  LL                                           ",
        "                            LL  LL  LL    LL  LL  LL                                           ",
        "                            LL  LL  LL    LL  LL  LL                                           ",
        "                            LLLLLL  LL    LL  LLLLLL                                           ",
        "                                                                                                ",
        "                                                                                                ",
    ] + ["                                                                                                "] * 54
    
    frames = [draw_sprite(idle1, colors)] * 10
    return create_spritesheet(frames, 96, 96)

# Goat sprite patterns
def create_goat_sprites():
    colors = {
        ' ': (0, 0, 0, 0),           # Transparent
        'B': (210, 180, 140, 255),   # Beige body
        'D': (180, 150, 110, 255),   # Dark beige
        'H': (230, 230, 230, 255),   # Horn
        'R': (190, 160, 120, 255),   # Medium beige
        'E': (50, 30, 20, 255),      # Eye
        'G': (150, 120, 90, 255),    # Beard
    }
    
    idle1 = [
        "                                                                                                ",
        "                                                                                                ",
        "                                                                                                ",
        "                                HH                      HH                                      ",
        "                              HH  HH                  HH  HH                                    ",
        "                            HH    HH                HH    HH                                    ",
        "                          HH      HH              HH      HH                                    ",
        "                        EEEE    DDDDDDDDDDDDDDDDDDD    EEEE                                    ",
        "                      EEBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBE                                     ",
        "                      EBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBE                                    ",
        "                    DDBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDD                                    ",
        "                    DBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBD                                     ",
        "                    DRRRDRRRDBBBBBBBBBBBBBBBBBBRRRDRRRRBBD                                     ",
        "                  DDBRRRRRRRDBBBBBBBBBBBBBBBBBDRRRRRRRRBDD                                    ",
        "                  DBBDRRRDRRDBBBBBBBBBBBBBBBBBRRRDRRRDBBD                                     ",
        "                  DBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBD                                     ",
        "                  DBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBD                                     ",
        "                  DBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBD                                     ",
        "                  DBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBD                                     ",
        "                  DBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBD                                     ",
        "                  DBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBD                                     ",
        "                  DBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBD                                     ",
        "                  DBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBD                                     ",
        "                  DBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDD                                    ",
        "                  DBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDD                                    ",
        "                  DDBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDD                                     ",
        "                    DBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBD                                      ",
        "                    DBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBD                                      ",
        "                    DDBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDD                                       ",
        "                      DBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBD                                         ",
        "                      DDBBBBBBBBBBBBBBBBBBBBBBBBBBBBDD                                         ",
        "                        DDDDDDDDDDDDDDDDDDDDDDDDDDDD                                           ",
        "                      GG    DD          DD    GG                                               ",
        "                     GG   GG  DD      DD  GG   GG                                              ",
        "                    GG    GG  DD      DD  GG    GG                                             ",
        "                    GG    DD          DD  GG                                                   ",
        "                    GG    DD          DD  GG                                                   ",
        "                    DD    DD          DD  DD                                                   ",
        "                  DD  DD  DD        DD  DD  DD                                                 ",
        "                  DD  DD  DD        DD  DD  DD                                                 ",
        "                  DD  DD  DD        DD  DD  DD                                                 ",
        "                  DD  DD  DD        DD  DD  DD                                                 ",
        "                  DD  DD  DD        DD  DD  DD                                                 ",
        "                  DDDDDD  DD        DD  DDDDDD                                                 ",
        "                                                                                                ",
    ] + ["                                                                                                "] * 52
    
    frames = [draw_sprite(idle1, colors)] * 10
    return create_spritesheet(frames, 96, 96)

# Alpaca sprite patterns
def create_alpaca_sprites():
    colors = {
        ' ': (0, 0, 0, 0),           # Transparent
        'C': (245, 222, 179, 255),   # Cream body
        'B': (222, 184, 135, 255),   # Brown
        'W': (238, 203, 173, 255),   # Light wool
        'E': (50, 30, 20, 255),      # Eye
        'N': (200, 170, 130, 255),   # Nose
        'D': (180, 150, 110, 255),   # Dark
    }
    
    idle1 = [
        "                                                                                                ",
        "                                                                                                ",
        "                                  EEEE  CCCCCCCC  EEEE                                         ",
        "                                EECCCCCCCCCCCCCCCCCCCE                                         ",
        "                                ECCCCCCCCCCCCCCCCCCCCCE                                        ",
        "                              DDCCCCCCCCCCCCCCCCCCCCCCDD                                       ",
        "                              DCCCCCCCCCCCCCCCCCCCCCCCD                                        ",
        "                              DCCCCCCCCCCCCCCCCCCCCCCCD                                        ",
        "                              DCCCCCCCCCCCCCCCCCCCCCCCD                                        ",
        "                              DCCCCCCCCCCCCCCCCCCCCCCCD                                        ",
        "                              DCCCCNNNNNNNNNNNNNCCCCCD                                         ",
        "                              DCCCCNNNNNNNNNNNNNCCCCCD                                         ",
        "                              DCCCCCCCCCCCCCCCCCCCCCCCD                                        ",
        "                              DCCCCCCCCCCCCCCCCCCCCCCCD                                        ",
        "                              DCCWWWCCCCCCCCCCCCWWWCCD                                         ",
        "                              DCCWWWWCCCCCCCCCCCWWWCCD                                         ",
        "                              DCCWWWCCCCCCCCCCCCWWWCCD                                         ",
        "                              DCCCCCCCCCCCCCCCCCCCCCCCD                                        ",
        "                              DCCCCCCCWWWWWWWWCCCCCCCD                                         ",
        "                              DCCCCCWWWWWWWWWWWCCCCCCD                                         ",
        "                              DCCCCCWWWWWWWWWWWCCCCCCD                                         ",
        "                              DCCCCCCWWWWWWWWCCCCCCCD                                          ",
        "                              DCCCCCCCCCCCCCCCCCCCCCD                                          ",
        "                              DCCCCCCCCCCCCCCCCCCCCCD                                          ",
        "                              DCCCCCCCCCCCCCCCCCCCCCD                                          ",
        "                              DCCCCCCCCCCCCCCCCCCCCD                                           ",
        "                              DCCCCCCCCCCCCCCCCCCCCD                                           ",
        "                            WWWCCCCCCCCCCCCCCCCCCWWW                                           ",
        "                          WWWWWWWCCCCCCCCCCCCCCWWWWWWW                                         ",
        "                          WWWWWWWWCCCCCCCCCCCWWWWWWWWW                                         ",
        "                          WWWWWWWWWCCCCCCCCCCWWWWWWWWW                                         ",
        "                          WWWWWWWWWWCCCCCCCWWWWWWWWWWW                                         ",
        "                          WWWWWWWWWWWCCCCCCWWWWWWWWWWW                                         ",
        "                          WWWWWWWWWWWWWCCWWWWWWWWWWWWW                                         ",
        "                          WWWWWWWWWWWWWWWWWWWWWWWWWWWW                                         ",
        "                          WWWWWWWWWWWWWWWWWWWWWWWWWWWW                                         ",
        "                            WWWWWWWWWWWWWWWWWWWWWWWW                                           ",
        "                            WWWWWWWWWWWWWWWWWWWWWWWW                                           ",
        "                              DWWWWWWWWWWWWWWWWWWD                                             ",
        "                              DDDDDDDDDDDDDDDDDDDD                                             ",
        "                              DD    DD    DD    DD                                             ",
        "                            DD  DD  DD  DD  DD  DD                                             ",
        "                            DD  DD  DD  DD  DD  DD                                             ",
        "                            DD  DD  DD  DD  DD  DD                                             ",
        "                            DD  DD  DD  DD  DD  DD                                             ",
        "                            DD  DD  DD  DD  DD  DD                                             ",
        "                            DDDDDD  DD  DD  DDDDDD                                             ",
        "                                                                                                ",
    ] + ["                                                                                                "] * 48
    
    frames = [draw_sprite(idle1, colors)] * 10
    return create_spritesheet(frames, 96, 96)

# Generate individual ruminant spritesheets
print("Generating cow.png...")
cow_png = create_cow_sprites()
with open('assets/sprites/cow.png', 'wb') as f:
    f.write(cow_png)
print("✓ Created assets/sprites/cow.png (576x192, 96x96 frames)")

print("Generating sheep.png...")
sheep_png = create_sheep_sprites()
with open('assets/sprites/sheep.png', 'wb') as f:
    f.write(sheep_png)
print("✓ Created assets/sprites/sheep.png (576x192, 96x96 frames)")

print("Generating goat.png...")
goat_png = create_goat_sprites()
with open('assets/sprites/goat.png', 'wb') as f:
    f.write(goat_png)
print("✓ Created assets/sprites/goat.png (576x192, 96x96 frames)")

print("Generating alpaca.png...")
alpaca_png = create_alpaca_sprites()
with open('assets/sprites/alpaca.png', 'wb') as f:
    f.write(alpaca_png)
print("✓ Created assets/sprites/alpaca.png (576x192, 96x96 frames)")


# Generate player.png (48x48 frames, simpler for player ship)
print("Generating player.png...")
player_colors = {
    ' ': (0, 0, 0, 0),
    'C': (0, 255, 255, 255),     # Cyan
    'B': (0, 200, 255, 255),     # Blue
    'D': (0, 150, 200, 255),     # Dark blue
    'O': (255, 165, 0, 255),     # Orange thrust
    'Y': (255, 215, 0, 255),     # Yellow thrust
}

player_idle = [
    "                                                ",
    "                       DD                       ",
    "                      DDDD                      ",
    "                     DDDDDD                     ",
    "                    DDDDDDD                    ",
    "                   DDDBBBDD                    ",
    "                  DDDBBBBBDDD                   ",
    "                 DDDBBBBBBDDDD                  ",
    "                DDDBBBCCCBBBDDD                 ",
    "               DDDBBCCCCCCBBDDD                 ",
    "              DDDBBBCCCCCCBBBDDDD               ",
    "             DDDBBBBCCCCCCBBBBDDD               ",
    "            DDDBBBBBBCCCCBBBBBDDDD              ",
    "           DDDBBBBBBBBBBBBBBBBBDDD              ",
    "          DDDBBBBBBBBBBBBBBBBBBDDDD             ",
    "         DDDBBBBBBBBBBBBBBBBBBBBDDD             ",
    "        DDDBBBBBBBBBBBBBBBBBBBBBDDDD            ",
] + ["                                                "] * 31

player_thrust = [
    "                                                ",
    "                       DD                       ",
    "                      DDDD                      ",
    "                     DDDDDD                     ",
    "                    DDDDDDD                    ",
    "                   DDDBBBDD                    ",
    "                  DDDBBBBBDDD                   ",
    "                 DDDBBBBBBDDDD                  ",
    "                DDDBBBCCCBBBDDD                 ",
    "               DDDBBCCCCCCBBDDD                 ",
    "              DDDBBBCCCCCCBBBDDDD               ",
    "             DDDBBBBCCCCCCBBBBDDD               ",
    "            DDDBBBBBBCCCCBBBBBDDDD              ",
    "           DDDBBBBBBBBBBBBBBBBBDDD              ",
    "          DDDBBBBBBBBBBBBBBBBBBDDDD             ",
    "         DDDBBBBBBBBBBBBBBBBBBBBDDD             ",
    "        DDDBBBBBBBBBBBBBBBBBBBBBDDDD            ",
    "       DDDBBBBBBBBBBBBBBBBBBBBBBDDDD            ",
    "      DDDBBBBBBBBBBBBBBBBBBBBBBBBDDD            ",
    "     DDDBBBBOOBBBBBBBBBBBBBBOOBBBBDDD           ",
    "    DDDBBBBOOYYBBBBBBBBBBBBOOYYBBBBDDD          ",
    "   DDDBBBBOOYYYYBBBBBBBBBBOOYYYYBBBBDDD         ",
    "  DDDBBBBOOYYOOBBBBBBBBBBBBOOYYOOBBBBDDD        ",
    " DDDBBBBOOOOOOBBBBBBBBBBBBBBOOOOOOBBBBDDD       ",
    "DDDBBBBBOOOBBBBBBBBBBBBBBBBBBBBOOOBBBBBDDD      ",
    "  DDDDOOOODDDDDDDDDDDDDDDDDDDDDDOOOODDDD        ",
    "     OOOO                          OOOO         ",
    "     OOO                            OOO         ",
    "     OO                              OO         ",
] + ["                                                "] * 19

player_frames = [
    draw_sprite(player_idle, player_colors),
    draw_sprite(player_idle, player_colors),
    draw_sprite(player_idle, player_colors),
    draw_sprite(player_idle, player_colors),
    draw_sprite(player_thrust, player_colors),
    draw_sprite(player_thrust, player_colors),
]

player_spritesheet = create_spritesheet(player_frames, 48, 48)
with open('assets/sprites/player.png', 'wb') as f:
    f.write(player_spritesheet)
print("✓ Created assets/sprites/player.png (288x96, 48x48 frames)")

# Generate projectiles.png (16x16 frames)
print("Generating projectiles.png...")
projectile_colors = {
    ' ': (0, 0, 0, 0),
    'Y': (255, 255, 0, 255),     # Yellow
    'W': (255, 255, 255, 255),   # White
    'R': (255, 0, 0, 255),       # Red
    'O': (255, 100, 0, 255),     # Orange
}

player_bullet = [
    "      YYYY      ",
    "     YYYYYY     ",
    "    YYYYYYYY    ",
    "   YYWWWWWWYY   ",
    "  YYWWWWWWWWYY  ",
    " YYWWWWWWWWWWYY ",
    " YYWWWWWWWWWWYY ",
    "YYWWWWWWWWWWWWYY",
    "YYWWWWWWWWWWWWYY",
    " YYWWWWWWWWWWYY ",
    " YYWWWWWWWWWWYY ",
    "  YYWWWWWWWWYY  ",
    "   YYWWWWWWYY   ",
    "    YYYYYYYY    ",
    "     YYYYYY     ",
    "      YYYY      ",
]

enemy_bullet = [
    "      RRRR      ",
    "     RRRRRR     ",
    "    RRRRRRRR    ",
    "   RROOOOOORRR  ",
    "  RROOOOOOOOORR ",
    " RROOOOOOOOOOORR",
    " RROOOOOOOOOOORR",
    "RROOOOOOOOOOOOORR",
    "RROOOOOOOOOOOOORR",
    " RROOOOOOOOOOORR",
    " RROOOOOOOOOOORR",
    "  RROOOOOOOOORR ",
    "   RROOOOOORRR  ",
    "    RRRRRRRR    ",
    "     RRRRRR     ",
    "      RRRR      ",
]

projectile_frames = [
    draw_sprite(player_bullet, projectile_colors),
    draw_sprite(player_bullet, projectile_colors),
    draw_sprite(enemy_bullet, projectile_colors),
    draw_sprite(enemy_bullet, projectile_colors),
]

projectiles_spritesheet = create_spritesheet(projectile_frames, 16, 16)
with open('assets/sprites/projectiles.png', 'wb') as f:
    f.write(projectiles_spritesheet)
print("✓ Created assets/sprites/projectiles.png (96x16, 16x16 frames)")

print("\n✓ All sprite sheets generated successfully!")
print("\nSprite sheets created:")
print("  - assets/sprites/cow.png (cow with spots and horns)")
print("  - assets/sprites/sheep.png (fluffy white sheep)")
print("  - assets/sprites/goat.png (goat with horns and beard)")
print("  - assets/sprites/alpaca.png (alpaca with long neck)")
print("  - assets/sprites/player.png (player spaceship)")
print("  - assets/sprites/projectiles.png (bullets)")
print("\nYou can now test the sprites at http://localhost:8080/sprite-example.html")
