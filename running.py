import pygame, math
from random import randint
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = 'player'
        self.image = pygame.Surface((200,200))
        self.image.fill('Blue')
        self.rect = self.image.get_rect(midbottom=(400,800))

        self.gravity = 0
        self.is_in_greund = True
        self.hovering = False
        self.hovering_start = 0

    def jump(self):
        if self.is_in_greund:
            self.gravity = -40
            self.rect.bottom += self.gravity
            self.is_in_greund = False
    
    def gravity_fall(self,keys):
        if keys[pygame.K_SPACE] and self.gravity > 0 and not self.hovering:
            self.hovering = True
            self.hovering_start = pygame.time.get_ticks()
            self.gravity = 0
        if self.hovering:
            current_time = pygame.time.get_ticks()
            time_elapsed = current_time - self.hovering_start

            if time_elapsed >= 250 or not keys[pygame.K_SPACE]:
                self.gravity += 2.5
        else:
            self.gravity += 2.5
        self.rect.bottom += self.gravity
        if self.rect.bottom >= 800:
            self.rect.bottom = 800
            self.gravity = 0
            self.is_in_greund = True
            self.hovering = False
    
    def update(self,keys):
        self.gravity_fall(keys)

class Enemy(pygame.sprite.Sprite):
    def __init__(self,type,velocity:int):
        super().__init__()
        if type == 'ground':
            enemy_surface=pygame.Surface((100,100))
            position=1900,800
        elif type == 'fly':
            enemy_surface=pygame.Surface((80,80))
            position=1900,500

        self.name = type
        self.has_scored = False
        self.velocity = velocity
        self.image = enemy_surface
        self.image.fill('Red')
        self.rect = self.image.get_rect(midbottom=(position))

    def destroy(self):
        if self.rect.x <= -1000:
            self.kill()

    def update(self):
        self.rect.x -= self.velocity
        self.destroy()

class Text(pygame.sprite.Sprite):
    def __init__(self,name: str,font_size: int,text: str,color: str,position: tuple):
        super().__init__()
        self.name = name
        self.font = pygame.font.Font('graphics/Pixeltype.ttf',font_size)
        self.image = self.font.render(text,False,color)
        self.rect = self.image.get_rect(center=position)


def collision_check(player,enemy_group) ->bool:
    """
    check if there is a collision between a given groupsingle and a group
    """
    hit = pygame.sprite.spritecollideany(player.sprite,enemy_group)
    if hit: return True
    return False
    
def get_sprite(name: str,group):
    """
    take one single sprite for a group and return it
    """
    for sprite in group:
        if sprite.name == name:
            return sprite

def get_enemy(score:int) -> tuple:
    """
    check for score and return a type of enemy to be spawn and the velocity value of this enemy
    """
    random_number = randint(0,10)
    match score:
        case n if n < 10:
            enemy_type = 'ground'
            enemy_velocity = randint(10,20)

        case n if 10 <= n < 30 and 0 <= random_number <= 3:
            enemy_type = 'fly'
            enemy_velocity = randint(10,20)

        case n if 10 <= n < 30 and 3 < random_number <= 10:
            enemy_type = 'ground'
            enemy_velocity = randint(20,40)

        case n if 30 <= n < 50 and 0 <= random_number <= 3:
            enemy_type = 'fly'
            enemy_velocity = randint(20,30)

        case n if 30 <= n < 50 and 3 < random_number <= 10:
            enemy_type = 'ground'
            enemy_velocity = randint(40,50)
        case _:
            if 0<=random_number<5:
                enemy_type = 'fly'
                enemy_velocity = randint(40,60)
            else:
                enemy_type = 'ground'
                enemy_velocity = randint(50,70)

    return enemy_type,enemy_velocity

def get_seconds(score: int) ->int:
    """
    takes the score and return a value in miliseconds to use in a timer, at score= 0 base value =1500
    """
    seconds = round(2000 - (500* math.exp(0.02*score)))
    if seconds < 500:
        return 500
    return seconds

def main():
    pygame.init()
    #screen type
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
    game_width = 2000
    game_hight = 1000
    if screen_width < game_width or screen_height < game_hight:
        flags = pygame.FULLSCREEN | pygame.SCALED
    else:
        flags = pygame.RESIZABLE | pygame.SCALED
    
    #screen setup
    screen = pygame.display.set_mode((game_width,game_hight),flags)
    clock = pygame.time.Clock()
    game_running=True

    #objects
    player = pygame.sprite.GroupSingle()
    enemys = pygame.sprite.Group()
    text = pygame.sprite.Group()

    player.add(Player())

    #game variables
    score = 0

    #backgorund
    background_surface = pygame.Surface((2000,1000))
    background_surface.fill('Black')
    ground_surface = pygame.Surface((2000,200))
    ground_surface.fill('White')

    #score keeper
    score_check_rect = pygame.Rect(400,0,1,1000)

    #text
    text.add(Text('Game over',500,'Game over','Red',(1000,500)))

    #timer
    seconds = 1500
    enemy_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(enemy_timer,seconds)

    while True:
        #spawn modifier
        new_seconds = get_seconds(score)
        if (seconds-100) > new_seconds:
            pygame.time.set_timer(enemy_timer,new_seconds)
            seconds = new_seconds
            print(new_seconds)

        #key tracker
        keys = pygame.key.get_pressed()

        #score
        score_font = pygame.font.Font('graphics/Pixeltype.ttf',100)
        score_surface = score_font.render(f'Score  {score}',False,'White')
        score_rect = score_surface.get_rect(midbottom=(1000,200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if game_running:
                #enemy spawn
                if event.type == enemy_timer:
                    enemy_type,enemy_velocity = get_enemy(score)
                    enemys.add(Enemy(enemy_type,enemy_velocity))
                #key check
                if event.type == pygame.KEYDOWN:
                    #jump
                    if event.key == pygame.K_SPACE:
                        player.sprite.jump() 
                    #exit
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
            if not game_running:
                #restart game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_running=True
        
        if game_running:
            #rendering
            screen.blit(background_surface,(0,0))
            screen.blit(ground_surface,(0,800))
            screen.blit(score_surface,score_rect)
            player.draw(screen)
            player.update(keys)
            enemys.draw(screen)
            enemys.update()

            #collisions
            if collision_check(player,enemys):
                game_running=False

            #score keeping
            for enemy in enemys:
                if pygame.Rect.colliderect(enemy.rect,score_check_rect) and not enemy.has_scored:
                    score += 1
                    enemy.has_scored = True

        if not game_running:
            #rendering
            screen.blit(background_surface,(0,0))
            game_over = get_sprite('Game over',text)
            screen.blit(game_over.image,game_over.rect)

            #reset variables
            enemys.empty()
            score = 0
            seconds = 1500
            pygame.time.set_timer(enemy_timer,seconds)


        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()
