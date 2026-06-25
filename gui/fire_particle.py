import pygame, math, random 

class FireParticle:
    def __init__(self, x, y):
        self.pos = [x, y]
        # Fire starts fast and spreads out
        self.vel = [random.uniform(-1.5, 1.5), random.uniform(3, 7)]
        self.life = random.randint(40, 80)
        self.max_life = self.life

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.life -= 1

    def draw(self, surface):
        ratio = self.life / self.max_life
        # 1. Realism: Size starts small and GROWS as it turns to smoke
        size = int((1 - ratio) * 20 + 5)
        
        # 2. Realism: Color shift (White -> Yellow -> Orange -> Grey)
        if ratio > 0.8: color = (255, 255, 200) # Hot White
        elif ratio > 0.4: color = (255, 150, 0) # Orange
        elif ratio > 0.2: color = (200, 50, 0)  # Red-ish
        else: color = (60, 60, 60)              # Smoke Grey

        # 3. Realism: Fade out
        alpha = int(ratio * 255)
        
        p_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(p_surf, (*color, alpha), (size, size), size)
        surface.blit(p_surf, (self.pos[0] - size, self.pos[1] - size))

