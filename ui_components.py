"""Simple solid-colour UI widgets. No gradient buttons anywhere."""
import pygame


def font(size, bold=False):
    return pygame.font.Font(None, size)


def text(surface, string, x, y, size=28, color=(255, 255, 255), bold=False, center=False):
    f = font(size, bold)
    img = f.render(string, True, color)
    rect = img.get_rect()
    rect.center = (x, y) if center else (x + rect.width // 2, y + rect.height // 2)
    # pygame Font render with topleft fallback: draw at rect.topleft
    surface.blit(img, rect.topleft)
    return rect


def draw_text(surface, string, pos, size=28, color=(255, 255, 255), bold=False):
    img = font(size, bold).render(string, True, color)
    surface.blit(img, pos)
    return img.get_rect(topleft=pos)


class Button:
    """Solid-colour rectangular button. Returns True on click."""

    def __init__(self, rect, label, bg=(255, 190, 20), fg=(20, 20, 20), size=28):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.bg = bg
        self.fg = fg
        self.size = size

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg, self.rect, border_radius=14)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=14)
        img = font(self.size, True).render(self.label, True, self.fg)
        surface.blit(img, img.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


def panel(surface, rect, bg=(10, 20, 50), border=(60, 180, 255)):
    pygame.draw.rect(surface, bg, rect, border_radius=18)
    pygame.draw.rect(surface, border, rect, 2, border_radius=18)
