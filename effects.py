import pygame
import random
import math

class ConfettiParticle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(5, 10)
        
        # Tốc độ ban đầu (văng ra mọi hướng)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 7)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed - 5 # Cho bay lên một chút
        
        self.gravity = 0.2
        self.rotation = random.uniform(0, 360)
        self.rot_speed = random.uniform(-10, 10)
        self.life = 1.0 # 100% sự sống
        self.fade_speed = random.uniform(0.01, 0.03)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity # Trọng lực kéo xuống
        self.rotation += self.rot_speed
        self.life -= self.fade_speed
        
    def draw(self, surface):
        if self.life <= 0:
            return
            
        # Tính toán alpha (độ mờ)
        alpha = int(self.life * 255)
        
        # Vẽ một mảnh giấy hình chữ nhật xoay
        s = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        s.fill((*self.color, alpha))
        rotated_s = pygame.transform.rotate(s, self.rotation)
        surface.blit(rotated_s, (self.x, self.y))

class EffectManager:
    def __init__(self):
        self.particles = []

    def create_confetti(self, x, y, count=20):
        colors = [
            (255, 50, 50), (50, 255, 50), (50, 50, 255),
            (255, 255, 50), (255, 50, 255), (50, 255, 255)
        ]
        for _ in range(count):
            color = random.choice(colors)
            self.particles.append(ConfettiParticle(x, y, color))

    def create_level_up(self, screen_width, screen_height):
        # Nổ pháo hoa ở nhiều điểm trên màn hình
        for _ in range(5):
            x = random.randint(100, screen_width - 100)
            y = random.randint(100, screen_height - 300)
            self.create_confetti(x, y, count=50)

    def update(self):
        for p in self.particles[:]:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)
