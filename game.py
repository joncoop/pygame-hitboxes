# Imports
import pygame


WIDTH = 600
HEIGHT = 600
TITLE = "Custom Hit Boxes"
FPS = 60


# callback function (what's that mean?)
def hitbox_collide(sprite1, sprite2):
    return sprite1.hitbox.colliderect(sprite2.hitbox)


# Sprites
class Entity(pygame.sprite.Sprite):

    def __init__(self, image, location, hitbox_size=None, hitbox_anchor='center'):
        '''
        hitbox_size should be an ordered pair in the form [width, height].
        hitbox_anchor is any valid rectangle alignment attribute that is
        an ordered pair.
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
        
        self.hitbox_anchor = hitbox_anchor
        self.hitbox.center = location
        self.align_hitbox()

    def move_x(self):
        self.hitbox.x += self.vx
        self.align_hitbox()

    def move_y(self):
        self.hitbox.y += self.vy
        self.align_hitbox()

    def check_collisions_x(self, group):
        hits = pygame.sprite.spritecollide(self, group, False, hitbox_collide)

        for hit in hits:
            if self.vx < 0:
                self.hitbox.left = hit.hitbox.right
            elif self.vx > 0:
                self.hitbox.right = hit.hitbox.left

            self.align_hitbox()

    def check_collisions_y(self, group):
        hits = pygame.sprite.spritecollide(self, group, False, hitbox_collide)

        for hit in hits:
            if self.vy < 0:
                self.hitbox.top = hit.hitbox.bottom
            elif self.vy > 0:
                self.hitbox.bottom = hit.hitbox.top

            self.align_hitbox()

    def align_hitbox(self):
        #self.rect.center = self.hitbox.center
        attribute_value = getattr(self.hitbox, self.hitbox_anchor)
        setattr(self.rect, self.hitbox_anchor, attribute_value)


class Wall(Entity):

    def __init__(self, image, location, *args):
        super().__init__(image, location, *args)    


class Player(Entity):

    def __init__(self, image, location, *args):
        super().__init__(image, location, *args)    

    def go_up(self):
        self.vy = -5

    def go_down(self):
        self.vy = 5

    def go_left(self):
        self.vx = -5

    def go_right(self):
        self.vx = 5

    def stop_x(self):
        self.vx = 0

    def stop_y(self):
        self.vy = 0

    def update(self, obstacles):
        self.move_x()
        self.check_collisions_x(obstacles)

        self.move_y()
        self.check_collisions_y(obstacles)


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

        self.p1 = Player(p1_img, [150, 150], [80, 80], 'midbottom')
    
        obstacle_img = pygame.Surface([100, 100])
        obstacle_img.fill(pygame.Color('green'))
  
        obstacle_1 = Wall(obstacle_img, [200, 400])
        obstacle_2 = Wall(obstacle_img, [400, 200])

        self.players = pygame.sprite.GroupSingle(self.p1)
        self.obstacles = pygame.sprite.Group(obstacle_1, obstacle_2)

    def process_input(self):
        pressed = pygame.key.get_pressed()
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        if pressed[pygame.K_UP]:
            self.p1.go_up()
        elif pressed[pygame.K_DOWN]:
            self.p1.go_down()
        else:
            self.p1.stop_y()
            
        if pressed[pygame.K_LEFT]:
            self.p1.go_left()
        elif pressed[pygame.K_RIGHT]:
            self.p1.go_right()
        else:
            self.p1.stop_x()

    def update(self):
        self.players.update(self.obstacles) 

    def render(self):
        self.screen.fill(pygame.Color('black'))
        self.players.draw(self.screen)
        self.obstacles.draw(self.screen)

        for p in self.players:
            pygame.draw.rect(self.screen, pygame.Color('white'), p.hitbox)

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
