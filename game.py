# Imports
import pygame


# Screen settings
WIDTH = 600
HEIGHT = 600
TITLE = "Custom Hit Boxes"
FPS = 60


# Player settings
P1_CONTROLS = {'up': pygame.K_w,
               'down': pygame.K_s,
               'left': pygame.K_a,
               'right': pygame.K_d}

P2_CONTROLS = {'up': pygame.K_UP,
               'down': pygame.K_DOWN,
               'left': pygame.K_LEFT,
               'right': pygame.K_RIGHT}

PLAYER_SPEED = 5


# Collision callback function
def hitbox_collide(sprite1, sprite2):
    return sprite1.hitbox.colliderect(sprite2.hitbox)


# Sprites
class Entity(pygame.sprite.Sprite):

    def __init__(self, image, location, hitbox_size=None, hitbox_anchor='center'):
        '''
        hitbox_size should be an ordered pair in the form [width, height].
        hitbox_anchor is any valid Rect positioning attribute. If the Rect
        attribute is not an ordered pair, then the hitbox will be centered
        on the other axis.
        '''
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.vx = 0
        self.vy = 0

        if hitbox_size is None:
            self.hitbox = self.rect
        else:
            w, h = hitbox_size
            self.hitbox = pygame.rect.Rect([0, 0, w, h])
        
        transformations = {'x': 'midleft',
                           'y': 'midtop',
                           'top': 'midtop',
                           'bottom': 'midbottom',
                           'left': 'midleft',
                           'right': 'midright',
                           'centerx': 'center',
                           'centery': 'center'}
        
        if hitbox_anchor in transformations:
            hitbox_anchor = transformations[hitbox_anchor]

        self.hitbox_anchor = hitbox_anchor
        self.hitbox.center = location
        self.align_rect_to_hitbox()

    def move_x(self):
        self.hitbox.x += self.vx
        self.align_rect_to_hitbox()

    def move_y(self):
        self.hitbox.y += self.vy
        self.align_rect_to_hitbox()

    def check_collisions_x(self, group):
        hits = pygame.sprite.spritecollide(self, group, False, hitbox_collide)
        hits.remove(self)

        for hit in hits:
            if self.vx < 0:
                self.hitbox.left = hit.hitbox.right
            elif self.vx > 0:
                self.hitbox.right = hit.hitbox.left

        self.align_rect_to_hitbox()

    def check_collisions_y(self, group):
        hits = pygame.sprite.spritecollide(self, group, False, hitbox_collide)
        hits.remove(self)

        for hit in hits:
            if self.vy < 0:
                self.hitbox.top = hit.hitbox.bottom
            elif self.vy > 0:
                self.hitbox.bottom = hit.hitbox.top

        self.align_rect_to_hitbox()

    def check_screen_edges(self):
        if self.hitbox.left < 0:
            self.hitbox.left = 0
        elif self.hitbox.right > WIDTH:
            self.hitbox.right = WIDTH
            
        if self.hitbox.top < 0:
            self.hitbox.top = 0
        elif self.hitbox.bottom > WIDTH:
            self.hitbox.bottom = WIDTH

        self.align_rect_to_hitbox()
            
    def align_rect_to_hitbox(self):
        attribute_value = getattr(self.hitbox, self.hitbox_anchor)
        setattr(self.rect, self.hitbox_anchor, attribute_value)


class Block(Entity):

    def __init__(self, image, location, *args):
        super().__init__(image, location, *args)    


class Player(Entity):

    def __init__(self, image, location, controls, *args):
        super().__init__(image, location, *args)    
        self.controls = controls

    def act(self, pressed):
        if pressed[self.controls['up']]:
            self.vy = -1 * PLAYER_SPEED
        elif pressed[self.controls['down']]:
            self.vy = PLAYER_SPEED
        else:
            self.vy = 0
            
        if pressed[self.controls['left']]:
            self.vx = -1 * PLAYER_SPEED
        elif pressed[self.controls['right']]:
            self.vx = PLAYER_SPEED
        else:
            self.vx = 0

    def update(self, collidables):
        self.move_x()
        self.check_collisions_x(collidables)
        self.move_y()
        self.check_collisions_y(collidables)
        self.check_screen_edges()


# Main game class 
class Game:
    
    def __init__(self):
        # Initialize pygame
        pygame.mixer.pre_init()
        pygame.init()

        # Make window
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.make_sprites()

    def make_sprites(self):
        p1_img = pygame.Surface([100, 100])
        p1_img.fill(pygame.Color('red'))

        p2_img = pygame.Surface([100, 100])
        p2_img.fill(pygame.Color('green'))

        p1 = Player(p1_img, [200, 200], P1_CONTROLS, [80, 80], 'midbottom')
        p2 = Player(p2_img, [400, 400], P2_CONTROLS, [80, 80], 'center')
    
        block_img = pygame.Surface([100, 100])
        block_img.fill(pygame.Color('blue'))
  
        b1 = Block(block_img, [200, 400])
        b2 = Block(block_img, [400, 200], [80, 80], 'left')

        self.players = pygame.sprite.Group(p1, p2)
        self.all_sprites = pygame.sprite.Group(p1, p2, b1, b2)

    def process_input(self):
        pressed = pygame.key.get_pressed()
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


        for player in self.players:
            player.act(pressed)

    def update(self):
        self.all_sprites.update(self.all_sprites) 

    def render(self):
        self.screen.fill(pygame.Color('lightgray'))
        self.all_sprites.draw(self.screen)

        for sprite in self.all_sprites:
            pygame.draw.rect(self.screen, pygame.Color('black'), sprite.hitbox, 2)

    def run(self):
        while self.running:
            self.process_input()     
            self.update()     
            self.render()
            
            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()


def main():
   g = Game()
   g.run()

   
if __name__ == "__main__":
    main()
