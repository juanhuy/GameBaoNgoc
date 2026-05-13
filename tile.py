import pygame
from settings import TILE_WIDTH, TILE_HEIGHT, TILE_BORDER_COLOR, TEXT_COLOR, PASTEL_COLORS, SLIDE_SPEED

class Tile:
    def __init__(self, x, y, z, tile_type, image):
        self.rect = pygame.Rect(x, y, TILE_WIDTH, TILE_HEIGHT)
        # Tọa độ thực tế (cho animation mượt)
        self.current_x = float(x)
        self.current_y = float(y)
        self.target_x = float(x)
        self.target_y = float(y)
        
        self.z = z
        self.tile_type = tile_type
        self.image = image
        self.is_blocked = False
        self.in_tray = False

    def update_animation(self):
        # Lerp (Nội suy tuyến tính) để tạo cảm giác trượt mượt mà
        if abs(self.target_x - self.current_x) > 0.5:
            self.current_x += (self.target_x - self.current_x) * SLIDE_SPEED
        else:
            self.current_x = self.target_x
            
        if abs(self.target_y - self.current_y) > 0.5:
            self.current_y += (self.target_y - self.current_y) * SLIDE_SPEED
        else:
            self.current_y = self.target_y
            
        # Cập nhật rect thực tế để vẽ và kiểm tra click
        self.rect.x = int(self.current_x)
        self.rect.y = int(self.current_y)

def create_text_tile_image(tile_type, font, icon_image=None):
    """Tạo một Surface cho ô, bo góc, có bóng 3D. Nếu có icon_image thì vẽ icon."""
    color_idx = (tile_type - 1) % len(PASTEL_COLORS)
    bg_color = PASTEL_COLORS[color_idx]
    
    # Tạo surface trong suốt
    surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT), pygame.SRCALPHA)
    
    border_radius = 12
    
    # 1. Vẽ phần đổ bóng sâu
    shadow_h = 6
    shadow_color = (max(0, bg_color[0]-50), max(0, bg_color[1]-50), max(0, bg_color[2]-50))
    shadow_rect = pygame.Rect(0, shadow_h, TILE_WIDTH, TILE_HEIGHT - shadow_h)
    pygame.draw.rect(surface, shadow_color, shadow_rect, border_radius=border_radius)
    
    # Vẽ thêm một lớp bóng đen nhẹ dưới cùng
    pygame.draw.rect(surface, (0, 0, 0, 60), pygame.Rect(2, shadow_h + 2, TILE_WIDTH-4, TILE_HEIGHT-(shadow_h+2)), border_radius=border_radius)
    
    # 2. Vẽ thân chính của mặt trên ô
    main_rect = pygame.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT - shadow_h)
    pygame.draw.rect(surface, bg_color, main_rect, border_radius=border_radius)
    
    # 3. Vẽ viền sáng tạo cảm giác bóng bẩy
    pygame.draw.rect(surface, TILE_BORDER_COLOR, main_rect, width=3, border_radius=border_radius)
    
    # 4. Highlight nội viền trên cùng
    highlight_rect = pygame.Rect(3, 3, TILE_WIDTH - 6, (TILE_HEIGHT - shadow_h) // 2)
    highlight_surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(highlight_surface, (255, 255, 255, 80), highlight_rect, border_radius=border_radius-2)
    surface.blit(highlight_surface, (0,0))
    
    if icon_image:
        # Scale icon để vừa khít trong ô (khoảng 50x50)
        try:
            scaled_icon = pygame.transform.smoothscale(icon_image, (50, 50))
            icon_rect = scaled_icon.get_rect(center=(TILE_WIDTH // 2, (TILE_HEIGHT - shadow_h) // 2))
            surface.blit(scaled_icon, icon_rect)
        except:
            # Nếu lỗi khi scale, quay lại vẽ số
            text_surface = font.render(str(tile_type), True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=(TILE_WIDTH // 2, (TILE_HEIGHT - shadow_h) // 2))
            surface.blit(text_surface, text_rect)
    else:
        # Vẽ chữ ở giữa thân chính
        text_surface = font.render(str(tile_type), True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(TILE_WIDTH // 2, (TILE_HEIGHT - shadow_h) // 2))
        surface.blit(text_surface, text_rect)
    
    return surface
