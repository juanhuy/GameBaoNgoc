# levels.py

# Để tăng độ khó, ta tăng số lượng ô (kích thước lưới) và số lớp (layers) đè lên nhau.
# Lưới tối đa nên là 6 hàng (để không bị chèn vào khay chứa) x 12 cột.

LEVELS = {
    1: { # Khởi động (Dễ)
        "layers": [[3, 4]], # 12 ô
        "types": 3
    },
    2: { # Bắt đầu có lớp đè
        "layers": [[4, 4], [2, 2]], # 20 ô
        "types": 4
    },
    3: {
        "layers": [[4, 6], [2, 4]], # 32 ô
        "types": 5
    },
    4: {
        "layers": [[5, 6], [3, 4], [1, 2]], # 44 ô
        "types": 6
    },
    5: { # Chồng nhiều lớp
        "layers": [[5, 7], [5, 5], [3, 3]], # 69 ô
        "types": 8
    },
    6: {
        "layers": [[6, 8], [4, 6], [2, 4], [1, 1]], # 81 ô
        "types": 9
    },
    7: {
        "layers": [[6, 9], [5, 7], [4, 5], [2, 3]], # 115 ô
        "types": 11
    },
    8: { # Ác mộng bắt đầu
        "layers": [[6, 10], [6, 8], [4, 6], [2, 4]], # 140 ô
        "types": 13
    },
    9: { # Cực khó
        "layers": [[6, 11], [5, 9], [4, 7], [3, 5], [2, 3]], # 160 ô
        "types": 15
    },
    10: { # Boss level (Như Cừu và Cừu)
        "layers": [[6, 12], [6, 10], [5, 8], [4, 6], [3, 4], [2, 2]], # 212 ô xếp chồng 6 lớp!
        "types": 16
    }
}
