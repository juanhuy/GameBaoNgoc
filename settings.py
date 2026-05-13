# settings.py

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FPS = 60

# Tile dimensions
TILE_WIDTH = 70
TILE_HEIGHT = 70

# Colors
BACKGROUND_COLOR = (245, 240, 235)  # Soft warm beige background
TILE_BORDER_COLOR = (255, 255, 255) # White border for a clean look
TEXT_COLOR = (60, 60, 60)
BLOCKED_COLOR = (0, 0, 0, 100)      # Lighter shadow for blocked tiles
TRAY_BG_COLOR = (220, 215, 210)     # Slightly darker than bg
SHADOW_COLOR = (200, 190, 180)      # Soft shadow

# Bảng màu Pastel cho các loại ô (lên đến 16 loại)
PASTEL_COLORS = [
    (255, 179, 186), # 1: Soft Pink
    (255, 223, 186), # 2: Peach
    (255, 255, 186), # 3: Pale Yellow
    (186, 255, 201), # 4: Mint Green
    (186, 225, 255), # 5: Light Blue
    (220, 208, 255), # 6: Lavender
    (255, 204, 229), # 7: Rose
    (204, 255, 229), # 8: Seafoam
    (204, 229, 255), # 9: Ice Blue
    (229, 204, 255), # 10: Lilac
    (255, 230, 204), # 11: Apricot
    (230, 255, 204), # 12: Lime Pastel
    (255, 204, 204), # 13: Salmon Light
    (204, 255, 204), # 14: Mint Light
    (204, 204, 255), # 15: Periwinkle
    (255, 218, 185)  # 16: Peach Puff
]

# Game settings
MAX_TRAY_SIZE = 7

# Animation settings
SLIDE_SPEED = 0.15 # Tốc độ trượt (Lerp factor)
