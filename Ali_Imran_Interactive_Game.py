import pygame
import sys
import os
import math
import arabic_reshaper
from bidi.algorithm import get_display

# Pygame Initialize
pygame.init()

# Screen Setup
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ali Imran - Real Images & Interactive Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
BLUE = (50, 150, 255)

# Clock & FPS
clock = pygame.time.Clock()
FPS = 60

def fix_urdu(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

# Font Load
try:
    font = pygame.font.SysFont("arial", 22)
    large_font = pygame.font.SysFont("arial", 32)
except:
    font = pygame.font.Font(None, 24)
    large_font = pygame.font.Font(None, 36)

# Player Class with Custom Face/Sprite Image Support
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 60
        self.height = 90
        
        # Load Character Face/Sprite if available (e.g. face.png or scene0.png)
        self.raw_image = None
        if os.path.exists("face.png"):
            try:
                self.raw_image = pygame.image.load("face.png").convert_alpha()
                self.raw_image = pygame.transform.scale(self.raw_image, (self.width, self.height))
            except:
                self.raw_image = None
        elif os.path.exists("scene0.png"):
            try:
                self.raw_image = pygame.image.load("scene0.png").convert_alpha()
                self.raw_image = pygame.transform.scale(self.raw_image, (self.width, self.height))
            except:
                self.raw_image = None

        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0
        self.speed_y = 0
        self.is_jumping = False
        self.facing_right = True
        self.anim_frame = 0

    def update(self):
        # Gravity
        self.speed_y += 0.8
        
        # Direction
        if self.speed_x > 0:
            self.facing_right = True
            self.anim_frame += 1
        elif self.speed_x < 0:
            self.facing_right = False
            self.anim_frame += 1

        self.rect.x += self.speed_x
        
        # Ground Collision
        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.speed_y = 0
            self.is_jumping = False

        self.rect.y += self.speed_y

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # Draw Player Surface
        self.image.fill((0, 0, 0, 0))
        if self.raw_image:
            img_to_draw = self.raw_image
            if not self.facing_right:
                img_to_draw = pygame.transform.flip(self.raw_image, True, False)
            
            # Slight bounce effect while walking
            bounce = int(math.sin(self.anim_frame * 0.3) * 3) if self.speed_x != 0 else 0
            self.image.blit(img_to_draw, (0, bounce))
        else:
            # Fallback Default Drawing
            pygame.draw.rect(self.image, BLUE, (10, 20, 40, 60), border_radius=5)

    def jump(self):
        if not self.is_jumping:
            self.speed_y = -15
            self.is_jumping = True

# Collectible Mission Class using Real Scene Images
class MissionItem(pygame.sprite.Sprite):
    def __init__(self, x, y, img_file):
        super().__init__()
        self.width = 70
        self.height = 70
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        if os.path.exists(img_file):
            try:
                loaded_img = pygame.image.load(img_file).convert_alpha()
                self.image = pygame.transform.scale(loaded_img, (self.width, self.height))
            except:
                pygame.draw.rect(self.image, GOLD, (0, 0, self.width, self.height))
        else:
            pygame.draw.rect(self.image, GOLD, (0, 0, self.width, self.height))
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Main Game Loop
def main():
    player = Player(50, SCREEN_HEIGHT - 140)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    missions = [
        {"title": "1. سڈنی بار سے جوا جیت کر رقم حاصل کریں", "x": 200, "image": "scene1.png"},
        {"title": "2. جوئے کی رقم سے ہتھیار اور ہیکنگ ڈیوائس خریدیں", "x": 380, "image": "scene2.png"},
        {"title": "3. کمپیوٹر ہیک کر کے لیبارٹری کا نقشہ حاصل کریں", "x": 560, "image": "scene3.png"},
        {"title": "4. لیبارٹری کو دھماکے سے تباہ کر کے مشن مکمل کریں!", "x": 740, "image": "scene8.png"}
    ]

    # Background Image Load Support (scene0.png)
    bg_image = None
    if os.path.exists("scene0.png"):
        try:
            bg_image = pygame.image.load("scene0.png").convert()
            bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT - 50))
        except:
            bg_image = None

    current_mission_idx = 0
    current_item = MissionItem(missions[0]["x"], SCREEN_HEIGHT - 120, missions[0]["image"])
    all_sprites.add(current_item)

    game_over = False

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    player.speed_x = -4
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    player.speed_x = 4
                elif event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d):
                    player.speed_x = 0

        if not game_over:
            all_sprites.update()

            if current_item and pygame.sprite.collide_rect(player, current_item):
                current_item.kill()
                current_mission_idx += 1
                
                if current_mission_idx < len(missions):
                    m_data = missions[current_mission_idx]
                    current_item = MissionItem(m_data["x"], SCREEN_HEIGHT - 120, m_data["image"])
                    all_sprites.add(current_item)
                else:
                    current_item = None
                    game_over = True

        # Render Background
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill(BLACK)

        # Ground
        pygame.draw.rect(screen, (50, 50, 50), (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        
        all_sprites.draw(screen)

        # Render UI
        if not game_over:
            mission_text = fix_urdu(missions[current_mission_idx]["title"])
            text_surface = font.render(mission_text, True, WHITE)
            
            # Text Background box for clarity
            pygame.draw.rect(screen, (0, 0, 0, 180), (10, 10, text_surface.get_width() + 20, 40))
            screen.blit(text_surface, (20, 18))
        else:
            win_text = fix_urdu("مشن مکمل! پاکیشیا سیکرٹ سروس کامیاب 🎯")
            win_surface = large_font.render(win_text, True, GREEN)
            pygame.draw.rect(screen, (0, 0, 0, 200), (SCREEN_WIDTH // 6 - 10, SCREEN_HEIGHT // 2 - 30, win_surface.get_width() + 20, 60))
            screen.blit(win_surface, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2 - 20))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()