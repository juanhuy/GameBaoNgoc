import pygame
import random
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BACKGROUND_COLOR, TRAY_BG_COLOR, TILE_WIDTH, TILE_HEIGHT, MAX_TRAY_SIZE
from tile import Tile, create_text_tile_image
from game import check_blocked, add_to_tray
from level_generator import generate_level_data
from effects import EffectManager

def load_assets():
    """Load các ảnh từ thư mục assets nếu có."""
    icons = {}
    assets_path = "assets"
    if os.path.exists(assets_path):
        for i in range(1, 17): 
            img_path = os.path.join(assets_path, f"{i}.png")
            if os.path.exists(img_path):
                try:
                    icons[i] = pygame.image.load(img_path).convert_alpha()
                except:
                    print(f"Không thể load ảnh: {img_path}")
    return icons

def setup_level(level_num, font, icons_cache):
    level_data = generate_level_data(level_num)
    layers_config = level_data["layers"]
    num_types = level_data["types"]
    
    total_tiles_count = 0
    for layer in layers_config:
        total_tiles_count += layer[0] * layer[1]
    
    valid_total = (total_tiles_count // 3) * 3
    
    tile_types = []
    for i in range(valid_total // 3):
        t_type = (i % num_types) + 1
        tile_types.extend([t_type, t_type, t_type])
    
    random.shuffle(tile_types)
    
    all_tiles = []
    tile_idx = 0
    
    image_cache = {}
    for t in set(tile_types):
        icon = icons_cache.get(t)
        image_cache[t] = create_text_tile_image(t, font, icon)
    
    for z, layer in enumerate(layers_config):
        rows, cols = layer
        layer_width = cols * (TILE_WIDTH + 5)
        layer_height = rows * (TILE_HEIGHT + 5)
        
        start_x = (SCREEN_WIDTH - layer_width) // 2 + (z * 15) + random.randint(-20, 20)
        start_y = (SCREEN_HEIGHT - layer_height) // 2 - 50 + (z * 15) + random.randint(-20, 20)
        
        for r in range(rows):
            for c in range(cols):
                if tile_idx < len(tile_types):
                    t_type = tile_types[tile_idx]
                    img = image_cache[t_type]
                    tile = Tile(start_x + c * (TILE_WIDTH + 5), start_y + r * (TILE_HEIGHT + 5), z, t_type, img)
                    all_tiles.append(tile)
                    tile_idx += 1
                    
    return all_tiles

def draw_rounded_panel(surface, rect, color, border_color=None, border_width=2, radius=15):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border_color:
        pygame.draw.rect(surface, border_color, rect, width=border_width, border_radius=radius)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Ghép Ô - Match 3 (Fireworks Edition)")
    clock = pygame.time.Clock()
    
    icons_cache = load_assets()
    effects = EffectManager()
    
    try:
        font = pygame.font.SysFont("Segoe UI", 24, bold=True)
        font_large = pygame.font.SysFont("Segoe UI", 40, bold=True)
        font_huge = pygame.font.SysFont("Segoe UI", 60, bold=True)
    except:
        font = pygame.font.Font(None, 24)
        font_large = pygame.font.Font(None, 48)
        font_huge = pygame.font.Font(None, 72)
        
    current_level = 1
    all_tiles = setup_level(current_level, font, icons_cache)
    tray = []
    game_over = False
    win = False
    level_complete = False
    triggered_lv_effect = False
    
    dark_surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(dark_surface, (0, 0, 0, 130), dark_surface.get_rect(), border_radius=12)
    
    running = True
    while running:
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = event.pos
                    
                    if win or game_over or level_complete:
                        if win or level_complete:
                            current_level += 1
                        
                        all_tiles = setup_level(current_level, font, icons_cache)
                        tray = []
                        game_over = False
                        win = False
                        level_complete = False
                        triggered_lv_effect = False
                        continue

                    clicked_tile = None
                    sorted_for_click = sorted([t for t in all_tiles if not t.in_tray], key=lambda x: x.z, reverse=True)
                    
                    for tile in sorted_for_click:
                        if tile.rect.collidepoint(pos):
                            is_blocked = check_blocked(tile, [t for t in all_tiles if not t.in_tray])
                            if not is_blocked:
                                clicked_tile = tile
                                break
                                
                    if clicked_tile:
                        success, matched = add_to_tray(clicked_tile, tray)
                        if not success:
                            game_over = True
                        if matched:
                            # Hiệu ứng nổ pháo hoa giấy tại khay
                            effects.create_confetti(clicked_tile.rect.centerx, clicked_tile.rect.centery, count=40)
                            
        # Cập nhật
        for tile in all_tiles:
            tile.update_animation()
        
        effects.update()
                            
        if not game_over and not level_complete:
            for tile in all_tiles:
                if not tile.in_tray:
                    tile.is_blocked = check_blocked(tile, [t for t in all_tiles if not t.in_tray])
                
            active_tiles = [t for t in all_tiles if not t.in_tray]
            if len(active_tiles) == 0 and len(tray) == 0:
                level_complete = True
                if current_level >= 10 and not triggered_lv_effect: # Có thể coi là win sau 10 level hoặc cứ tiếp tục
                    win = True
            
        # Kích hoạt hiệu ứng lên level
        if (level_complete or win) and not triggered_lv_effect:
            effects.create_level_up(SCREEN_WIDTH, SCREEN_HEIGHT)
            triggered_lv_effect = True
            
        # Vẽ
        screen.fill(BACKGROUND_COLOR)
        
        header_rect = pygame.Rect(20, 20, 180, 50)
        draw_rounded_panel(screen, header_rect, (255, 255, 255), (200, 200, 200))
        level_text = font.render(f"LEVEL {current_level}", True, (50, 50, 50))
        screen.blit(level_text, (header_rect.centerx - level_text.get_width()//2, header_rect.centery - level_text.get_height()//2))
        
        tray_rect = pygame.Rect(170, SCREEN_HEIGHT - 150, 660, 120)
        tray_surface = pygame.Surface((660, 120), pygame.SRCALPHA)
        draw_rounded_panel(tray_surface, tray_surface.get_rect(), (255, 255, 255, 120), (255, 255, 255, 200), radius=20)
        screen.blit(tray_surface, (170, SCREEN_HEIGHT - 150))
        
        tiles_to_draw = sorted([t for t in all_tiles if not t.in_tray], key=lambda t: t.z)
        
        for tile in tiles_to_draw:
            screen.blit(tile.image, tile.rect)
            if tile.is_blocked:
                screen.blit(dark_surface, tile.rect)
                
        for tile in tray:
            screen.blit(tile.image, tile.rect)
            
        # Vẽ hiệu ứng lên trên các ô
        effects.draw(screen)
            
        if win or level_complete or game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0,0))
            
            panel_rect = pygame.Rect(SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT//2 - 120, 500, 240)
            draw_rounded_panel(screen, panel_rect, (255, 255, 255), (200, 200, 200), radius=25)
            
            if win:
                msg = font_large.render("XUẤT SẮC! PHÁ ĐẢO", True, (46, 204, 113))
                desc = font.render("Bạn là bậc thầy ghép ô!", True, (100, 100, 100))
            elif level_complete:
                msg = font_large.render(f"HOÀN THÀNH LEVEL {current_level}", True, (52, 152, 219))
                desc = font.render("Click để sang màn mới", True, (100, 100, 100))
            else:
                msg = font_large.render("THUA RỒI!", True, (231, 76, 60))
                desc = font.render("Khay chứa đã đầy. Click để chơi lại.", True, (100, 100, 100))
                
            screen.blit(msg, (panel_rect.centerx - msg.get_width()//2, panel_rect.y + 60))
            screen.blit(desc, (panel_rect.centerx - desc.get_width()//2, panel_rect.y + 130))
            
        pygame.display.flip()
        clock.tick(FPS)
        
    pygame.quit()

if __name__ == "__main__":
    main()
