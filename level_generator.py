import random

def generate_level_data(level_num):
    """
    Thuật toán sinh màn chơi vô hạn dựa trên số Level.
    Càng Level cao, số lớp càng dày, số loại ô càng nhiều và mật độ ô càng lớn.
    """
    
    # 1. Tính toán số loại ô (tối thiểu 3, tối đa 16)
    num_types = min(3 + (level_num // 2), 16)
    
    # 2. Tính toán số lớp (Layers)
    # Level 1: 1 lớp, Level 10: 6 lớp, Level 50: ~10 lớp (giới hạn để tránh quá lag)
    num_layers = min(1 + (level_num // 3), 10)
    
    layers = []
    
    # 3. Tính toán kích thước lưới cho từng lớp
    # Ta giới hạn Rows tối đa là 6, Cols tối đa là 12 để vừa màn hình
    for i in range(num_layers):
        # Càng lớp trên (i cao), kích thước có thể nhỏ dần hoặc ngẫu nhiên
        # Nhưng phải đảm bảo không quá nhỏ
        max_r = min(4 + (level_num // 10), 6)
        max_c = min(4 + (level_num // 5), 12)
        
        rows = random.randint(3, max_r)
        cols = random.randint(3, max_c)
        layers.append([rows, cols])
    
    # 4. Đảm bảo tổng số ô chia hết cho 3 (sẽ được xử lý trong setup_level ở main.py)
    
    return {
        "layers": layers,
        "types": num_types
    }
