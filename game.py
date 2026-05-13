import pygame
from settings import SCREEN_HEIGHT, TILE_WIDTH, TILE_HEIGHT, MAX_TRAY_SIZE

def check_blocked(target_tile, all_tiles):
    """Kiểm tra xem target_tile có bị ô nào ở lớp trên đè lên không."""
    for other in all_tiles:
        if other.z > target_tile.z and not other.in_tray:
            if target_tile.rect.colliderect(other.rect):
                return True
    return False

def add_to_tray(tile, tray):
    """Thêm ô vào khay, sắp xếp và kiểm tra match. Trả về (success, matched)"""
    if len(tray) >= MAX_TRAY_SIZE:
        return False, False  # Khay đầy, không thêm được
        
    tile.in_tray = True
    tray.append(tile)
    
    # Sắp xếp theo loại để các ô cùng loại đứng cạnh nhau
    tray.sort(key=lambda x: x.tile_type)
    
    # Cập nhật vị trí hiển thị trong khay
    reposition_tray(tray)
    
    # Kiểm tra match 3
    matched = update_tray(tray)
    
    return True, matched

def reposition_tray(tray):
    """Đặt lại vị trí các ô trong khay để chúng nằm cạnh nhau."""
    start_x = 200  # Tọa độ X bắt đầu của khay
    y = SCREEN_HEIGHT - TILE_HEIGHT - 50  # Cách đáy màn hình 50px
    
    for idx, tile in enumerate(tray):
        tile.target_x = start_x + idx * (TILE_WIDTH + 10)
        tile.target_y = y

def update_tray(tray):
    """Xóa 3 ô cùng loại liên tiếp. Trả về True nếu có match."""
    i = 0
    matched = False
    while i <= len(tray) - 3:
        if tray[i].tile_type == tray[i+1].tile_type == tray[i+2].tile_type:
            # Xóa 3 ô cùng loại
            del tray[i:i+3]
            matched = True
            # Cập nhật lại vị trí các ô còn lại trong khay
            reposition_tray(tray)
            continue 
        i += 1
    return matched
